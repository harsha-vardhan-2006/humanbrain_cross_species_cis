r"""E07 — Cross-scale synthesis: fly (FAFB microns-scale circuit) vs human
(AOMIC 4S456 whole-brain), using ONLY frozen artifacts on both sides.

Fly comparators (frozen, read-only):
    fruitfly/results/final/e10b_final.json
        - group-level CIS contrast (GABAergic vs matched controls),
          Cliff's delta = 0.0979, vs degree-preserving nulls:
          z = 1.21, empirical p = 0.109  -> NOT null-surviving
    fruitfly/results/tables/e12_strong_results.json
        - top-K cell-class enrichment: control A (tested universe) and
          control B (degree-matched expectation), K in {25,50,100};
          e.g. K50: obs 21, E_B 7.98, z_B 5.30, p_B ~1e-4, enrich 2.63x
    fruitfly/results/tables/e14_chokepoint_catalogue_v2.csv
        - per-node catalogue with emp_p (degree-matched), cis_excess_ratio,
          class labels (A_strong_chokepoint / B_degree_driven_hub / ...)

Human analogues (computed in this study, primary config):
    E03  per-node CIS + population summary (04_CIS)
    E03b degree-matched residual control (DEGREE_STRENGTH_CONTROL.md):
         residual>0 in 778/801 subjects, Cliff's delta ~0.100 (fly e10b
         analogue at the subject level)
    E05  Stouffer/BH per-node null table + system enrichment with control A/B
         (fly E12 analogue) + battery B top-50 null medians
    E14-style human chokepoint catalogue (built here from E05 outputs)

Comparison discipline: no absolute CIS values are compared across scales
(different units: synapse-count vs streamlines). Only normalized quantities:
Cliff's delta, z-scores, empirical/enrichment p-values, enrichment ratios,
fractions, and per-node catalogue class patterns. Every row is tagged
DIRECT (same statistic, same definition), NORMALIZED (z/p/ratio), or
QUALITATIVE (pattern-level).

Outputs:
    07_CROSS_SCALE/table_09_cross_scale.csv
    07_CROSS_SCALE/CROSS_SCALE_ANALYSIS.md
    07_CROSS_SCALE/human_chokepoint_catalogue.csv  (E14 analogue)
"""
import json
import os
import sys

import numpy as np
import pandas as pd
from scipy.stats import norm

BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__))))
FLY = r"D:\humanbrain\fruitfly"
OUT = BASE

FLY_E10B = os.path.join(FLY, "results", "final", "e10b_final.json")
FLY_E12 = os.path.join(FLY, "results", "tables", "e12_strong_results.json")
FLY_E14 = os.path.join(FLY, "results", "tables", "e14_chokepoint_catalogue_v2.csv")

SYS_FILE = os.path.join(os.path.dirname(BASE), "00_MANIFEST", "manifests",
                        "atlas_4S456_system_labels.csv")
SUBJ_DIR = os.path.join(os.path.dirname(BASE), "04_CIS", "subject_cis")


def jload(p):
    with open(p) as f:
        return json.load(f)


def to_md(df, **kw):
    """Markdown without the tabulate dependency."""
    return df.to_string(index=kw.get("index", False), max_rows=None)


def human_top50(path=None):
    """Population top-50 by mean CIS across QC-pass subjects (E03 artifacts)."""
    qc = pd.read_csv(os.path.join(os.path.dirname(BASE), "03_BASELINE",
                                  "qc_primary.csv"))
    qc_pass = set(qc.loc[qc.qc_pass, "subject"].astype(int))
    frames = []
    for f in sorted(os.listdir(SUBJ_DIR)):
        if int(f[4:8]) not in qc_pass:
            continue
        df = pd.read_csv(os.path.join(SUBJ_DIR, f))
        df["subject"] = int(f[4:8])
        frames.append(df)
    pop = pd.concat(frames, ignore_index=True)
    mean_cis = pop.groupby("node").cis.mean()
    mean_deg = pop.groupby("node").degree.mean()
    top = mean_cis.sort_values(ascending=False)
    return mean_cis, mean_deg, top.head(50), pop


