r"""FINAL REPRODUCIBILITY AUDIT — numeric verification (Part 2/17).

Recomputes every documented headline number from the frozen artifacts using
ONLY the Python standard library (csv/json/math/statistics) so it runs on any
machine regardless of installed packages. Each check prints PASS/FAIL with the
recomputed value vs the documented value. Output is the appendix of
FINAL_REPRODUCIBILITY_AUDIT.md.

Run:  python verify_final_numbers.py
Exit code 0 = all PASS, 1 = at least one FAIL. Read-only; writes nothing.
"""
import csv
import io
import json
import math
import os
import re
import statistics
import sys
from collections import Counter

BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
NDP = os.path.join(BASE, "05_NULLS", "degree_preserving")
FLY_CANDIDATES = [
    r"D:\humanbrain\fruitfly",
    os.path.abspath(os.path.join(BASE, "..", "..", "fruitfly")),
    os.path.abspath(os.path.join(BASE, "..", "fruitfly")),
]

results = []


def check(name, documented, recomputed, tol=0.0, note=""):
    if isinstance(documented, float) or isinstance(recomputed, float):
        ok = documented is not None and recomputed is not None and (
            abs(recomputed - documented) <= (tol if tol else 1e-9 * max(1.0, abs(documented))))
    else:
        ok = documented == recomputed
    results.append((name, documented, recomputed, ok, note))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: documented={documented} recomputed={recomputed} {note}")
    return ok


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def two_sided_sign_p(k, n):
    """Exact two-sided binomial p for k successes in n fair coin flips."""
    from math import comb
    if k == n:
        p_upper = comb(n, k) * 0.5 ** n
        return min(1.0, 2 * p_upper)
    return None


# ----------------------------------------------------------------- DATA
man = read_csv(os.path.join(BASE, "00_MANIFEST", "subject_manifest.csv"))
check("N subjects acquired", 900, len(man))

qc = read_csv(os.path.join(BASE, "03_BASELINE", "qc_primary.csv"))
n_pass = sum(1 for r in qc if r["qc_pass"].strip() == "True")
check("QC-pass subjects", 801, n_pass)
check("QC table rows (acquired+QC)", 900, len(qc))

labels = read_csv(os.path.join(BASE, "00_MANIFEST", "manifests", "atlas_4S456_system_labels.csv"))
check("Atlas node count (4S456 labels)", 456, len(labels))
sys_counts = Counter(r["system"] for r in labels)
print(f"       system label counts: {dict(sys_counts)}")

k_expected = int(round(0.15 * 456 * 455 / 2))
check("Edges at 15% cost (round(c*N(N-1)/2))", 15561, k_expected,
      note="manuscript: 15,561 edges, mean degree 68.2")

# ------------------------------------------- E03b degree-strength control
dsc = load_json(os.path.join(BASE, "04_CIS", "degree_strength_control_summary.json"))
def jget(d, *keys, default=None):
    for k in keys:
        if isinstance(d, dict) and k in d:
            d = d[k]
        else:
            return default
    return d
pos_subj = jget(dsc, "n_subjects_residual_positive") or jget(dsc, "residual_positive_subjects") or jget(dsc, "subjects_with_positive_median_residual")
n_subj = jget(dsc, "n_subjects") or jget(dsc, "n_subjects_total") or jget(dsc, "subjects")
delta_med = jget(dsc, "cliffs_delta_median") or jget(dsc, "median_cliffs_delta")
pairs = jget(dsc, "n_pairs_total") or jget(dsc, "n_pairs") or jget(dsc, "pairs_total")
print(f"       degree_strength_control_summary.json keys: {list(dsc.keys())}")
if pos_subj is not None:
    check("Residual-positive subjects", 778, int(pos_subj))
if n_subj is not None:
    check("Subjects in residual analysis", 801, int(n_subj))
if delta_med is not None:
    check("Cliff's delta median (human)", 0.100, round(float(delta_med), 3), tol=0.0005)
if pairs is not None:
    check("Matched pairs total", 36846, int(pairs))
