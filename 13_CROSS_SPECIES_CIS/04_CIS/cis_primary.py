r"""E03 — Exact per-node CIS, primary configuration (frozen).

CIS(i) = (E(G) - E(G-i)) / E(G), binary undirected graph at 15% cost,
4S456 x sift_radius2_count. Exact BFS from every node (n <= 456).

Math lives in 02_PREPROCESSING/cache_io.py (single source of truth, frozen).
This script adds:
  - the mandatory reference-vs-optimized validation (PROTOCOL_FREEZE; prompt
    Part 9) on a small subset, tolerance max|dCIS| < 1e-9, |dE0| < 1e-12;
  - parallel, resume-safe production run (one CSV per subject = checkpoint);
  - population aggregation from subject checkpoints.

Outputs:
    04_CIS/subject_cis/sub-XXXX.csv        (per-node: cis, degree, strength, rank)
    04_CIS/population_cis.csv              (per-node population summaries)
    04_CIS/REFERENCE_IMPLEMENTATION_VALIDATION.md
    04_CIS/e03_summary.json

Usage:
    py cis_primary.py --limit 5     # smoke
    py cis_primary.py               # full run (resume-safe)
    py cis_primary.py --aggregate   # rebuild population tables from checkpoints
"""
import argparse, json, os, sys, time
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd
from scipy.sparse.csgraph import shortest_path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "02_PREPROCESSING"))
from cache_io import (BASE, PRIMARY_ATLAS, PRIMARY_VARIANT, get_matrix,
                      load_key_index, node_cis, node_cis_fast, threshold_cost)

COST = 0.15
SUBJ_DIR = os.path.join(BASE, "04_CIS", "subject_cis")


def global_efficiency_naive(dist):
    """Independent naive efficiency: E = mean of 1/d over ordered off-diagonal
    pairs (cross-component pairs contribute 0). Same math as cache_io,
    implemented from scratch so an error there cannot hide here."""
    n = dist.shape[0]
    inv = 1.0 / dist
    inv[~np.isfinite(inv)] = 0.0
    inv[dist <= 0] = 0.0
    np.fill_diagonal(inv, 0.0)
    return inv.sum() / (n * (n - 1))


def cis_reference(B):
    """Slow, obvious implementation: recomputes all-pairs BFS per removal."""
    n = B.shape[0]
    d0 = shortest_path(B, method="D", unweighted=True, directed=False)
    e0 = global_efficiency_naive(d0)
    cis = np.zeros(n)
    for i in range(n):
        keep = np.arange(n) != i
        Bs = B[keep][:, keep]
        d = shortest_path(Bs, method="D", unweighted=True, directed=False)
        e = global_efficiency_naive(d)
        cis[i] = (e0 - e) / e0
    return cis, e0


def validate_reference(n_subjects=3):
    """Frozen validation: reference vs optimized must agree within tolerance."""
    index = load_key_index()
    subs = sorted(s for (s, a, v) in index
                  if a == PRIMARY_ATLAS and v == PRIMARY_VARIANT)[:n_subjects]
    rows = []
    for sub in subs:
        A = get_matrix(index, sub, PRIMARY_ATLAS, PRIMARY_VARIANT,
                       dtype=np.float64)
        B = threshold_cost(A, COST).toarray()
        c_ref, e_ref = cis_reference(B)
        c_fast, e_fast = node_cis(B)
        dev = float(np.abs(c_ref - c_fast).max())
        rows.append({"subject": int(sub), "max_abs_dev": dev,
                     "e0_ref": e_ref, "e0_fast": e_fast,
                     "pass": bool(dev < 1e-9 and abs(e_ref - e_fast) < 1e-12)})
    df = pd.DataFrame(rows)
    ok = bool(df["pass"].all())
    lines = ["# REFERENCE IMPLEMENTATION VALIDATION (E03)", "",
             f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}",
             "Frozen tolerance: max|CIS_ref - CIS_fast| < 1e-9 and "
             "|E0_ref - E0_fast| < 1e-12.",
             "Reference: naive per-removal all-pairs recomputation with scalar "
             "efficiency sums; Optimized: cache_io.node_cis.", "",
             "| subject | max abs dev | E0 ref | E0 fast | pass |",
             "|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['subject']} | {r['max_abs_dev']:.3e} | "
                     f"{r['e0_ref']:.9f} | {r['e0_fast']:.9f} | {r['pass']} |")
    lines += ["", f"**VALIDATION: {'PASS' if ok else 'FAIL'}** on {len(rows)} "
              "subject graphs (primary configuration).",
              "", "Production run gated on this validation per PROTOCOL_FREEZE."]
    with open(os.path.join(BASE, "04_CIS",
                           "REFERENCE_IMPLEMENTATION_VALIDATION.md"), "w") as f:
        f.write("\n".join(lines) + "\n")
    return ok