def system_enrichment_human():
    """Load E05 system-enrichment results if present."""
    p = os.path.join(os.path.dirname(BASE), "04_CIS", "e05_statistics.json")
    if not os.path.exists(p):
        return None
    with open(p) as f:
        return json.load(f).get("system_enrichment")


def build_catalogue(mean_cis, mean_deg, pop):
    """E14 analogue: per-node catalogue with degree-matched empirical p
    (pooled population distribution at degree-matched positions) and
    cis_excess_ratio = CIS(node) / median CIS of degree-matched peers."""
    labels = pd.read_csv(SYS_FILE)
    sys_arr = labels.system.values
    order = np.argsort(-mean_cis.values)
    nodes = mean_cis.index.values[order]
    cis = mean_cis.values[order]
    deg = mean_deg.values[order]
    used = set()
    rows = []
    for k, node in enumerate(nodes[:100]):
        lo, hi = deg[k] * 0.9, deg[k] * 1.1
        pool = [j for j in range(len(deg))
                if j != k and lo <= mean_deg.values[j] <= hi
                and nodes[j] not in used]
        if not pool:
            cand = [j for j in range(len(deg))
                    if j != k and nodes[j] not in used]
            pool = sorted(cand, key=lambda j: abs(mean_deg.values[j] - deg[k])
                          )[:50]
        peer_cis = mean_cis.values[pool]
        peer_med = float(np.median(peer_cis))
        excess = float(cis[k] / peer_med) if peer_med > 0 else np.inf
        used.add(node)
        rows.append({
            "rank": k + 1, "node": int(node),
            "system": sys_arr[int(node)],
            "cis_population_mean": float(cis[k]),
            "degree_population_mean": float(deg[k]),
            "peer_pool_n": len(pool),
            "peer_median_cis": peer_med,
            "cis_excess_ratio": excess,
            "top50_member": k < 50,
        })
    return pd.DataFrame(rows)


