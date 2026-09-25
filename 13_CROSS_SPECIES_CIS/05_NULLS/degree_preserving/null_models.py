r"""E04 — Degree-preserving null battery (frozen PROTOCOL_FREEZE §4).

Port of fruitfly/src/experiments/null_models.py Maslov-Sneppen semantics to
undirected simple graphs, with the fly project's adversarial regression tests
(hub-selfloop/pendant, dense, ring) re-run on the undirected variant.

CIS on null graphs uses cache_io.node_cis_fast (boolean-matmul all-pairs),
gated by a mandatory equivalence validation vs the scipy node_cis reference
(used for all observed/E03 numbers) on real subject graphs before any battery.

Frozen scope:
  (a) subject sample n=100 (seed 20260922) x 100 nulls each: FULL per-node
      CIS per null graph -> per-node degree-matched empirical p.
  (b) 200 subjects (same seed, includes the 100) x 100 nulls each: CIS at the
      subject's top-50 observed-CIS positions -> population summary statistic.
  Null seeds: 100+i per graph; rejection redraw on preservation failure.

Outputs (resume-safe):
  05_NULLS/degree_preserving/FAST_IMPLEMENTATION_VALIDATION.md
  05_NULLS/degree_preserving/regression_tests_undirected.csv/.json
  05_NULLS/degree_preserving/battery_a/sub-XXXX_nulls.npz   (100 x 456 CIS)
  05_NULLS/degree_preserving/battery_b/sub-XXXX_battery_b.csv
  05_NULLS/degree_preserving/null_manifest_battery_a.csv
  05_NULLS/degree_preserving/null_validation_battery_a.csv
  05_NULLS/degree_preserving/null_results_battery_b.csv
"""
import faulthandler
faulthandler.enable()
import argparse, json, os, sys, time

import numpy as np
import io
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "02_PREPROCESSING"))
from cache_io import (BASE, PRIMARY_ATLAS, PRIMARY_VARIANT, allpairs_dist,
                      get_matrix, global_efficiency, load_key_index,
                      node_cis, node_cis_fast, node_cis_fast_at,
                      threshold_cost)

COST = 0.15
N_NULLS = 100
N_PER_CHUNK = 5          # nulls per atomic part-checkpoint (~2 min of work)
SEED_BASE = 100          # nulls 100+i per graph
SUBJECT_SEED = 20260922  # frozen subject-sample seed
OUT = os.path.join(BASE, "05_NULLS", "degree_preserving")
A_DIR = os.path.join(OUT, "battery_a")
B_DIR = os.path.join(OUT, "battery_b")


# ----------------------------------------------------------------------------
# Maslov-Sneppen rewiring (undirected port of the fly implementation)
# ----------------------------------------------------------------------------

