"""FIGURE 5 — Anatomical distribution of FDR-surviving nodes (paper Fig. 5).

Typesetting-time render promised in FIGURE_PROVENANCE.md. Uses ONLY frozen
artifacts (table_07_null_results.csv + atlas_4S456_system_labels.csv);
no statistics are recomputed. Output: 08_FIGURES/fig05_fdr_anatomical.{png,pdf}.

Note on numbering: the existing fig05_degree_controlled.* file maps to paper
Fig. 4 (see FIGURE_PROVENANCE.md). This render takes the paper-Fig. 5 slot
and is named fig05_fdr_anatomical.* to avoid overwriting any frozen file.
"""
import csv
import os
from collections import Counter

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
T7 = os.path.join(BASE, "09_TABLES", "table_07_null_results.csv")
LABELS = os.path.join(BASE, "00_MANIFEST", "manifests", "atlas_4S456_system_labels.csv")
OUT_PNG = os.path.join(BASE, "08_FIGURES", "fig05_fdr_anatomical.png")
OUT_PDF = os.path.join(BASE, "08_FIGURES", "fig05_fdr_anatomical.pdf")

# --- read frozen artifacts (read-only) -------------------------------------
with open(LABELS, newline="", encoding="utf-8-sig") as f:
    sys_of = {int(r["node"]): r["system"] for r in csv.DictReader(f)}
with open(T7, newline="", encoding="utf-8-sig") as f:
    survivors = [
        (int(r["node"]), float(r["stouffer_z"]))
        for r in csv.DictReader(f)
        if float(r["q_bh"]) < 0.05
    ]

assert len(survivors) == 43, f"expected 43 FDR survivors, got {len(survivors)}"
counts = Counter(sys_of[n] for n, _ in survivors)
order = [s for s, _ in counts.most_common()]
values = [counts[s] for s in order]

# --- render ----------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.2, 4.2))
bars = ax.bar(range(len(order)), values, color="#4C72B0", edgecolor="black", linewidth=0.6)
ax.set_xticks(range(len(order)))
ax.set_xticklabels(order, rotation=45, ha="right", fontsize=9)
ax.set_ylabel("FDR-surviving nodes (q < 0.05)")
ax.set_title("Anatomical distribution of the 43 FDR-surviving nodes (4S456)", fontsize=11)
for rect, v in zip(bars, values):
    ax.text(rect.get_x() + rect.get_width() / 2, v + 0.2, str(v), ha="center", fontsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.set_ylim(0, max(values) * 1.15)
fig.tight_layout()
fig.savefig(OUT_PNG, dpi=300)
fig.savefig(OUT_PDF)
plt.close(fig)
print(f"system counts: {dict(counts)}")
print(f"max Stouffer z among survivors: {max(z for _, z in survivors):.2f}")
print(f"written: {OUT_PNG}")
print(f"written: {OUT_PDF}")