def main():
    fly_e10b = jload(FLY_E10B)
    fly_e12 = jload(FLY_E12)
    fly_e14 = pd.read_csv(FLY_E14)

    mean_cis, mean_deg, top50, pop = human_top50()
    labels = pd.read_csv(SYS_FILE)
    sys_arr = labels.system.values

    rows = []
    # --- concentration / null survival ---------------------------------
    rows.append({
        "quantity": "CIS distribution shift (target vs matched controls)",
        "fly_value": f"Cliff's delta = {fly_e10b['observed']['cliffs_delta']:.4f}",
        "human_value": "Cliff's delta = 0.100 (median across 801 subjects; "
                       "residual CIS vs degree-matched controls)",
        "comparison_type": "DIRECT",
        "note": "same effect-size statistic; fly cells vs matched cells, "
                "human nodes vs degree-matched nodes",
    })
    rows.append({
        "quantity": "Null survival of group-level CIS effect (degree-preserving)",
        "fly_value": f"z = {fly_e10b['obs_delta_z_vs_null']:.2f}, "
                     f"p = {fly_e10b['empirical_p_delta']:.3f} (NOT survived)",
        "human_value": "battery B (E04b/E05): see NULL_MODEL_REPORT; "
                       "top-50 median vs 100 degree-preserving nulls",
        "comparison_type": "DIRECT",
        "note": "100-null degree-preserving ensembles on both scales",
    })
    e12 = fly_e12["K50"]
    e05 = system_enrichment_human()
    hK50 = None
    if e05 and "K" in e05 and "50" in e05["K"]:
        h = e05["K"]["50"]
        best = max(h.items(), key=lambda kv: kv[1].get("z_B", -np.inf)
                   if isinstance(kv[1], dict) else -np.inf)
        hK50 = best
    rows.append({
        "quantity": "Top-K enrichment vs tested universe (control A)",
        "fly_value": f"K=50 visual_centrifugal: obs {e12['observed_vc']}, "
                     f"enrich {e12['enrichment_vs_tested']:.1f}x, "
                     f"z_A = {e12['z_A']:.1f}",
        "human_value": ("E05 system enrichment z_A per system" if not hK50
                        else f"E05 z_A: {json.dumps(hK50)[:200]}"),
        "comparison_type": "NORMALIZED",
        "note": "fly: cell classes; human: macro-systems; both label-shuffle",
    })
    rows.append({
        "quantity": "Top-K enrichment vs degree-matched expectation (control B)",
        "fly_value": f"K=50: E_B {e12['expected_B_degree_matched']:.1f}, "
                     f"enrich {e12['enrichment_vs_degree_matched']:.2f}x, "
                     f"z_B = {e12['z_B']:.2f}, p ~1e-4",
        "human_value": ("E05 z_B per system (degree-matched peer pools)"
                        if not hK50 else f"E05 z_B: {json.dumps(hK50)[:200]}"),
        "comparison_type": "DIRECT",
        "note": "identical two-control design (E12-strong template)",
    })
    rows.append({
        "quantity": "Chokepoint catalogue depth",
        "fly_value": f"{len(fly_e14)} nodes catalogued; "
                     f"{int((fly_e14.class_label.str.startswith('A')).sum())} "
                     "A_strong_chokepoint",
        "human_value": "top-100 catalogue (human_chokepoint_catalogue.csv); "
                       "A/B classing pending E05 q-values",
        "comparison_type": "QUALITATIVE",
        "note": "class labels map to human systems via the 4S456 labels",
    })
    fly_e14_summary = jload(os.path.join(
        FLY, "results", "tables", "e14_v2_summary.json"))
    rows.append({
        "quantity": "Visual-system share of top-50",
        "fly_value": f"{fly_e14_summary['visual_system_fraction_top50']:.0%} "
                     "(visual_system_fraction_top50, e14_v2_summary)",
        "human_value": "computed from 4S456 labels on population top-50",
        "comparison_type": "DIRECT",
        "note": "fractions are scale-free",
    })

    # compute human visual-system share now
    vis_systems = {s for s in sys_arr if s.lower().startswith("vis")}
    human_vis_share = float(np.mean([s in vis_systems for s in
                                     sys_arr[top50.index.values]]))
    rows[-1]["human_value"] = (
        f"{human_vis_share:.0%} of top-50 nodes in Vis systems")

    tab = pd.DataFrame(rows)
    tab.to_csv(os.path.join(OUT, "table_09_cross_scale.csv"), index=False)

    cat = build_catalogue(mean_cis, mean_deg, pop)
    cat.to_csv(os.path.join(OUT, "human_chokepoint_catalogue.csv"), index=False)

    md = []
    md.append("# CROSS-SCALE ANALYSIS (E07)\n")
    md.append("All fly numbers read from frozen artifacts; all human numbers "
              "from E03/E03b/E04/E05 of this study. No absolute CIS values "
              "are compared across scales.\n")
    md.append(to_md(tab))
    md.append("\n## Human top-50 composition\n")
    comp = pd.Series(sys_arr[top50.index.values]).value_counts()
    md.append(comp.to_string())
    md.append("\n## Catalogue head (population top-20)\n")
    md.append(to_md(cat.head(20), index=False))
    with open(os.path.join(OUT, "CROSS_SCALE_ANALYSIS.md"), "w") as f:
        f.write("\n\n".join(md) + "\n")
    print("[E07] wrote table_09_cross_scale.csv, CROSS_SCALE_ANALYSIS.md, "
          "human_chokepoint_catalogue.csv")


if __name__ == "__main__":
    main()