def maslov_sneppen_undirected(A, n_swaps_factor=10, seed=0):
    """Rewire preserving the EXACT per-node degree sequence.

    Picks two edges (u1,v1),(u2,v2) and swaps targets to (u1,v2),(u2,v1),
    rejecting self-loops, duplicate edges, and degenerate picks — faithful to
    the fly directed implementation's semantics. Edges canonicalized u<v.
    Returns (csr_binary_graph, info_dict).
    """
    rng = np.random.default_rng(seed)
    Ac = A.tocoo()
    n = Ac.shape[0]
    u, v = Ac.row.astype(np.int64), Ac.col.astype(np.int64)
    lo, hi = np.minimum(u, v), np.maximum(u, v)
    keep = lo != hi
    lo, hi = lo[keep], hi[keep]
    # Deduplicate canonicalized edges: a symmetric input stores each undirected
    # edge twice (i,j) and (j,i); the slot array must hold each edge ONCE or
    # edge_set bookkeeping and degree preservation silently diverge.
    _, uniq_idx = np.unique(
        lo * np.int64(n) + hi, return_index=True)
    u, v = lo[np.sort(uniq_idx)].copy(), hi[np.sort(uniq_idx)].copy()
    m = len(u)
    if m < 2:
        return A.tocsr(), {"n_swaps": 0, "accepted": 0}

    n_swaps = m * n_swaps_factor
    edge_set = set(zip(u.tolist(), v.tolist()))
    accepted = 0
    for _ in range(n_swaps):
        i1, i2 = rng.integers(0, m, size=2)
        if i1 == i2:
            continue
        u1, v1, u2, v2 = int(u[i1]), int(v[i1]), int(u[i2]), int(v[i2])
        if u1 == u2 or v1 == v2:
            continue
        n1 = (min(u1, v2), max(u1, v2))
        n2 = (min(u2, v1), max(u2, v1))
        if n1[0] == n1[1] or n2[0] == n2[1]:
            continue
        if n1 == n2:
            continue
        e1 = (min(u1, v1), max(u1, v1))
        e2 = (min(u2, v2), max(u2, v2))
        if n1 in edge_set or n2 in edge_set:
            continue
        edge_set.discard(e1)
        edge_set.discard(e2)
        edge_set.add(n1)
        edge_set.add(n2)
        u[i1], v[i1] = n1
        u[i2], v[i2] = n2
        accepted += 1

    from scipy.sparse import csr_matrix
    N = csr_matrix((np.ones(2 * m), (np.concatenate([u, v]),
                                     np.concatenate([v, u]))), shape=(n, n))
    N.sum_duplicates()
    N.data[:] = 1.0
    return N, {"n_swaps": int(n_swaps), "accepted": int(accepted)}