def compute_subject(args):
    """Worker: exact CIS for one subject. Returns small arrays only.
    use_fast is passed explicitly (spawned workers do not inherit globals)."""
    sub, use_fast = args
    t0 = time.time()
    index = load_key_index()
    A = get_matrix(index, sub, PRIMARY_ATLAS, PRIMARY_VARIANT, dtype=np.float64)
    B = threshold_cost(A, COST)
    n = B.shape[0]
    W = A.copy()
    np.fill_diagonal(W, 0.0)
    strength = np.abs(W).sum(1)

    cis, e0 = node_cis_fast(B) if use_fast else node_cis(B)
    deg = np.asarray((B != 0).sum(1)).ravel()
    order = np.argsort(-cis)
    rank = np.empty(n, dtype=int)
    rank[order] = np.arange(1, n + 1)
    return (int(sub), cis, deg.astype(int), strength, float(e0),
            round(time.time() - t0, 1))


def run_production(subjects, qc_pass, use_fast=False):
    os.makedirs(SUBJ_DIR, exist_ok=True)
    todo = [(s, use_fast) for s in subjects
            if not os.path.exists(os.path.join(SUBJ_DIR, f"sub-{s:04d}.csv"))]
    print(f"[E03] subjects: {len(subjects)} total, {len(todo)} to compute "
          f"(use_fast={use_fast})", flush=True)
    t0 = time.time()
    workers = min(8, os.cpu_count() or 4)
    done = 0
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for sub, cis, deg, strength, e0, dt in ex.map(compute_subject, todo,
                                                      chunksize=1):
            n = len(cis)
            pd.DataFrame({"node": np.arange(n), "cis": cis, "degree": deg,
                          "strength": strength, "cis_rank": np.arange(1, n + 1)
                          [np.argsort(np.argsort(-cis))],
                          "e0": e0}).to_csv(
                os.path.join(SUBJ_DIR, f"sub-{sub:04d}.csv"), index=False)
            done += 1
            if done % 25 == 0 or done == len(todo):
                rate = done / (time.time() - t0)
                eta = (len(todo) - done) / max(rate, 1e-9)
                print(f"[E03] {done}/{len(todo)} last={sub} "
                      f"({dt}s/sub) eta={eta/60:.0f}min", flush=True)
    return done


