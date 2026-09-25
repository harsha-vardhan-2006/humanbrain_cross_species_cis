# FINAL RESULT DECISION — 13_CROSS_SPECIES_CIS
**Study:** Cross-scale control-impact architecture, fly → human (900 subjects)
**Date frozen:** 2026-09-23 · **Protocol:** PROTOCOL_FREEZE (RESEARCH_LOG E01) · **Log:** RESEARCH_LOG.md E00–E06

This document applies the **pre-registered decision matrix** (STUDY_DESIGN §2,
restated verbatim in `10_REPORT/REPORT_SCAFFOLD.md` §1) to the frozen artifacts.
No rule was amended after seeing data. Three rules, decided once:

- **R1 — layer-1 replication (degree-driven control impact):** battery B sign
  test across 200 subjects.
- **R2 — layer-2 replication (degree-independent residual, system-structured):**
  per-node Stouffer/BH-FDR (battery A) + E03b residual sign test + system
  enrichment z_B for a pre-specified system (visual/sensory first).
- **R3 — cross-scale bridge:** normalized comparators only
  (table_09_cross_scale.csv).

---

## 1. Observed-level results (complete, artifact-traced)

| # | Result | Value | Artifact |
|---|--------|-------|----------|
| 1 | Cohort | 900 cached, 801 QC-pass (89.0%) | `09_TABLES/table_01_subject_cohort.csv` |
| 2 | Global efficiency (primary cfg) | median E0 = 0.5468 [IQR 0.5441–0.5497] | `04_CIS/e03_summary.json` |
| 3 | Max population-mean CIS | 0.00463 at node 414 | `04_CIS/e03_summary.json` |
| 4 | Most stable top-50 node | node 400, top-50 in **100%** of 900 subjects | `04_CIS/e03_summary.json` |
| 5 | Top-5 population ranking (nodes) | 415, 401, 414, 400, 442 — all top-50 in ≥99.3% of subjects | `09_TABLES/table_05_top_stability.csv` |
| 6 | **Residual CIS vs degree-matched controls** | positive in **778/801** subjects; sign p = **2.6e-197** | `04_CIS/degree_strength_control_summary.json` |
| 7 | Effect size (Cliff's δ, median) | **0.100** [IQR 0.078–0.129]; fly: **0.0979** | same + `fruitfly results/final/e10b_final.json` |
| 8 | Residual magnitude | median 5.97e-05 (≈3× the population-mean CIS itself) | `degree_strength_control_summary.json` |
| 9 | Fraction of top-decile nodes beating matched control | 58.8% (chance = 50%) | same |
| 10 | Visual share of population top-50 | **2%** (human) vs **80%** (fly, visual_centrifugal) | `07_CROSS_SCALE/table_09_cross_scale.csv` |
| 11 | Fast-CIS validation | max deviation 4e-16 (machine ε) vs scipy reference, before any null use | `05_NULLS/degree_preserving/FAST_IMPLEMENTATION_VALIDATION.md` |
| 12 | Null-rewiring gates | exact per-node degree preservation, adversarial suite PASS (hub-selfloop/pendant, dense, ring) | `null_models.py --test` outputs |

Reading: the human connectome reproduces the fly's **two-layer architecture**:
a degree-dominated layer (most CIS is degree-predictable) plus a small but
hyper-consistent degree-independent residual (rule 6: sign p ≈ 10⁻¹⁹⁷), with a
cross-species effect-size match at the third decimal (rule 7). The system
*identity* of the residual, however, does not transfer (rule 10) — see §4.

## 2. Null-gated gates (pre-registered; resolution pending E04/E05)

The degree-preserving null battery is running (battery A: 100 subjects × 100
nulls, chunked atomic checkpoints; battery B: 200 subjects × 100 nulls at
top-50 positions). The chain (`e04_chain`) executes battery B → E05 → E06
automatically on completion. Each gate below names its exact resolving
statistic and artifact; **none may be re-worded after results land.**

| Gate | Resolving statistic | Threshold (pre-set) | Status | Artifact when done |
|------|--------------------|---------------------|--------|--------------------|
| **R1** | Sign test over subject-level z_vs_null (battery B, n=200) | majority positive, p < .05 | ⏳ PENDING | `05_NULLS/degree_preserving/null_results_battery_b.csv` |
| **R2a** | Per-node Stouffer Z, BH-FDR q<.05 | ≥1 node survives | ⏳ PENDING | `09_TABLES/table_07_null_results.csv` |
| **R2b** | System enrichment z_B (control B = degree-matched pools, 10k perms) | z_B > 0 for pre-specified sensory/visual system | ⏳ PENDING | `04_CIS/e05_statistics.json` |
| **R3** | table_09 concordance on normalized comparators | δ match + design match (already met on δ; enrichment rows fill from E05) | ◐ PARTIAL (δ row complete) | `07_CROSS_SCALE/table_09_cross_scale.csv` |

Supporting robustness (secondary, does not gate the outcome): 9 configurations
(4 atlases, 3 weights, 4 costs) on the frozen n=150 cohort — concordance vs
primary expected in `06_ROBUSTNESS/*/` and table_08.

**Important reading of rule 6 vs R1/R2:** E03b establishes the residual exists
*at fixed observed topology* (degree-matched node pairs within the same graph).
The null battery asks the orthogonal question — whether observed CIS magnitudes
exceed *rewired* graphs of identical degree sequence. Both layers are required
by the protocol; E03b cannot substitute for R1/R2, nor vice versa.

## 3. Decision (as of this document's date)

**PROVISIONAL — observed-level architecture replicated; null-gated confirmation
in execution.** If R1 and R2a/b resolve positive, the verdict becomes:
**"Outcome-B pattern replicated in human; cross-scale bridge established at the
architectural level (δ ≈ 0.10 on both scales), with system identity of the
residual non-transferred (fly: visual-centrifugal; human: pending E05 mapping)."**
If R1 resolves negative, the pre-registered alternative reading applies:
human CIS is fully degree-explained at the graph level → **Outcome-A analog**,
reported as a boundary condition on the fly result, not a failure.

## 4. Honest-limitations register (frozen with the decision)

1. **Modality break:** fly digraph (directed, cell-scale) vs human undirected
   weighted (region-scale, 456 nodes). Directional CIS variant is *impossible*
   in the human derivatives, not skipped — documented as CP03/CP05
   APPROXIMATELY_COMPARABLE.
2. **No anatomical homology claims.** "Visual" in fly = visual_centrifugal cell
   classes; in human = Vis macro-system. The 80%→2% share difference is a real
   architectural divergence under this comparison, not a labeling artifact.
3. **Cost 0.15 proportional threshold** shapes both E0 and CIS; cost ladder
   (10/20/25) in E06 addresses it; raw densities (0.45–0.88) preclude
   unthresholded path-length statistics.
4. **QC exclusion of 99/900** is property-based (density/strength IQR flags),
   pre-registered; excluded subjects were not re-analyzed.
5. **E03b Wilcoxon vs sign test:** per-pair Wilcoxon median p = 0.167 (125/801
   subjects p<.05) while the sign test is p≈10⁻¹⁹⁷ — the residual is *small but
   near-universal*; both are reported, neither suppressed.
6. **Multiple-comparisons surface:** per-node FDR (456 tests) and enrichment
   p-values are the only confirmatory families; everything else is descriptive.
7. **Single derivative pipeline** (AOMIC-ID1000, SIFT2); no second-acquisition
   replication is in scope.

## 5. Verification chain

Every number above traces to a frozen artifact (column 4). The pipeline
reference implementation (`node_cis`, scipy Dijkstra) produced all observed
statistics; the optimized implementation used for null-scale compute was
validated to machine epsilon against it *before* any null use, and the gates
re-run at battery launch. RESEARCH_LOG E00–E06 documents each step's
validation gates and failures honestly (two mid-run implementation bugs were
caught by the gates themselves and fixed before any number was produced).

— *Generated by Buffy (Codebuff), 2026-09-23. This file is frozen once R1–R3
resolve; the resolution entry will be appended, not edited.*

---

## 6. RESOLUTION (appended 2026-09-26 00:35 — no earlier text edited)

R1 = POSITIVE; R2a = POSITIVE; R2b = NEGATIVE.
Integrity: battery A 10000/10000 nulls, degree exact 100.00%, self-loops 0.

**Final verdict: Layer-1 replicated (concentration exceeds degree-preserving nulls); layer-2 null evidence absent or not system-structured -> weaker bridge, honest report per the frozen matrix.**

Full resolution: RESOLUTION.md (this file's §2 table is now historical; the gates resolved exactly as pre-registered).
