r"""E02 — Baseline network characterization + QC gate (CIS-blind).

Per the frozen protocol: cost threshold ladder {10, 15, 20, 25}% on the PRIMARY
weight (sift count) for every atlas and subject; baseline graph stats; QC gate
(PROTOCOL_FREEZE §5, CIS-blind) on the primary configuration defines the
QC-pass cohort.

Outputs:
    03_BASELINE/baseline_network_properties.csv
    03_BASELINE/qc_primary.csv
    03_BASELINE/BASELINE_RESULTS.md
    09_TABLES/table_baseline_network_properties.csv
"""
import json, os, sys, time
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components, shortest_path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "02_PREPROCESSING"))
from cache_io import (ATLASES, BASE, PRIMARY_ATLAS, PRIMARY_VARIANT,
                      get_matrix, load_key_index, threshold_cost)

COSTS = [0.10, 0.15, 0.20, 0.25]


def graph_stats(B):
    n = B.shape[0]
    ncc, labels = connected_components(B, directed=False)
    comp_sizes = np.bincount(labels)
    giant = int(comp_sizes.max())
    dist = shortest_path(B, method="D", unweighted=True, directed=False)
    off = dist[~np.eye(n, dtype=bool)]
    finite = off[np.isfinite(off)]
    ge = float((1.0 / finite[finite > 0]).sum() / (n * (n - 1))) if len(finite) else 0.0
    diag = np.diag(dist)
    finite_d = diag[np.isfinite(diag) & (diag > 0)]
    cpl = float(finite_d.mean()) if len(finite_d) else float("nan")
    deg = (B != 0).sum(1).A1 if hasattr((B != 0), "A1") else np.asarray((B != 0).sum(1)).ravel()
    return {"ge": ge, "cpl": cpl, "n_components_excl_singletons": int((comp_sizes > 1).sum()),
            "giant_frac": giant / n, "mean_degree": float(deg.mean()),
            "edges": int(deg.sum() // 2)}


def process_subject(sub):
    """Worker: baseline stats for one subject across all atlases x cost ladder.
    Returns (rows, qcrow) for that subject only (RAM-safe)."""
    index = load_key_index()
    rows, qcrow = [], []
    for atlas in ATLASES:
        key = (sub, atlas, PRIMARY_VARIANT)
        if key not in index:
            continue
        A = get_matrix(index, sub, atlas, PRIMARY_VARIANT, dtype=np.float64)
        for cost in COSTS:
            B = threshold_cost(A, cost)
            st = graph_stats(B)
            rows.append({"subject": sub, "atlas": atlas, "cost": cost, **st})
            if atlas == PRIMARY_ATLAS and cost == 0.15:
                n = A.shape[0]
                deg = np.asarray((B != 0).sum(1)).ravel()
                isolated = int((deg == 0).sum())
                W = A.copy(); np.fill_diagonal(W, 0.0)
                off = W[~np.eye(n, dtype=bool)]  # flat: off-diagonal values
                density = (off != 0).mean()
                strength = np.abs(W).sum(1)  # row sums of |W| (diag already 0)
                qcrow.append({
                    "subject": sub, "n_nodes": n, "density_raw": float(density),
                    "isolated_nodes_post_threshold": isolated,
                    "n_components_multi": st["n_components_excl_singletons"],
                    "giant_frac": st["giant_frac"], "ge": st["ge"],
                    "strength_mean": float(strength.mean()),
                })
    return rows, qcrow


def main():
    t0 = time.time()
    index = load_key_index()
    subjects = sorted({s for s, _, _ in index})
    print(f"[E02] cache index: {len(index)} matrices, {len(subjects)} subjects",
          flush=True)

    from concurrent.futures import ProcessPoolExecutor
    rows, qcrow = [], []
    done = 0
    with ProcessPoolExecutor(max_workers=min(8, os.cpu_count() or 4)) as ex:
        for r, q in ex.map(process_subject, subjects):
            rows.extend(r)
            qcrow.extend(q)
            done += 1
            if done % 100 == 0 or done == len(subjects):
                print(f"[E02] {done}/{len(subjects)} subjects at "
                      f"{time.time()-t0:.0f}s", flush=True)

    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(BASE, "03_BASELINE", "baseline_network_properties.csv"), index=False)
    df.to_csv(os.path.join(BASE, "09_TABLES", "table_baseline_network_properties.csv"), index=False)

    # QC gate on primary configuration (CIS-blind, PROTOCOL_FREEZE §5)
    qc = pd.DataFrame(qcrow)
    med = qc[["density_raw", "strength_mean"]].median()
    q1 = qc[["density_raw", "strength_mean"]].quantile(0.25)
    q3 = qc[["density_raw", "strength_mean"]].quantile(0.75)
    iqr = q3 - q1
    qc["flag_density_iqr"] = (qc.density_raw < med.density_raw - 3*iqr.density_raw) | \
                             (qc.density_raw > med.density_raw + 3*iqr.density_raw)
    qc["flag_strength_iqr"] = (qc.strength_mean < med.strength_mean - 3*iqr.strength_mean) | \
                              (qc.strength_mean > med.strength_mean + 3*iqr.strength_mean)
    qc["flag_components"] = qc.n_components_multi > 1  # >1 multi-node component = giant + fragment (giant alone is normal)
    qc["flag_isolated"] = qc.isolated_nodes_post_threshold > 0
    flag_cols = [c for c in qc.columns if c.startswith("flag_")]
    qc["qc_pass"] = ~qc[flag_cols].any(axis=1)
    qc.to_csv(os.path.join(BASE, "03_BASELINE", "qc_primary.csv"), index=False)

    summary = {
        "subjects": int(len(subjects)),
        "rows": int(len(df)),
        "elapsed_s": round(time.time() - t0, 1),
        "qc_pass_n": int(qc.qc_pass.sum()),
        "qc_flagged_n": int((~qc.qc_pass).sum()),
        "qc_flag_counts": {c: int(qc[c].sum()) for c in flag_cols},
        "primary_ge_median_15pct": float(qc["ge"].median()),
        "primary_giant_frac_median": float(qc["giant_frac"].median()),
    }
    with open(os.path.join(BASE, "03_BASELINE", "baseline_summary.json"), "w") as f:
        json.dump(summary, f, indent=1)
    print("[E02] DONE", summary)


if __name__ == "__main__":
    main()