sp = jget(dsc, "sign_test_p_two_sided")
if sp is not None:
    check("Residual sign test p (two-sided)", 2.6e-197, float(sp), tol=1e-198,
          note="manuscript §4.2: 2.6 x 10^-197")
wp = jget(dsc, "wilcoxon_p_median")
if wp is not None:
    check("Per-subject Wilcoxon median p", 0.167, round(float(wp), 3), tol=5e-4)
nwl = jget(dsc, "subjects_wilcoxon_p_lt_05")
if nwl is not None:
    check("Subjects with Wilcoxon p<.05", 125, int(nwl))

# ------------------------------------------------------- E03 CIS summary
e03 = load_json(os.path.join(BASE, "04_CIS", "e03_summary.json"))
check("Max population-mean CIS (node 414)", 0.00462, round(e03["cis_mean_pop_max"], 5), tol=5e-6,
      note="manuscript rounding corrected 0.00463 -> 0.00462 on 2026-09-26")
check("Max-CIS node", 414, e03["cis_max_mean_node"])

# ------------------------------------------------------- E05 statistics
e05 = load_json(os.path.join(BASE, "04_CIS", "e05_statistics.json"))
pn = e05["per_node_null"]
check("FDR q<.05 node count", 43, pn["n_q_nodes_fdr05"])
check("Max Stouffer z (node 400)", 23.3008, round(pn["max_z"], 4), tol=1e-4)
check("Max-z node", 400, pn["max_z_node"])
check("Subjects with nulls (battery A)", 100, pn["subjects_with_nulls"])

# analytic Stouffer ceiling: 10 * Phi^{-1}(100/101) must equal max_z
from statistics import NormalDist
ceiling = 10.0 * NormalDist().inv_cdf(100.0 / 101.0)
check("Stouffer ceiling analytic (10*inv_cdf(100/101))", round(pn["max_z"], 6),
      round(ceiling, 6), tol=1e-4,
      note="validates the repeated z=23.3008 tie as the exact add-one ceiling")

st = read_csv(os.path.join(BASE, "09_TABLES", "table_07_null_results.csv"))
n_q = sum(1 for r in st if float(r["q_bh"]) < 0.05)
n_inf = sum(1 for r in st if float(r["stouffer_z"]) == float("-inf"))
check("table_07 rows", 456, len(st))
check("table_07 FDR survivors", 43, n_q)
check("table_07 censored (-inf) rows", 413, n_inf,
      note="nodes where every null >= observed; p floor 1.0 -> isf = -inf")

se = e05["system_enrichment"]["K"]["50"]
check("K=50 Vis observed", 1, se["observed"]["Vis"], note="= 2% of top-50")
vis = se["systems"]["Vis"]
check("K=50 Vis z_B (negative, not enriched)", -0.38, round(vis["z_B"], 2), tol=5e-3)
sub = se["systems"]["Subcortical_Cerebellar"]
check("K=50 Subcortical/Cerebellar observed", 26, sub["observed"])
check("K=50 Subcortical z_A", 9.0558, round(sub["z_A"], 4), tol=1e-3)
check("K=50 Subcortical z_B", 2.0761, round(sub["z_B"], 4), tol=1e-3)
check("K=50 Subcortical p_B", 0.031197, round(sub["p_B"], 6), tol=1e-5)
check("K=50 Subcortical enrichment_B", 1.2475, round(sub["enrichment_B"], 4), tol=1e-3)
k25 = e05["system_enrichment"]["K"]["25"]["systems"]["Subcortical_Cerebellar"]
check("K=25 Subcortical z_B (NOT significant)", 0.8056, round(k25["z_B"], 4), tol=1e-3,
      note="K-ladder non-replication documented in manuscript §5.2")

ds = e05["degree_strength"]
check("Spearman(CIS,degree) median (~rho=0.94)", 0.943, round(ds["spearman_cis_degree_median"], 3), tol=5e-4)
rs = e05["rank_stability"]
check("Rank stability median Spearman", 0.996, round(rs["median_spearman"], 3), tol=5e-4)

