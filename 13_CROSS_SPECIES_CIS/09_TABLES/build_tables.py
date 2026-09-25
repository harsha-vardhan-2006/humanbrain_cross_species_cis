r"""Build machine-readable tables (01-05, 07, 10) for 09_TABLES from
frozen study artifacts. Tables 06 (degree control) and 08 (robustness)
and 09 (cross-scale) are written by their own phases.

    table_01_subject_cohort      cohort accounting (E01/E02)
    table_02_baseline_network    network properties per atlas (E02)
    table_03_qc_summary          QC gates and pass rates (E02)
    table_04_population_cis      per-node population CIS summary (E03)
    table_05_top_stability       top-node stability stats (E03)
    table_07_null_results        per-node null stats (E05; placeholder here)
    table_10_decision_summary    primary outcome snapshot (E03/E03b)
"""
import json
import os
import sys

import numpy as np
import pandas as pd

BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    ".."))
T = os.path.join(BASE, "09_TABLES")
os.makedirs(T, exist_ok=True)


def t01_cohort():
    qc = pd.read_csv(os.path.join(BASE, "03_BASELINE", "qc_primary.csv"))
    idx = pd.read_csv(os.path.join(BASE, "02_PREPROCESSING", "cache_keys.csv"))
    subs = idx[idx.atlas == "atlas_4S456Parcels"].subject.nunique()
    rows = [{"atlas": "atlas_4S456Parcels", "n_subjects_cached": subs,
             "n_qc_pass": int(qc.qc_pass.sum()),
             "n_qc_fail": int((~qc.qc_pass).sum()),
             "qc_pass_rate": float(qc.qc_pass.mean())}]
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(T, "table_01_subject_cohort.csv"), index=False)
    return df


def t02_baseline():
    src = os.path.join(BASE, "03_BASELINE", "baseline_network_properties.csv")
    df = pd.read_csv(src)
    df.to_csv(os.path.join(T, "table_02_baseline_network.csv"), index=False)
    return df


def t03_qc():
    qc = pd.read_csv(os.path.join(BASE, "03_BASELINE", "qc_primary.csv"))
    rows = []
    for c in qc.columns:
        if c in ("subject", "qc_pass"):
            continue
        if qc[c].dtype.kind not in "ifb":
            continue
        rows.append({"metric": c,
                     "mean": float(pd.to_numeric(qc[c], errors="coerce").mean()),
                     "median": float(pd.to_numeric(qc[c], errors="coerce").median())})
    n_pass = int(qc.qc_pass.sum())
    rows.append({"metric": "n_qc_pass", "mean": n_pass, "median": n_pass})
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(T, "table_03_qc_summary.csv"), index=False)
    return df


def t04_population():
    src = os.path.join(BASE, "04_CIS", "population_cis_summary.csv")
    df = pd.read_csv(src)
    df.to_csv(os.path.join(T, "table_04_population_cis.csv"), index=False)
    return df


def t05_stability():
    g = pd.read_csv(os.path.join(BASE, "04_CIS", "population_cis_summary.csv"))
    top = g.sort_values("top50_rate", ascending=False).head(20).copy()
    top.insert(0, "stability_rank", np.arange(1, len(top) + 1))
    top.to_csv(os.path.join(T, "table_05_top_stability.csv"), index=False)
    return top


def t07_placeholder():
    p = os.path.join(T, "table_07_null_results.csv")
    if not os.path.exists(p):
        pd.DataFrame({"node": [], "stouffer_z": [], "p_one_sided": [],
                      "q_bh": [], "subjects_with_nulls": []}).to_csv(
            p, index=False)
        return "placeholder written (E05 will overwrite)"
    return "already written by E05"


def t10_decision():
    e03 = json.load(open(os.path.join(BASE, "04_CIS", "e03_summary.json")))
    e03b = json.load(open(os.path.join(BASE, "04_CIS",
                                       "degree_strength_control_summary.json")))
    rows = [
        {"outcome": "O1: topological chokepoints exist (CIS>0)",
         "value": f"max population-mean CIS = {e03['cis_mean_pop_max']:.4f} "
                  f"(node {e03['cis_max_mean_node']}); "
                  f"top50_rate max = {e03['top50_rate_max']:.2f} "
                  f"(node {e03['top50_rate_max_node']})",
         "status": "SUPPORTED (observed level; null arbiter = E04/E05)"},
        {"outcome": "O2: CIS structure beyond degree",
         "value": f"residual>0 in {e03b['subjects_with_positive_median_residual']}"
                  f"/{e03b['subjects']} subjects (sign p="
                  f"{e03b['sign_test_p_two_sided']:.2e}); Cliff's delta "
                  f"{e03b['cliffs_delta_median']:.3f}",
         "status": "SUPPORTED at fixed topology; null arbiter = E04/E05"},
        {"outcome": "O3: cross-scale architectural match (fly)",
         "value": "fly delta 0.098 vs human 0.100; enrichment designs matched "
                  "(E12 template); see 07_CROSS_SCALE",
         "status": "PENDING E04/E05 integration"},
    ]
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(T, "table_10_decision_summary.csv"), index=False)
    return df


def main():
    msgs = []
    for fn, name in [(t01_cohort, "table_01"), (t02_baseline, "table_02"),
                     (t03_qc, "table_03"), (t04_population, "table_04"),
                     (t05_stability, "table_05"), (t07_placeholder, "table_07"),
                     (t10_decision, "table_10")]:
        try:
            r = fn()
            msgs.append(f"{name}: OK {'' if isinstance(r, str) else r.shape}")
        except Exception as e:  # noqa: BLE001 — report and continue
            msgs.append(f"{name}: FAILED {e}")
    print("\n".join(msgs))


if __name__ == "__main__":
    main()