def verify_degree_preserved(B_null, B_obs):
    """Exact verification: per-node degree sequence identical, edge count
    identical, no self-loops, binary values only."""
    d0 = np.asarray((B_obs != 0).sum(1)).ravel()
    d1 = np.asarray((B_null != 0).sum(1)).ravel()
    return {
        "degree_per_node_exact": bool(np.array_equal(d0, d1)),
        "edges_match": bool(int(d0.sum()) == int(d1.sum())),
        "n_edges_null": int(d1.sum() // 2),
        "self_loops": int((B_null.diagonal() != 0).sum()),
        "binary_values_only": bool(float(abs(B_null).max()) <= 1.0 + 1e-12),
    }


# ----------------------------------------------------------------------------
# Adversarial regression tests (fly convention, undirected variant)
# ----------------------------------------------------------------------------

def run_regression_tests():
    from scipy.sparse import csr_matrix
    from scipy.sparse.csgraph import connected_components
    results = []

    def check(name, B, seed=0):
        N, info = maslov_sneppen_undirected(B, seed=seed)
        ver = verify_degree_preserved(N, B)
        _, lab = connected_components(N, directed=False)
        ver["giant_frac"] = float(np.bincount(lab).max() / N.shape[0])
        results.append({"test": name, **ver, **info})
        return ver

    # 1) hub + pendant edge (hub-selfloop trap, undirected)
    n = 30
    rows, cols = [], []
    for j in range(1, 15):
        rows += [0, j]; cols += [j, 0]
    rows += [1, 2]; cols += [2, 1]
    check("hub_pendant", csr_matrix((np.ones(len(rows)), (rows, cols)),
                                    shape=(n, n)))

    # 2) dense graph (p ~ 0.6)
    rng = np.random.default_rng(1)
    n = 60
    W = rng.random((n, n))
    W = np.triu(W, 1)
    W[W < 0.4] = 0
    W += W.T
    check("dense_p60", csr_matrix(W))

    # 3) ring (degree 2 everywhere)
    n = 40
    W = np.zeros((n, n))
    a = np.arange(n)
    W[a, (a + 1) % n] = 1
    W[(a + 1) % n, a] = 1
    check("ring_k2", csr_matrix(W))

    df = pd.DataFrame(results)
    os.makedirs(OUT, exist_ok=True)
    df.to_csv(os.path.join(OUT, "regression_tests_undirected.csv"), index=False)
    ok = bool(df.degree_per_node_exact.all() and df.edges_match.all()
              and (df.self_loops == 0).all() and df.binary_values_only.all())
    with open(os.path.join(OUT, "regression_tests_undirected.json"), "w") as f:
        json.dump({"pass": ok, "tests": results}, f, indent=1)
    print(f"[E04] regression tests: {'PASS' if ok else 'FAIL'}")
    return ok


# ----------------------------------------------------------------------------
# Fast-CIS equivalence validation (gates the batteries)
# ----------------------------------------------------------------------------

def validate_fast_cis(n_subjects=3):
    """node_cis (scipy, used for all observed results) vs node_cis_fast
    (matmul, used on null graphs) must agree to 1e-9 on real subject graphs."""
    index = load_key_index()
    subs = sorted(s for (s, a, v) in index
                  if a == PRIMARY_ATLAS and v == PRIMARY_VARIANT)[:n_subjects]
    rows = []
    for sub in subs:
        A = get_matrix(index, sub, PRIMARY_ATLAS, PRIMARY_VARIANT,
                       dtype=np.float64)
        B = threshold_cost(A, COST)
        c_ref, e_ref = node_cis(B)
        c_fast, e_fast = node_cis_fast(B)
        dev = float(np.abs(c_ref - c_fast).max())
        rows.append({"subject": int(sub), "max_abs_dev_cis": dev,
                     "abs_dev_e0": abs(e_ref - e_fast),
                     "pass": bool(dev < 1e-9 and abs(e_ref - e_fast) < 1e-12)})
    ok = bool(pd.DataFrame(rows)["pass"].all())
    lines = ["# FAST CIS IMPLEMENTATION VALIDATION (E04)", "",
             f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}",
             "node_cis (scipy all-pairs; used for all OBSERVED results) vs",
             "node_cis_fast (boolean-matmul all-pairs; used for NULL graphs).",
             "Frozen tolerance: max|dCIS| < 1e-9, |dE0| < 1e-12.", "",
             "| subject | max abs dev CIS | abs dev E0 | pass |", "|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['subject']} | {r['max_abs_dev_cis']:.3e} | "
                     f"{r['abs_dev_e0']:.3e} | {r['pass']} |")
    lines += ["", f"**VALIDATION: {'PASS' if ok else 'FAIL'}**"]
    with open(os.path.join(OUT, "FAST_IMPLEMENTATION_VALIDATION.md"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"[E04] fast-CIS validation: {'PASS' if ok else 'FAIL'}")
    return ok


# ----------------------------------------------------------------------------
# Subject samples (frozen, nested, single seed)
# ----------------------------------------------------------------------------

def subject_samples(qc_pass_subjects):
    rng = np.random.default_rng(SUBJECT_SEED)
    perm = rng.permutation(np.sort(np.asarray(list(qc_pass_subjects),
                                              dtype=int)))
    return perm[:100], perm[:200]  # (a), (b)


def _null_cis_one(B_obs, seed, nodes=None):
    """One degree-preserving null -> (cis_at_nodes, e0, ver, info, attempts, rt).

    nodes=None computes the full 456-node CIS vector (battery A); an index
    array computes CIS only at those positions (battery B, ~9x cheaper).
    The rewired graph and all verification are identical in both modes.
    """
    for attempt in range(5):
        N, info = maslov_sneppen_undirected(B_obs,
                                            seed=seed + 1000 * attempt)
        ver = verify_degree_preserved(N, B_obs)
        if ver["degree_per_node_exact"] and ver["edges_match"] \
                and ver["self_loops"] == 0 and ver["binary_values_only"]:
            break
    else:
        raise RuntimeError(f"null preservation failed after 5 attempts "
                           f"(seed {seed})")
    from scipy.sparse.csgraph import connected_components
    _, lab = connected_components(N, directed=False)
    ver["giant_frac"] = float(np.bincount(lab).max() / N.shape[0])
    t0 = time.time()
    if nodes is None:
        cis, e0 = node_cis_fast(N)
    else:
        cis, e0 = node_cis_fast_at(N, np.asarray(nodes))
    return cis, float(e0), ver, info, attempt + 1, time.time() - t0


# ----------------------------------------------------------------------------
# Batteries
# ----------------------------------------------------------------------------

def _battery_a_chunk(job):
    """Worker: nulls [i0, i0+n) for one subject -> one atomic part file.

    Chunk-level checkpoints: every part (~N_PER_CHUNK * ~15s of work) lands
    well inside any compute window; assembly into the final npz is a cheap,
    atomic rename once all 20 parts exist. Killed batches therefore lose at
    most one chunk, not a whole subject.
    Returns (sub, i0, n_per_chunk, elapsed_s, n_ok).
    """
    sub, i0, n_per_chunk = job
    index = load_key_index()
    A = get_matrix(index, sub, PRIMARY_ATLAS, PRIMARY_VARIANT, dtype=np.float64)
    B_obs = threshold_cost(A, COST)
    n = B_obs.shape[0]
    t0 = time.time()
    nulls = np.zeros((n_per_chunk, n), dtype=np.float32)
    e0s = np.zeros(n_per_chunk)
    man_rows, val_rows = [], []
    n_ok = 0
    for k in range(n_per_chunk):
        i = i0 + k
        if i >= N_NULLS:
            break
        seed = SEED_BASE + i
        cis, e0, ver, info, attempts, rt = _null_cis_one(B_obs, seed)
        nulls[k] = cis
        e0s[k] = e0
        n_ok += 1
        man_rows.append({"subject": sub, "null_id": i, "seed": seed,
                         "rewire_accepted": info["accepted"],
                         "n_swaps_factor": 10, "attempts": attempts,
                         "cis_runtime_s": round(rt, 3), "status": "ok"})
        val_rows.append({"subject": sub, "null_id": i, **ver})
    buf = io.BytesIO()
    np.savez_compressed(buf, null_cis=nulls, e0_nulls=e0s,
                        subject=np.int64(sub), i0=np.int64(i0))
    tmp = os.path.join(A_DIR, f"sub-{sub:04d}_part_{i0:03d}.npz.tmp")
    with open(tmp, "wb") as f:
        f.write(buf.getvalue())
    os.replace(tmp, os.path.join(A_DIR, f"sub-{sub:04d}_part_{i0:03d}.npz"))
    pd.DataFrame(man_rows).to_csv(
        os.path.join(A_DIR, f"sub-{sub:04d}_manifest_{i0:03d}.csv"),
        index=False)
    pd.DataFrame(val_rows).to_csv(
        os.path.join(A_DIR, f"sub-{sub:04d}_validation_{i0:03d}.csv"),
        index=False)
    return (sub, i0, n_per_chunk, round(time.time() - t0, 1), n_ok)


def _assemble_battery_a_subject(sub):
    """Merge this subject's part files into the final npz + unified tables
    (atomic rename; idempotent; then delete parts)."""
    parts = sorted(f for f in os.listdir(A_DIR)
                   if f.startswith(f"sub-{sub:04d}_part_")
                   and f.endswith(".npz"))
    if not parts:
        return False
    cis_blocks, e0_blocks, i0s = [], [], []
    for f in parts:
        with np.load(os.path.join(A_DIR, f)) as z:
            cis_blocks.append(z["null_cis"])
            e0_blocks.append(z["e0_nulls"])
            i0s.append(int(z["i0"]))
    order = np.argsort(i0s)
    cis_blocks = [cis_blocks[j] for j in order]
    e0_blocks = [e0_blocks[j] for j in order]
    if sum(b.shape[0] for b in cis_blocks) != N_NULLS:
        return False  # incomplete; leave parts in place
    nulls = np.concatenate(cis_blocks, axis=0)
    e0s = np.concatenate(e0_blocks, axis=0)
    buf = io.BytesIO()
    np.savez_compressed(buf, null_cis=nulls, e0_nulls=e0s,
                        subject=np.int64(sub))
    tmp = os.path.join(A_DIR, f"sub-{sub:04d}_nulls.npz.tmp")
    with open(tmp, "wb") as f:
        f.write(buf.getvalue())
    os.replace(tmp, os.path.join(A_DIR, f"sub-{sub:04d}_nulls.npz"))
    for f in parts:
        os.remove(os.path.join(A_DIR, f))
    return True


def _battery_a_subject(sub):
    """Legacy whole-subject worker (kept for reference; chunked path is used)."""
    pass


def battery_a(start=0, stop=0, workers=8):
    """(a) n=100 subjects x 100 nulls: full per-node CIS per null graph.
    Work is submitted as (subject, chunk) jobs -> atomic part checkpoints;
    finished subjects are assembled from their parts automatically.
    """
    qc = pd.read_csv(os.path.join(BASE, "03_BASELINE", "qc_primary.csv"))
    sample_a, _ = subject_samples(qc.loc[qc.qc_pass, "subject"].values)
    if stop:
        sample_a = sample_a[start:stop]
    elif start:
        sample_a = sample_a[start:]
    os.makedirs(A_DIR, exist_ok=True)
    sample_a = [int(s) for s in sample_a]

    jobs = []
    for s in sample_a:
        if os.path.exists(os.path.join(A_DIR, f"sub-{s:04d}_nulls.npz")):
            continue
        have = set()
        for f in os.listdir(A_DIR):
            if f.startswith(f"sub-{s:04d}_part_") and f.endswith(".npz"):
                have.add(int(f[14:17]))
        for i0 in range(0, N_NULLS, N_PER_CHUNK):
            if i0 not in have:
                jobs.append((s, i0, N_PER_CHUNK))
    print(f"[E04a] {len(sample_a)} sampled subjects, {len(jobs)} chunk jobs "
          f"({N_PER_CHUNK} nulls each), {workers} workers", flush=True)
    t0 = time.time()
    done = 0
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for sub, i0, npc, dt, n_ok in ex.map(_battery_a_chunk, jobs,
                                             chunksize=1):
            done += 1
            if done % 5 == 0 or done == len(jobs):
                rate = done / (time.time() - t0)
                eta = (len(jobs) - done) / max(rate, 1e-9)
                print(f"[E04a] chunks {done}/{len(jobs)} last=sub{sub}+{i0} "
                      f"({dt:.0f}s) eta={eta/60:.0f}min", flush=True)
    for s in sample_a:
        if _assemble_battery_a_subject(s):
            print(f"[E04a] assembled sub-{s:04d}", flush=True)
    _merge_battery_a_manifests()
    print(f"[E04a] DONE in {(time.time()-t0)/60:.1f} min")


def _merge_battery_a_manifests():
    """Concatenate per-subject manifest/validation rows into battery files.

    Chunked battery A writes sub-XXXX_manifest_000.csv / sub-XXXX_validation_000.csv
    (one per 5-null chunk), so the match is on the '_manifest_'/'_validation_'
    infix, not the '_manifest.csv' suffix (which matched only the legacy
    whole-subject layout and silently produced empty battery files).
    """
    man = [pd.read_csv(os.path.join(A_DIR, f)) for f in sorted(os.listdir(A_DIR))
           if "_manifest_" in f and f.endswith(".csv")]
    val = [pd.read_csv(os.path.join(A_DIR, f)) for f in sorted(os.listdir(A_DIR))
           if "_validation_" in f and f.endswith(".csv")]
    if man:
        pd.concat(man, ignore_index=True).sort_values(["subject", "null_id"]).to_csv(
            os.path.join(OUT, "null_manifest_battery_a.csv"), index=False)
    if val:
        pd.concat(val, ignore_index=True).sort_values(["subject", "null_id"]).to_csv(
            os.path.join(OUT, "null_validation_battery_a.csv"), index=False)


def _battery_b_subject(sub):
    """Worker: top-50-position null statistic for one subject.

    Reuses battery A's stored full-CIS nulls when the subject is in sample A
    (identical seeds -> identical null graphs -> exact reuse, no statistical
    difference; recorded in the manifest as source=battery_a_reuse).
    """
    sub = int(sub)
    index = load_key_index()
    ckpt = os.path.join(BASE, "04_CIS", "subject_cis", f"sub-{sub:04d}.csv")
    if os.path.exists(ckpt):
        cis_obs = pd.read_csv(ckpt).cis.values
    else:
        A = get_matrix(index, sub, PRIMARY_ATLAS, PRIMARY_VARIANT,
                       dtype=np.float64)
        cis_obs, _ = node_cis(threshold_cost(A, COST))
    top = np.argsort(-cis_obs)[:50]
    obs_median = float(np.median(cis_obs[top]))

    npz = os.path.join(A_DIR, f"sub-{sub:04d}_nulls.npz")
    if os.path.exists(npz):
        with np.load(npz) as z:
            null_medians = np.median(z["null_cis"][:, top], axis=1)
        source = "battery_a_reuse"
    else:
        A = get_matrix(index, sub, PRIMARY_ATLAS, PRIMARY_VARIANT,
                       dtype=np.float64)
        B_obs = threshold_cost(A, COST)
        null_medians = np.zeros(N_NULLS)
        for i in range(N_NULLS):
            cis_n, _, _, _, _, _ = _null_cis_one(B_obs, SEED_BASE + i,
                                                 nodes=top)
            null_medians[i] = np.median(cis_n)
        source = "fresh"

    emp_p = (float((null_medians >= obs_median).sum()) + 1.0) / (N_NULLS + 1.0)
    mu, sd = float(null_medians.mean()), float(null_medians.std(ddof=1))
    z = (obs_median - mu) / sd if sd > 0 else 0.0
    out_csv = os.path.join(B_DIR, f"sub-{sub:04d}_battery_b.csv")
    pd.DataFrame({
        "subject": [sub], "top50_median_observed": [obs_median],
        "top50_median_null_mean": [mu], "top50_median_null_sd": [sd],
        "z_vs_null": [z], "emp_p_ge": [emp_p], "n_nulls": [N_NULLS],
        "null_source": [source],
    }).to_csv(out_csv, index=False)
    return sub, source


def battery_b(start=0, stop=0, workers=8):
    """(b) n=200 subjects x 100 nulls: CIS at top-50 observed positions."""
    qc = pd.read_csv(os.path.join(BASE, "03_BASELINE", "qc_primary.csv"))
    _, sample_b = subject_samples(qc.loc[qc.qc_pass, "subject"].values)
    if stop:
        sample_b = sample_b[start:stop]
    elif start:
        sample_b = sample_b[start:]
    os.makedirs(B_DIR, exist_ok=True)
    todo = [s for s in sample_b
            if not os.path.exists(os.path.join(B_DIR, f"sub-{int(s):04d}_battery_b.csv"))]
    print(f"[E04b] {len(sample_b)} sampled, {len(todo)} to compute, "
          f"{workers} workers", flush=True)
    t0 = time.time()
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for k, (sub, source) in enumerate(ex.map(_battery_b_subject, todo)):
            if (k + 1) % 10 == 0 or k + 1 == len(todo):
                print(f"[E04b] {k+1}/{len(todo)} last={sub}({source}) "
                      f"at {(time.time()-t0)/60:.1f} min", flush=True)
    allb = [pd.read_csv(os.path.join(B_DIR, f)) for f in
            sorted(os.listdir(B_DIR)) if f.endswith("_battery_b.csv")]
    pd.concat(allb, ignore_index=True).sort_values("subject").to_csv(
        os.path.join(OUT, "null_results_battery_b.csv"), index=False)
    print(f"[E04b] DONE in {(time.time()-t0)/60:.1f} min")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true")
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--battery", choices=["a", "b"], default=None)
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--stop", type=int, default=0)
    ap.add_argument("--no-validate", action="store_true",
                    help="skip gates (only after PASS in identical code state)")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    if args.test:
        run_regression_tests()
        return
    if args.validate:
        validate_fast_cis()
        return
    if args.battery:
        if not args.no_validate:
            ok = run_regression_tests() and validate_fast_cis()
            if not ok:
                print("[E04] gates FAILED — battery aborted")
                return
        if args.battery == "a":
            battery_a(args.start, args.stop, workers=args.workers)
        else:
            battery_b(args.start, args.stop, workers=args.workers)
    else:
        print("nothing to do: pass --test / --validate / --battery a|b")


if __name__ == "__main__":
    main()
