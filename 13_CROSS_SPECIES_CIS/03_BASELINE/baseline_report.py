r"""Generate 03_BASELINE/BASELINE_RESULTS.md from baseline_network_properties.csv
and qc_primary.csv (reproducible: regenerates the md from frozen artifacts)."""
import os

import numpy as np
import pandas as pd

BASE = r"D:\humanbrain\humanbrain\13_CROSS_SPECIES_CIS"
PRIMARY_ATLAS = "atlas_4S456Parcels"
PRIMARY_VARIANT = "sift_radius2_count_connectivity"

b = pd.read_csv(os.path.join(BASE, "03_BASELINE",
                             "baseline_network_properties.csv"))
qc = pd.read_csv(os.path.join(BASE, "03_BASELINE", "qc_primary.csv"))
summ = b[b.cost == 0.15].groupby("atlas").agg(
    ge_median=("ge", "median"), ge_iqr_lo=("ge", lambda x: x.quantile(0.25)),
    ge_iqr_hi=("ge", lambda x: x.quantile(0.75)),
    mean_degree=("mean_degree", "mean"), edges_median=("edges", "median"),
    giant_frac_median=("giant_frac", "median"))

p = b[(b.atlas == PRIMARY_ATLAS) & (b.cost == 0.15)]
flag_counts = {c: int(qc[c].sum()) for c in qc.columns if c.startswith("flag_")}

lines = [
    "# BASELINE RESULTS (E02) — intact networks before perturbation",
    "",
    "Configuration: sift_radius2_count (PRIMARY weight), proportional cost",
    "threshold, ladder {10, 15, 20, 25}%; binary undirected graphs;",
    "efficiency on unweighted shortest paths (PROTOCOL_FREEZE §2).",
    "Cohort: 900 subjects × 7 atlases (25,200 thresholded graphs).",
    "",
    "## 1. Primary configuration (4S456 × sift count × 15% cost)",
    "",
    f"- Global efficiency: median {p['ge'].median():.4f}, "
    f"IQR [{p['ge'].quantile(0.25):.4f}, {p['ge'].quantile(0.75):.4f}]",
    f"- Mean degree: mean {p['mean_degree'].mean():.1f} "
    f"(SD {p['mean_degree'].std():.1f}); edges median {int(p['edges'].median())}",
    f"- Giant component: median fraction {p['giant_frac'].median():.4f} "
    f"(graphs with giant_frac<1: {(p.giant_frac < 1).sum()}/900)",
    "",
    "## 2. Atlas × cost structure",
    "",
    "| atlas | GE median @15% | GE IQR | mean degree | edges med | giant med |",
    "|---|---|---|---|---|---|",
]
for atlas, r in summ.iterrows():
    lines.append(f"| {atlas} | {r.ge_median:.4f} | "
                 f"[{r.ge_iqr_lo:.4f}, {r.ge_iqr_hi:.4f}] | "
                 f"{r.mean_degree:.1f} | {int(r.edges_median)} | "
                 f"{r.giant_frac_median:.4f} |")
lines += [
    "",
    "### Cost ladder (4S456, GE median)",
    "",
    "| cost | 10% | 15% | 20% | 25% |",
    "|---|---|---|---|---|",
]
ladder = b[b.atlas == PRIMARY_ATLAS].groupby("cost")["ge"].median()
lines.append("| GE | " + " | ".join(f"{ladder[c]:.4f}" for c in
                                    [0.10, 0.15, 0.20, 0.25]) + " |")
lines += [
    "",
    "## 3. QC gate (CIS-blind, PROTOCOL_FREEZE §5)",
    "",
    f"- QC PASS: {int(qc.qc_pass.sum())}/900 subjects "
    f"(flagged: {int((~qc.qc_pass).sum())})",
    "- Flag counts: " + ", ".join(f"{k}={v}" for k, v in flag_counts.items()),
    "- Flags are recorded, never deletions; QC-pass cohort is used for the",
    "  primary analysis, and sensitivity analyses report both cohorts.",
    "",
    "## 4. Notes",
    "",
    "- All 25,200 raw matrices passed structural QC (0 NaN/Inf, 0 dim",
    "  mismatches, 0 asymmetry > 1e-9, 0 negative off-diagonals) — see",
    "  01_RAW_PROBES/raw_flags.json.",
    "- Post-threshold isolated nodes (94 subjects) are the dominant flag:",
    "  expected at 15% cost in sparse parcellations; CIS(i)=0 is forced for",
    "  isolated i by definition, and these subjects remain in the QC-pass",
    "  cohort unless the frozen >1-multi-node-component rule triggers",
    "  (0 subjects).",
    "",
    "Reproducible via: py 03_BASELINE/baseline_report.py",
]
with open(os.path.join(BASE, "03_BASELINE", "BASELINE_RESULTS.md"), "w",
          encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print("BASELINE_RESULTS.md written")
