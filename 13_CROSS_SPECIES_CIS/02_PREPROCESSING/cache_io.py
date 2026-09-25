r"""Shared cache loader + frozen graph utilities (single source of truth).

The E01 v2 cache stores one npz part per raw zip:
    02_PREPROCESSING/cache_parts/cache_part_NN.npz
    02_PREPROCESSING/cache_keys.csv   (key, subject, atlas, variant, part_file)

Math here is the FROZEN convention (PROTOCOL_FREEZE.md §2):
  - threshold_cost: binarize keeping top floor-ish (round) c * N(N-1)/2
    off-diagonal entries by weight; diagonal zeroed; undirected.
  - global efficiency on the binary unweighted graph.
"""
import os

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path

BASE = r"D:\humanbrain\humanbrain\13_CROSS_SPECIES_CIS"
PARTS_DIR = os.path.join(BASE, "02_PREPROCESSING", "cache_parts")
KEYS_CSV = os.path.join(BASE, "02_PREPROCESSING", "cache_keys.csv")

ATLASES = ["atlas_4S456Parcels", "atlas_4S256Parcels", "atlas_4S156Parcels",
           "atlas_Brainnetome246Ext", "atlas_AICHA384Ext", "atlas_Gordon333Ext",
           "atlas_AAL116"]
VARIANTS = ["sift_radius2_count_connectivity",
            "sift_invnodevol_radius2_count_connectivity",
            "radius2_count_connectivity",
            "radius2_meanlength_connectivity"]
PRIMARY_ATLAS = "atlas_4S456Parcels"
PRIMARY_VARIANT = "sift_radius2_count_connectivity"


def load_key_index():
    """(subject, atlas, variant) -> (part_path, member_name)."""
    idx = pd.read_csv(KEYS_CSV, dtype={"key": str, "part_file": str})
    out = {}
    for r in idx.itertuples(index=False):
        out[(int(r.subject), r.atlas, r.variant)] = (
            os.path.join(PARTS_DIR, r.part_file), r.key.replace("|", "__"))
    return out


def get_matrix(index, subject, atlas, variant, dtype=np.float32):
    """Load one cached matrix (fp32 on disk -> requested dtype)."""
    part_path, member = index[(int(subject), atlas, variant)]
    with np.load(part_path, allow_pickle=False) as z:
        return z[member].astype(dtype, copy=False)


def threshold_cost(A, cost):
    """Binary graph keeping top `cost` fraction of off-diagonal weights.

    Frozen: k = round(cost * N(N-1)/2) largest |off-diagonal| entries
    (count weights are >= 0); diagonal zeroed; output symmetric binary csr.
    Ties at the k-th value are resolved deterministically by argpartition
    (same input array -> same selected set).
    """
    n = A.shape[0]
    W = np.asarray(A, dtype=np.float64).copy()
    np.fill_diagonal(W, 0.0)
    m = n * (n - 1) // 2
    k = int(round(cost * m))
    iu = np.triu_indices(n, 1)
    w = W[iu]
    if k == 0:
        return csr_matrix((n, n))
    idx = np.argpartition(w, -k)[-k:]
    mask = np.zeros_like(w, dtype=bool)
    mask[idx] = True
    B = np.zeros_like(W)
    B[iu[0][mask], iu[1][mask]] = 1.0
    B += B.T
    return csr_matrix(B)


def allpairs_dist(B):
    """Exact all-pairs unweighted shortest paths on binary graph B (dense)."""
    return shortest_path(B, method="D", unweighted=True, directed=False)


def allpairs_dist_fast(Ab):
    """Exact all-pairs unweighted distances via boolean-reachability matmuls.

    Ab: dense 0/1 adjacency. P_k = binarized A^k marks nodes reached by a
    walk of exactly k steps; first-k-reached assignment gives exact shortest
    distances ( walks >= shortest paths, and any shorter walk would have
    assigned an earlier k ). Terminates when no node is newly reached, so it
    runs O(diameter) multiplies (diameter ~4 at 15% cost on 4S456).
    Validated against scipy allpairs_dist: identical finite-distance pattern
    and values on real subject graphs (E04 validation report).
    """
    n = Ab.shape[0]
    A = (np.asarray(Ab) != 0).astype(np.float32)
    np.fill_diagonal(A, 0.0)  # defensive: kill self-loops on a private copy
    P = A.copy()
    dist = np.where(A > 0, 1.0, np.inf)
    np.fill_diagonal(dist, 0.0)
    for k in range(2, n + 1):
        P = (P @ A) > 0  # exactly-k-step reachability
        P = P.astype(np.float32)
        newly = (P > 0) & np.isinf(dist)
        if not newly.any():
            break
        dist[newly] = float(k)
    return dist


