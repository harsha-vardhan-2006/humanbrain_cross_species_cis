r"""E03b — Degree/strength-matched control analysis (frozen protocol §3).

For every QC-pass subject (primary configuration): nodes in the top CIS decile
are matched to controls within ±10% total degree, 1:1 greedy (highest-CIS
first), no replacement; nearest-50 fallback flagged. Subject-level matched-pair
statistics; population summary. Degree matching alone is never treated as
sufficient evidence (the decisive arbiter is the E04 null battery).

Outputs:
    04_CIS/degree_strength_control_results.csv
    04_CIS/degree_strength_control_per_subject.csv
    04_CIS/degree_strength_control_summary.json
    09_TABLES/table_06_degree_strength_controls.csv
    04_CIS/DEGREE_STRENGTH_CONTROL.md
"""
import json, os, time

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon, binomtest

BASE = r"D:\humanbrain\humanbrain\13_CROSS_SPECIES_CIS"
SUBJ_DIR = os.path.join(BASE, "04_CIS", "subject_cis")


def cliffs_delta(x, y):
    x, y = np.asarray(x), np.asarray(y)
    gt = (x[:, None] > y[None, :]).sum()
    lt = (x[:, None] < y[None, :]).sum()
    return (gt - lt) / (len(x) * len(y))


def match_controls(cis, deg, top_nodes, rel=0.10, k_nearest=50):
    """1:1 greedy nearest-degree matching without replacement.

    Highest-CIS node matches first; pool = unused nodes within ±10% of the
    node's degree; fallback = 50 nearest-degree unused nodes (flagged).
    """
    used = set()
    pairs = []
    order = top_nodes[np.argsort(-cis[top_nodes])]
    for node in order:
        lo, hi = deg[node] * (1 - rel), deg[node] * (1 + rel)
        pool = [j for j in range(len(deg))
                if j not in used and j != node and lo <= deg[j] <= hi]
        match_type = "pm10"
        if not pool:
            cand = [j for j in range(len(deg))
                    if j not in used and j != node]
            if not cand:
                continue
            pool = sorted(cand, key=lambda j: abs(deg[j] - deg[node])
                          )[:k_nearest]
            match_type = "nearest50"
        ctrl = min(pool, key=lambda j: abs(deg[j] - deg[node]))
        used.add(ctrl)
        pairs.append({"node": node, "control": ctrl, "match_type": match_type,
                      "degree": int(deg[node]),
                      "control_degree": int(deg[ctrl]),
                      "cis": float(cis[node]),
                      "control_cis": float(cis[ctrl]),
                      "residual_cis": float(cis[node] - cis[ctrl])})
    return pairs