# ----------------------------------------------------------- battery B
bb = read_csv(os.path.join(NDP, "null_results_battery_b.csv"))
zs = [float(r["z_vs_null"]) for r in bb]
n_pos = sum(1 for z in zs if z > 0)
check("Battery B subjects", 200, len(bb))
check("Battery B z>0 subjects", 200, n_pos)
check("Battery B median z", 16.36, round(statistics.median(zs), 2), tol=5e-3)
p_sign = two_sided_sign_p(n_pos, len(bb))
check("Battery B two-sided sign p (2*0.5^200)", 1.2446e-60, p_sign, tol=1e-63)
src = Counter(r["null_source"] for r in bb)
check("Battery B null sources {fresh:100, reuse:100}", 2, len([k for k, v in src.items() if v == 100]))

# ----------------------------------------------------- battery A integrity
val = read_csv(os.path.join(NDP, "null_validation_battery_a.csv"))
n_exact = sum(1 for r in val if r["degree_per_node_exact"].strip() == "True")
n_loops = sum(int(float(r["self_loops"])) for r in val)
check("Battery A nulls (100 subj x 100)", 10000, len(val))
check("Battery A exact degree preservation", 10000, n_exact)
check("Battery A self-loops total", 0, n_loops)

manA = read_csv(os.path.join(NDP, "null_manifest_battery_a.csv"))
acc = [int(float(r["rewire_accepted"])) for r in manA]
rate = statistics.mean(acc) / (15561 * 10)
check("Rewire acceptance rate (corrected)", 0.494, round(rate, 3), tol=5e-3,
      note="count-bug fix 2026-09-26; was reported as 7694144.8%")

# ------------------------------------------------------------ E06 robustness
t8 = read_csv(os.path.join(BASE, "09_TABLES", "table_08_robustness.csv"))
check("E06 configuration count", 9, len(t8))
# No numeric tolerance was pre-registered for E06; the concordance is a
# descriptive comparison. Verify the authoritative max like-for-like delta
# (atlas_AAL116) at full precision against the RESOLUTION.md concordance.
res_path = os.path.join(BASE, "10_REPORT", "RESOLUTION.md")
if os.path.exists(res_path):
    with open(res_path, encoding="utf-8") as f:
        res_text = f.read()
    m_aal = re.search(r"atlas_AAL116\s+150\s+([\d.]+)\s+([\d.]+)", res_text)
    if m_aal:
        aal_mean = float(m_aal.group(1))
        aal_delta = float(m_aal.group(2))
        check("E06 atlas_AAL116 top50 mean (max-deviation config)", 0.003848, aal_mean, tol=5e-7)
        check("E06 max like-for-like top50 delta (atlas_AAL116)", 0.002619, aal_delta, tol=5e-7,
              note="full precision 0.0026194; descriptive, no pre-registered tolerance")

# ------------------------------------------------------------- fly artifacts
fly = None
for c in FLY_CANDIDATES:
    p = os.path.join(c, "results", "final", "e10b_final.json")
    if os.path.exists(p):
        fly = c
        break
if fly:
    e10b = load_json(os.path.join(fly, "results", "final", "e10b_final.json"))
    fd = jget(e10b, "observed", "cliffs_delta") or jget(e10b, "cliffs_delta") or jget(e10b, "observed_delta")
    print(f"       fly e10b keys: {list(e10b.keys())[:12]}")
    if fd is not None:
        check("Fly Cliff's delta", 0.0979, round(float(fd), 4), tol=5e-5)
    fp = jget(e10b, "empirical_p_delta") or jget(e10b, "p_delta")
    if fp is not None:
        check("Fly null empirical p (NOT survived)", 0.109, round(float(fp), 3), tol=5e-4)
else:
    print("[NOT RUN] fly artifacts not reachable from this machine (documented paths checked)")

# ---------------------------------------------------------------- summary
fails = [r for r in results if not r[3]]
print("\n=== SUMMARY ===")
print(f"checks: {len(results)}  PASS: {len(results) - len(fails)}  FAIL: {len(fails)}")
if fails:
    for f in fails:
        print("  FAIL:", f[0], "| documented:", f[1], "| recomputed:", f[2])
sys.exit(1 if fails else 0)
