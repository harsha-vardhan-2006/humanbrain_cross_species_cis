r"""Figures 1-9 (regenerable from frozen artifacts; skips missing inputs).

Reproducible: py 08_FIGURES/make_figures.py  (writes PNG+PDF into 08_FIGURES)
"""
import json, os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE = r"D:\humanbrain\humanbrain\13_CROSS_SPECIES_CIS"
FIG = os.path.join(BASE, "08_FIGURES")
os.makedirs(FIG, exist_ok=True)
plt.rcParams.update({"figure.dpi": 150, "font.size": 8})


def _save(fig, name):
    fig.savefig(os.path.join(FIG, name + ".png"), bbox_inches="tight")
    fig.savefig(os.path.join(FIG, name + ".pdf"), bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


def fig1_workflow():
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.axis("off")
    steps = ["AOMIC 900\n(READ-ONLY)", "E01 extract\n+QC", "E02 baseline\n+QC gate",
             "E03 exact CIS\n900 subj", "E03b degree\ncontrols", "E04 nulls\n100x100",
             "E05 stats\nBH-FDR", "E06 robust-\nness", "E07 cross-scale\n(fly frozen)",
             "E08 decision\nA/B/C/D"]
    for i, s in enumerate(steps):
        x = i % 5
        y = 1 - (i // 5)
        ax.add_patch(plt.Rectangle((x * 1.9, y), 1.6, 0.8,
                                   fill=False, lw=1))
        ax.text(x * 1.9 + 0.8, y + 0.4, s, ha="center", va="center", fontsize=7)
        if x < 4:
            ax.annotate("", xy=(x * 1.9 + 1.9, y + 0.4),
                        xytext=(x * 1.9 + 1.6, y + 0.4),
                        arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.annotate("", xy=(0.8, 1.0), xytext=(8.4, 0.0),
                arrowprops=dict(arrowstyle="->", lw=0.8, ls=":"))
    ax.set_xlim(-0.1, 9.6)
    ax.set_ylim(-0.1, 2.0)
    _save(fig, "fig01_workflow")


def fig2_population():
    qc = pd.read_csv(os.path.join(BASE, "03_BASELINE", "qc_primary.csv"))
    b = pd.read_csv(os.path.join(BASE, "03_BASELINE",
                                 "baseline_network_properties.csv"))
    p = b[(b.atlas == "atlas_4S456Parcels") & (b.cost == 0.15)]
    fig, axes = plt.subplots(1, 3, figsize=(9, 2.6))
    axes[0].hist(p["ge"], bins=40, color="#4477aa")
    axes[0].set_xlabel("global efficiency @15% cost")
    axes[0].set_ylabel("subjects")
    axes[1].hist(qc.n_components_multi, bins=range(0, 6), color="#66ccee")
    axes[1].set_xlabel("multi-node components")
    flags = {c.replace("flag_", ""): int(qc[c].sum())
             for c in qc.columns if c.startswith("flag_")}
    axes[2].bar(flags.keys(), flags.values(), color="#ee6677")
    axes[2].set_ylabel("flagged subjects")
    axes[2].tick_params(axis="x", rotation=45)
    fig.suptitle(f"Human cohort (QC pass {int(qc.qc_pass.sum())}/900)",
                 fontsize=9)
    _save(fig, "fig02_population_qc")


def fig3_population_cis():
    f = os.path.join(BASE, "04_CIS", "population_cis_summary.csv")
    if not os.path.exists(f):
        return print("skip fig03 (no population summary yet)")
    g = pd.read_csv(f).sort_values("cis_mean", ascending=False)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3))
    axes[0].plot(g.cis_mean.values, lw=1)
    axes[0].axhline(0, color="k", lw=0.5)
    axes[0].set_xlabel("node rank (population mean CIS)")
    axes[0].set_ylabel("mean CIS")
    axes[1].plot(g.sort_values("top50_rate", ascending=False).top50_rate.values)
    axes[1].set_xlabel("node rank (top-50 membership rate)")
    axes[1].set_ylabel("fraction of subjects in top-50")
    _save(fig, "fig03_population_cis")


def fig4_cis_vs_degree_strength():
    f = os.path.join(BASE, "04_CIS", "population_cis_summary.csv")
    if not os.path.exists(f):
        return print("skip fig04 (no population summary yet)")
    g = pd.read_csv(f)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3))
    axes[0].scatter(g.degree_mean, g.cis_mean, s=4, alpha=0.5)
    axes[0].set_xlabel("mean degree")
    axes[0].set_ylabel("mean CIS")
    axes[1].scatter(np.log10(g.strength_mean + 1), g.cis_mean, s=4, alpha=0.5)
    axes[1].set_xlabel("log10 mean strength")
    axes[1].set_ylabel("mean CIS")
    _save(fig, "fig04_cis_vs_degree_strength")


def fig5_degree_controlled():
    f = os.path.join(BASE, "04_CIS", "degree_strength_control_per_subject.csv")
    if not os.path.exists(f):
        return print("skip fig05 (no degree control yet)")
    ps = pd.read_csv(f)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3))
    axes[0].hist(ps.residual_median, bins=40, color="#4477aa")
    axes[0].axvline(0, color="k", lw=0.8)
    axes[0].set_xlabel("subject median residual CIS (obs - control)")
    axes[1].hist(ps.cliffs_delta, bins=40, color="#66ccee")
    axes[1].axvline(0, color="k", lw=0.8)
    axes[1].set_xlabel("Cliff's delta (top-decile vs matched)")
    _save(fig, "fig05_degree_controlled")


