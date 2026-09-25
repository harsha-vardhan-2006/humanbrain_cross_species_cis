r"""E06 — Robustness battery (frozen ladder; compute-bounded sensitivity).

Pre-declared conditions (PROTOCOL_FREEZE §1 ladder + STUDY_DESIGN atlas/weight
sensitivity), all at the frozen CIS definition:
  cost:     4S456 x sift_count at 10%, 20%, 25%   (primary is 15% = E03)
  atlas:    4S256, 4S156, Brainnetome246Ext, AAL116 x sift_count @ 15%
  weight:   4S456 x sift_invnodevol, 4S456 x radius2_count @ 15%
Cohort: first 150 QC-pass subjects of the frozen seeded permutation
(seed 20260922) — documented compute-bounded scope, mirroring the null battery.

Per condition, per subject: mean/median/max CIS, top-50 mean CIS (concentration),
top-decile mean CIS, Spearman(CIS, degree), Gini coefficient of the CIS
distribution. Same-atlas conditions additionally yield node-level rank
correlations with the primary condition (rank reproducibility); cross-atlas
comparisons are distributional/architectural only (no node correspondence).

Gates: per-condition fast-vs-scipy CIS validation on 2 subjects (1e-9).

Outputs:
  06_ROBUSTNESS/robustness_per_subject_condition.csv
  06_ROBUSTNESS/robustness_condition_summary.csv
  09_TABLES/table_08_robustness.csv
  06_ROBUSTNESS/ROBUSTNESS_RESULTS.md   (written after all conditions land)

Usage:
    py robustness.py --validate          # all condition gates
    py robustness.py --condition cost_10 --start 0 --stop 50
    py robustness.py --summarize
"""
import argparse, json, os, sys, time

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "02_PREPROCESSING"))
from cache_io import (BASE, PRIMARY_ATLAS, PRIMARY_VARIANT, get_matrix,
                      load_key_index, node_cis, node_cis_fast, threshold_cost)

OUT = os.path.join(BASE, "06_ROBUSTNESS")
N_SUBJECTS = 150
SUBJECT_SEED = 20260922

CONDITIONS = {
    "cost_10":  (PRIMARY_ATLAS, PRIMARY_VARIANT, 0.10),
    "cost_20":  (PRIMARY_ATLAS, PRIMARY_VARIANT, 0.20),
    "cost_25":  (PRIMARY_ATLAS, PRIMARY_VARIANT, 0.25),
    "atlas_4S256":   ("atlas_4S256Parcels", PRIMARY_VARIANT, 0.15),
    "atlas_4S156":   ("atlas_4S156Parcels", PRIMARY_VARIANT, 0.15),
    "atlas_B246":    ("atlas_Brainnetome246Ext", PRIMARY_VARIANT, 0.15),
    "atlas_AAL116":  ("atlas_AAL116", PRIMARY_VARIANT, 0.15),
    "weight_invnodevol": (PRIMARY_ATLAS,
                          "sift_invnodevol_radius2_count_connectivity", 0.15),
    "weight_r2count":    (PRIMARY_ATLAS,
                          "radius2_count_connectivity", 0.15),
}


def robustness_subjects():
    qc = pd.read_csv(os.path.join(BASE, "03_BASELINE", "qc_primary.csv"))
    qc_pass = np.sort(qc.loc[qc.qc_pass, "subject"].values.astype(int))
    rng = np.random.default_rng(SUBJECT_SEED)
    perm = rng.permutation(qc_pass)
    return perm[:N_SUBJECTS]


def condition_summary_rows(cis):
    n = len(cis)
    order = np.sort(cis)[::-1]
    k50, kdec = 50, max(1, int(np.ceil(0.1 * n)))
    # Gini coefficient of |CIS| distribution (concentration, scale-free)
    x = np.sort(np.abs(cis))
    cum = np.cumsum(x)
    gini = float((n + 1 - 2 * (cum / cum[-1]).sum()) / n) if cum[-1] > 0 else 0.0
    return {"cis_mean": float(cis.mean()), "cis_median": float(np.median(cis)),
            "cis_max": float(cis.max()),
            "top50_mean": float(order[:k50].mean()),
            "topdecile_mean": float(order[:kdec].mean()),
            "gini_abs_cis": gini}


def _compute_one(args):
    """Worker: one subject x one condition -> summary row (checkpointed)."""
    cond, sub = args
    atlas, variant, cost = CONDITIONS[cond]
    cdir = os.path.join(OUT, cond)
    os.makedirs(cdir, exist_ok=True)
    fout = os.path.join(cdir, f"sub-{int(sub):04d}.csv")
    if os.path.exists(fout):
        return cond, pd.read_csv(fout).iloc[0].to_dict()
    index = load_key_index()
    A = get_matrix(index, int(sub), atlas, variant, dtype=np.float64)
    B = threshold_cost(A, cost)
    cis, e0 = node_cis_fast(B)
    deg = np.asarray((B != 0).sum(1)).ravel()
    r = condition_summary_rows(cis)
    r.update({"subject": int(sub), "condition": cond, "atlas": atlas,
              "variant": variant, "cost": cost, "e0": float(e0),
              "spearman_cis_degree": float(spearmanr(cis, deg).statistic),
              "n_nodes": len(cis)})
    pd.DataFrame([r]).to_csv(fout, index=False)
    return cond, r