def main():
    t0 = time.time()
    qc = pd.read_csv(os.path.join(BASE, "03_BASELINE", "qc_primary.csv"))
    qc_pass = set(qc.loc[qc.qc_pass, "subject"].astype(int))

    all_pairs, per_subject = [], []
    for fname in sorted(os.listdir(SUBJ_DIR)):
        sub = int(fname[4:8])
        if sub not in qc_pass:
            continue
        df = pd.read_csv(os.path.join(SUBJ_DIR, fname))
        cis, deg = df.cis.values, df.degree.values
        top_decile = df[df.cis_rank <= max(
            1, int(np.ceil(0.1 * len(df))))].node.values
        pairs = match_controls(cis, deg, top_decile)
        for p in pairs:
            p["subject"] = sub
        all_pairs.extend(pairs)
        if pairs:
            res = np.array([p["residual_cis"] for p in pairs])
            try:
                w_p = float(wilcoxon([p["cis"] for p in pairs],
                                     [p["control_cis"] for p in pairs]).pvalue)
            except ValueError:
                w_p = float("nan")
            per_subject.append({
                "subject": sub, "n_pairs": len(pairs),
                "residual_median": float(np.median(res)),
                "residual_mean": float(res.mean()),
                "frac_beat_control": float((res > 0).mean()),
                "wilcoxon_p": w_p,
                "cliffs_delta": cliffs_delta([p["cis"] for p in pairs],
                                             [p["control_cis"] for p in pairs])})

    ap_df = pd.DataFrame(all_pairs)
    ap_df.to_csv(os.path.join(BASE, "04_CIS",
                              "degree_strength_control_results.csv"),
                 index=False)
    ps = pd.DataFrame(per_subject)
    ps.to_csv(os.path.join(BASE, "04_CIS",
                           "degree_strength_control_per_subject.csv"),
              index=False)

    n_pos = int((ps.residual_median > 0).sum())
    sign = binomtest(n_pos, len(ps), 0.5)
    summary = {
        "subjects": int(len(ps)),
        "pairs_total": int(len(ap_df)),
        "nearest50_fallback_pairs": int(
            (ap_df.match_type == "nearest50").sum()),
        "residual_median_across_subjects": float(ps.residual_median.median()),
        "residual_iqr_across_subjects": [
            float(ps.residual_median.quantile(0.25)),
            float(ps.residual_median.quantile(0.75))],
        "subjects_with_positive_median_residual": n_pos,
        "sign_test_p_two_sided": float(sign.pvalue),
        "mean_frac_beat_control": float(ps.frac_beat_control.mean()),
        "cliffs_delta_median": float(ps.cliffs_delta.median()),
        "cliffs_delta_iqr": [float(ps.cliffs_delta.quantile(0.25)),
                             float(ps.cliffs_delta.quantile(0.75))],
        "wilcoxon_p_median": float(ps.wilcoxon_p.median()),
        "subjects_wilcoxon_p_lt_05": int((ps.wilcoxon_p < 0.05).sum()),
        "elapsed_s": round(time.time() - t0, 1),
    }
    with open(os.path.join(BASE, "04_CIS",
                           "degree_strength_control_summary.json"), "w") as f:
        json.dump(summary, f, indent=1)
    ap_df.head(20000).to_csv(
        os.path.join(BASE, "09_TABLES", "table_06_degree_strength_controls.csv"),
        index=False)

    lines = [
        "# DEGREE/STRENGTH CONTROL (E03b) — frozen protocol §3",
        "",
        f"Cohort: {summary['subjects']} QC-pass subjects; "
        f"{summary['pairs_total']} matched pairs "
        f"(top CIS decile per subject; ±10% degree, 1:1 greedy; "
        f"{summary['nearest50_fallback_pairs']} nearest-50 fallback rows).",
        "",
        "| quantity | value |",
        "|---|---|",
        f"| residual CIS (obs − control), median across subjects | "
        f"{summary['residual_median_across_subjects']:.2e} |",
        f"| residual IQR | "
        f"[{summary['residual_iqr_across_subjects'][0]:.2e}, "
        f"{summary['residual_iqr_across_subjects'][1]:.2e}] |",
        f"| subjects with positive median residual | "
        f"{n_pos}/{summary['subjects']} "
        f"(sign test p={summary['sign_test_p_two_sided']:.3g}) |",
        f"| mean fraction of pairs beating control | "
        f"{summary['mean_frac_beat_control']:.3f} |",
        f"| Cliff's δ (median across subjects) | "
        f"{summary['cliffs_delta_median']:.3f} |",
        f"| subjects with Wilcoxon p<0.05 | "
        f"{summary['subjects_wilcoxon_p_lt_05']}/{summary['subjects']} |",
        "",
        "Interpretation rule (frozen): degree matching is a necessary but not",
        "sufficient control — the decisive arbiter is the degree-preserving",
        "null battery (E04/E05). Positive residuals indicate CIS structure",
        "beyond degree at FIXED topology; the null battery tests structure",
        "beyond degree at RANDOMIZED topology.",
        "",
        "Reproducible via: py 04_CIS/degree_control.py",
    ]
    with open(os.path.join(BASE, "04_CIS", "DEGREE_STRENGTH_CONTROL.md"),
              "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("[E03b] DONE", json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