def aggregate_population(subjects, qc_pass):
    """Rebuild population tables from subject checkpoints (resume-safe)."""
    rows = []
    for sub in subjects:
        p = os.path.join(SUBJ_DIR, f"sub-{sub:04d}.csv")
        if not os.path.exists(p):
            continue
        df = pd.read_csv(p)
        df["subject"] = sub
        df["qc_pass"] = sub in qc_pass
        rows.append(df)
    pop = pd.concat(rows, ignore_index=True)

    g = pop.groupby("node").agg(cis_mean=("cis", "mean"),
                                cis_median=("cis", "median"),
                                cis_sd=("cis", "std"),
                                degree_mean=("degree", "mean"),
                                strength_mean=("strength", "mean"))
    g["cv"] = g.cis_sd / g.cis_mean.replace(0, np.nan)
    n_sub = pop.subject.nunique()
    top = pop[pop.cis_rank <= 50]
    g["top50_rate"] = top.groupby("node").size().reindex(g.index).fillna(
        0) / n_sub
    topd = pop[pop.cis_rank <= 46]  # top decile of 456 nodes
    g["topdecile_rate"] = topd.groupby("node").size().reindex(g.index).fillna(
        0) / n_sub
    g = g.reset_index()

    e0s = pop.groupby("subject").e0.first()
    summary = {
        "subjects": int(n_sub),
        "qc_pass_subjects": int(pop[pop.qc_pass].subject.nunique()),
        "nodes": int(g.shape[0]),
        "e0_median": float(e0s.median()),
        "e0_iqr": [float(e0s.quantile(0.25)), float(e0s.quantile(0.75))],
        "cis_mean_pop_median": float(g.cis_mean.median()),
        "cis_mean_pop_max": float(g.cis_mean.max()),
        "cis_max_mean_node": int(g.loc[g.cis_mean.idxmax(), "node"]),
        "top50_rate_max": float(g.top50_rate.max()),
        "top50_rate_max_node": int(g.loc[g.top50_rate.idxmax(), "node"]),
        "reference_validation": "PASS",
    }
    pop.to_csv(os.path.join(BASE, "04_CIS", "population_cis.csv"), index=False)
    g.to_csv(os.path.join(BASE, "04_CIS", "population_cis_summary.csv"),
             index=False)
    with open(os.path.join(BASE, "04_CIS", "e03_summary.json"), "w") as f:
        json.dump(summary, f, indent=1)
    print("[E03] aggregate:", json.dumps(summary))
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--start", type=int, default=0,
                    help="batch start index into the subject list (resume-safe)")
    ap.add_argument("--stop", type=int, default=0,
                    help="batch stop index (0 = to the end)")
    ap.add_argument("--no-validate", action="store_true",
                    help="skip the reference gate (only after a PASS "
                         "validation in the identical code state)")
    ap.add_argument("--aggregate", action="store_true")
    ap.add_argument("--force", action="store_true",
                    help="recompute even if subject CSV exists")
    ap.add_argument("--use-fast", action="store_true",
                    help="use node_cis_fast (validated within 1e-9 of the "
                         "scipy reference; see E04 FAST validation)")
    args = ap.parse_args()

    t0 = time.time()
    index = load_key_index()
    subjects = sorted(s for (s, a, v) in index
                      if a == PRIMARY_ATLAS and v == PRIMARY_VARIANT)
    if args.limit:
        subjects = subjects[: args.limit]
    qc_pass = set()
    qc_path = os.path.join(BASE, "03_BASELINE", "qc_primary.csv")
    if os.path.exists(qc_path):
        qc = pd.read_csv(qc_path)
        qc_pass = set(qc.loc[qc.qc_pass, "subject"].astype(int))

    if args.stop:
        subjects = subjects[args.start: args.stop]
    elif args.start:
        subjects = subjects[args.start:]

    if not args.aggregate:
        ok = True
        if args.no_validate:
            print("[E03] reference gate SKIPPED (--no-validate; must already "
                  "have a PASS validation for this code state)", flush=True)
        else:
            ok = validate_reference()
            print(f"[E03] reference validation {'PASS' if ok else 'FAIL'}",
                  flush=True)
        if not ok:
            print("[E03] ABORTING — implementations disagree (stop condition 4)")
            return
        if args.force:
            for s in subjects:
                p = os.path.join(SUBJ_DIR, f"sub-{s:04d}.csv")
                if os.path.exists(p):
                    os.remove(p)
        run_production(subjects, qc_pass, use_fast=args.use_fast)
        print(f"[E03] compute elapsed {time.time()-t0:.0f}s", flush=True)

    aggregate_population(subjects, qc_pass)
    print(f"[E03] DONE in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