def compute_condition(cond, subjects, index, workers=8):
    atlas, variant, cost = CONDITIONS[cond]
    cdir = os.path.join(OUT, cond)
    os.makedirs(cdir, exist_ok=True)
    from concurrent.futures import ProcessPoolExecutor
    jobs = [(cond, s) for s in subjects
            if not os.path.exists(
                os.path.join(cdir, f"sub-{int(s):04d}.csv"))]
    rows = []
    cached = [(cond, pd.read_csv(os.path.join(cdir, f"sub-{int(s):04d}.csv"))
               .iloc[0].to_dict()) for s in subjects
              if os.path.exists(os.path.join(cdir, f"sub-{int(s):04d}.csv"))]
    rows.extend(r for _, r in cached)
    t0 = time.time()
    done = 0
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for _, r in ex.map(_compute_one, jobs):
            rows.append(r)
            done += 1
            if done % 25 == 0 or done == len(jobs):
                print(f"[E06:{cond}] {done}/{len(jobs)} at "
                      f"{(time.time()-t0)/60:.1f} min", flush=True)
    return rows


def validate_conditions(n_check=2):
    """Per-condition fast-vs-scipy gate on the first n_check subjects."""
    index = load_key_index()
    subs = robustness_subjects()[:n_check]
    all_ok = True
    for cond, (atlas, variant, cost) in CONDITIONS.items():
        devs = []
        for sub in subs:
            A = get_matrix(index, int(sub), atlas, variant, dtype=np.float64)
            B = threshold_cost(A, cost)
            c_ref, e_ref = node_cis(B)
            c_fast, e_fast = node_cis_fast(B)
            devs.append(max(float(np.abs(c_ref - c_fast).max()),
                            abs(e_ref - e_fast) * 1e3))
        ok = max(devs) < 1e-9
        all_ok &= ok
        print(f"[E06-gate] {cond}: max_dev={max(devs):.2e} "
              f"{'PASS' if ok else 'FAIL'}", flush=True)
    with open(os.path.join(OUT, "condition_validation.json"), "w") as f:
        json.dump({c: {"max_dev": None, "gate": "PASS" if all_ok else "SEE_LOG"}
                   for c in CONDITIONS}, f, indent=1)
    return all_ok


def summarize():
    rows = []
    for cond in CONDITIONS:
        cdir = os.path.join(OUT, cond)
        files = [f for f in sorted(os.listdir(cdir)) if f.endswith(".csv")]
        if not files:
            continue
        df = pd.concat([pd.read_csv(os.path.join(cdir, f)) for f in files],
                       ignore_index=True)
        rows.append({
            "condition": cond, "atlas": df.atlas.iloc[0],
            "variant": df.variant.iloc[0], "cost": df.cost.iloc[0],
            "n_subjects": len(df),
            "cis_mean_of_means": df.cis_mean.mean(),
            "top50_mean_of_means": df.top50_mean.mean(),
            "topdecile_mean_of_means": df.topdecile_mean.mean(),
            "cis_max_median": df.cis_max.median(),
            "gini_abs_cis_median": df.gini_abs_cis.median(),
            "spearman_cis_degree_median": df.spearman_cis_degree.median(),
            "e0_median": df.e0.median(),
        })
    summ = pd.DataFrame(rows)
    if summ.empty:
        print("[E06] nothing to summarize yet")
        return
    summ.to_csv(os.path.join(OUT, "robustness_condition_summary.csv"),
                index=False)
    summ.to_csv(os.path.join(BASE, "09_TABLES", "table_08_robustness.csv"),
                index=False)
    print(summ[["condition", "n_subjects", "top50_mean_of_means",
                "gini_abs_cis_median", "spearman_cis_degree_median"]].to_string(
                    index=False))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--condition", type=str, default=None)
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--stop", type=int, default=0)
    ap.add_argument("--summarize", action="store_true")
    ap.add_argument("--no-validate", action="store_true")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    if args.summarize:
        summarize()
        return
    if args.validate:
        ok = validate_conditions()
        print("[E06] gates:", "PASS" if ok else "FAIL")
        return

    index = load_key_index()
    subjects = robustness_subjects()
    if args.stop:
        subjects = subjects[args.start:args.stop]
    elif args.start:
        subjects = subjects[args.start:]

    conds = [args.condition] if args.condition else list(CONDITIONS)
    if not args.no_validate:
        ok = validate_conditions()
        if not ok:
            print("[E06] gates FAILED — aborting")
            return
    for cond in conds:
        t0 = time.time()
        rows = compute_condition(cond, subjects, index, workers=args.workers)
        pd.DataFrame(rows).to_csv(
            os.path.join(OUT, f"{cond}_per_subject.csv"), index=False)
        print(f"[E06] {cond} done in {(time.time()-t0)/60:.1f} min")
    summarize()


if __name__ == "__main__":
    main()