def fig6_obs_vs_null():
    st = os.path.join(BASE, "09_TABLES", "table_07_null_results.csv")
    bb = os.path.join(BASE, "05_NULLS", "degree_preserving",
                      "null_results_battery_b.csv")
    made = False
    if os.path.exists(st):
        d = pd.read_csv(st)
        # Stouffer z is -inf for nodes where every battery-A null exceeded the
        # observed value (p_one_sided hits the 1.0 floor, so isf(1.0) = -inf).
        # 413/456 nodes are in that state; they are non-significant by
        # construction (p = q = 1.0). Histograms cannot span -inf, so plot the
        # finite nodes and report the censored count in the panel label.
        fin = d[np.isfinite(d.stouffer_z)]
        n_cens = len(d) - len(fin)
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.hist(fin.stouffer_z, bins=50, color="#4477aa")
        ax.set_xlabel("per-node Stouffer z (obs vs degree-preserving nulls)")
        ax.set_ylabel("nodes")
        ax.set_title(f"{len(fin)} finite; {n_cens} at p=1 floor (z=-inf)", fontsize=7)
        _save(fig, "fig06a_stouffer")
        made = True
    if os.path.exists(bb):
        b = pd.read_csv(bb)
        fig2, ax2 = plt.subplots(figsize=(5, 3))
        ax2.hist(b.z_vs_null, bins=30, color="#ee6677")
        ax2.axvline(0, color="k", lw=0.8)
        ax2.set_xlabel("top-50 concentration z vs subject-matched nulls")
        ax2.set_ylabel("subjects")
        _save(fig2, "fig06b_battery_b")
        made = True
    if made:
        plt.close("all")
        _save(plt.figure(), "fig06_placeholder_empty") if False else None
    if not made:
        return print("skip fig06 (no null results yet)")


def fig7_robustness():
    f = os.path.join(BASE, "09_TABLES", "table_08_robustness.csv")
    if not os.path.exists(f):
        return print("skip fig07 (no robustness table yet)")
    d = pd.read_csv(f)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3))
    axes[0].barh(d.condition, d.top50_mean_of_means, color="#4477aa")
    axes[0].set_xlabel("top-50 mean CIS (population mean)")
    axes[1].barh(d.condition, d.gini_abs_cis_median, color="#ee6677")
    axes[1].set_xlabel("Gini of |CIS| (median across subjects)")
    axes[1].tick_params(axis="y", labelsize=6)
    _save(fig, "fig07_robustness")


def fig8_cross_scale():
    """Fly vs human normalized comparators (Cliff's delta + K50 enrichment
    vs control B), reading frozen fly artifacts + human phase outputs."""
    import json
    fly = r"D:\humanbrain\fruitfly"
    try:
        e10b = json.load(open(os.path.join(fly, "results", "final",
                                           "e10b_final.json")))
        e12 = json.load(open(os.path.join(fly, "results", "tables",
                                          "e12_strong_results.json")))
    except OSError:
        return print("skip fig08 (fly artifacts unavailable)")
    human_delta = None
    dc = os.path.join(BASE, "04_CIS", "degree_strength_control_summary.json")
    if os.path.exists(dc):
        human_delta = json.load(open(dc)).get("cliffs_delta_median")
    fig, axes = plt.subplots(1, 2, figsize=(8, 3))
    axes[0].bar(["fly\n(e10b)", "human\n(E03b)"],
                [e10b["observed"]["cliffs_delta"],
                 human_delta if human_delta is not None else 0.0],
                color=["#4477aa", "#ee6677"])
    axes[0].set_ylabel("Cliff's delta (CIS structure\nbeyond matched controls)")
    axes[1].bar(["fly K=50", "human K=50"],
                [e12["K50"]["enrichment_vs_degree_matched"], np.nan],
                color=["#4477aa", "#ee6677"])
    axes[1].set_ylabel("top-50 enrichment vs\ndegree-matched control B")
    axes[1].text(1, 0.5, "E05\npending", ha="center", transform=axes[1].transAxes)
    _save(fig, "fig08_cross_scale")


def fig9_conceptual():
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.axis("off")
    ax.text(0.5, 0.9, "Control-impact architecture decision", ha="center",
            fontsize=9)
    boxes = [("degree/strength\ncontrols", 0.15, 0.55),
             ("degree-preserving\nnulls", 0.5, 0.55),
             ("robustness\n(atlas/weight/cost)", 0.85, 0.55)]
    for t, x, y in boxes:
        ax.add_patch(plt.Rectangle((x - 0.14, y - 0.12), 0.28, 0.24,
                                   fill=False))
        ax.text(x, y, t, ha="center", va="center", fontsize=7)
    ax.text(0.5, 0.22, "RESULT A residual architecture  |  RESULT B "
            "degree/topology-explained\nRESULT C mixed  |  RESULT D not "
            "supported", ha="center", fontsize=8)
    for x, _ in [(0.15, 0), (0.5, 0), (0.85, 0)]:
        ax.annotate("", xy=(0.5, 0.34), xytext=(x, 0.43),
                    arrowprops=dict(arrowstyle="->", lw=0.8))
    _save(fig, "fig09_conceptual")


if __name__ == "__main__":
    fig1_workflow()
    fig2_population()
    fig3_population_cis()
    fig4_cis_vs_degree_strength()
    fig5_degree_controlled()
    fig6_obs_vs_null()
    fig7_robustness()
    fig8_cross_scale()
    fig9_conceptual()
    print("figures done (missing inputs skipped with notice)")