def node_cis_fast(B):
    """node_cis with allpairs_dist_fast (identical math, BLAS multiplies).

    Removal is handled by zeroing row/col i of the working adjacency instead
    of building an (n-1)x(n-1) copy per node: paths THROUGH node i then
    disappear, so the resulting distance matrix equals the induced-subgraph
    distance matrix exactly (mathematically identical; faster than np.ix_
    copies). The original row/col are restored after each measurement.
    """
    n = B.shape[0]
    if n < 3:
        raise ValueError("node_cis_fast requires n >= 3")
    Ab = (B.toarray() if hasattr(B, "toarray") else np.asarray(B)) != 0
    Ab = Ab.astype(np.float32)
    e0 = global_efficiency(allpairs_dist_fast(Ab))
    cis = np.zeros(n)
    for i in range(n):
        row_i = Ab[i, :].copy()
        col_i = Ab[:, i].copy()
        Ab[i, :] = 0.0
        Ab[:, i] = 0.0
        d = allpairs_dist_fast(Ab)
        # global_efficiency normalizes by n(n-1) over the full matrix; the
        # reference E(G-i) is over the induced (n-1)-node subgraph, i.e. the
        # same numerator (i-blocks contribute 0) divided by (n-1)(n-2).
        s = global_efficiency(d) * n * (n - 1)
        E_i = s / ((n - 1) * (n - 2))
        cis[i] = (e0 - E_i) / e0
        Ab[i, :] = row_i
        Ab[:, i] = col_i
    return cis, e0


def node_cis_fast_at(B, nodes):
    """node_cis_fast evaluated only at the given node indices.

    Each CIS(i) is an independent computation, so restricting the output to
    `nodes` is mathematically identical to the full vector restricted a
    posteriori; inherits the node_cis_fast reference validation (1e-9).
    Used by battery B (top-50 positions) -> ~9x cheaper per null graph.
    Returns (cis_at_nodes, e0).
    """
    n = B.shape[0]
    if n < 3:
        raise ValueError("node_cis_fast_at requires n >= 3")
    Ab = (B.toarray() if hasattr(B, "toarray") else np.asarray(B)) != 0
    Ab = Ab.astype(np.float32)
    e0 = global_efficiency(allpairs_dist_fast(Ab))
    cis = np.zeros(len(nodes))
    for j, i in enumerate(nodes):
        i = int(i)
        row_i = Ab[i, :].copy()
        col_i = Ab[:, i].copy()
        Ab[i, :] = 0.0
        Ab[:, i] = 0.0
        d = allpairs_dist_fast(Ab)
        s = global_efficiency(d) * n * (n - 1)
        E_i = s / ((n - 1) * (n - 2))  # see node_cis_fast: subgraph normalization
        cis[j] = (e0 - E_i) / e0
        Ab[i, :] = row_i
        Ab[:, i] = col_i
    return cis, e0


def global_efficiency(dist):
    """E = (1/(N(N-1))) * sum_{i≠j} 1/d(i,j); inf/cross-component -> 0."""
    n = dist.shape[0]
    off = dist[~np.eye(n, dtype=bool)]
    inv = np.where(np.isfinite(off) & (off > 0), 1.0 / off, 0.0)
    return inv.sum() / (n * (n - 1))


def node_cis(B):
    """Exact per-node CIS for binary graph B.

    CIS(i) = (E(G) - E(G-i)) / E(G); E(G-i) recomputed exactly on the
    induced (N-1)-node subgraph. Node i is restored for every measurement.
    Returns (cis_vector, E0).
    """
    n = B.shape[0]
    e0 = global_efficiency(allpairs_dist(B))
    cis = np.zeros(n)
    for i in range(n):
        keep = np.ones(n, dtype=bool)
        keep[i] = False
        d = allpairs_dist(B[np.ix_(keep, keep)])
        cis[i] = (e0 - global_efficiency(d)) / e0
    return cis, e0
