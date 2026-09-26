# REPORT SCAFFOLD — 13_CROSS_SPECIES_CIS

Working draft for FINAL_RESULT_DECISION.md + MANUSCRIPT_DRAFT.md.
Everything below either (a) is already frozen fact, or (b) carries a
`[T: path]` token marking the artifact the live number will be read from.
Nothing here is interpretable until E04/E05/E06 complete; tokens are filled
by `fill_report.py` (to be written) and manually reviewed.

---

## 1. Pre-registered outcome rules (from STUDY_DESIGN.md §2 + PROTOCOL_FREEZE)

The fly study fixes the *prediction*: an Outcome-B pattern —
(i) CIS is dominated by degree (control-A null ≈ degree-matched expectation);
(ii) any residual (CIS beyond degree) is system-structured rather than diffuse,
with **sensory/visual systems as the pre-specified candidates**.

Confirmatory branches (decided once, after E05/E06, in FINAL_RESULT_DECISION.md):

- **R1 (replication of layer 1):** observed top-50 median CIS exceeds the
  degree-preserving null in the majority of subjects (battery B sign test
  `p < .05`, [T: 05_NULLS/degree_preserving/null_results_battery_b.csv]).
  Positive → human layer-1 (degree-driven control impact) replicates.
  Negative → human CIS is *fully* degree-explained: Outcome-A-analog; report
  as a boundary condition on the fly result, not a failure.
- **R2 (replication of layer 2):** per-node Stouffer Z (battery A) survives
  BH-FDR q<.05 at ≥1 node AND E03b degree-controlled residual CIS is positive
  in the majority of subjects ([T: 04_CIS/degree_strength_control_results.csv])
  AND system enrichment z_B > 0 for a pre-specified system (visual/sensory
  first, per STUDY_DESIGN §2) ([T: 04_CIS/e05_statistics.json]).
- **R3 (cross-scale bridge):** fly ↔ human concordance on normalized
  comparators only (z-scores, enrichment ratios, Cliff's δ, concentration
  indices) — table_09_cross_scale.csv. No raw-value or anatomy claims (CP03/CP05).

Decision matrix (fixed in advance):
| R1 | R2 | Verdict |
|----|----|---------|
| + | + | Outcome-B replicated in human; bridge established |
| + | − | Layer 1 replicates; residual absent → weaker bridge, honest report |
| − | ± | Outcome-A analog; cross-species divergence at layer 1 |

Either branch is reportable (fly-paper standard). No branch may be redefined
after seeing the numbers.

## 2. Methods skeleton (already determined by frozen code)

- **Dataset:** AOMIC-ID1000 (900 subjects), SIFT-filtered streamline-count
  structural connectomes *[label corrected 2026-09-26; was "SIFT2" — the
  primary weight is `sift_radius2_count_connectivity`]*
  7 atlases; primary = 4S456Parcels, sift_radius2_count weight, 15% cost.
  [T: ../00_Metadata/AOMIC_VERIFICATION_REPORT.md; 00_MANIFEST/manifests/]
- **Preprocessing:** symmetric verification, diagonal zeroing, proportional
  threshold at cost 0.15 per subject. QC: [T: 03_BASELINE/qc_primary.csv]
  → 801/900 pass (E02).
- **CIS:** exact per-node CIS = 1 − E(G−i)/E(G), global efficiency on the
  thresholded undirected weighted graph; exact computation (456 removals),
  scipy Dijkstra reference implementation `node_cis` (E03; 900/900 subjects).
  Fast boolean-matmul implementation `node_cis_fast` validated to machine
  epsilon (max dev 4e-16) vs reference on real subject graphs before any
  null use; used only for null/robustness compute.
  [T: 02_PREPROCESSING/cache_io.py; 05_NULLS/degree_preserving/FAST_IMPLEMENTATION_VALIDATION.md]
- **Nulls:** Maslov–Sneppen degree-preserving rewiring (exact per-node degree
  sequence, adversarial regression suite ported from fly: hub-selfloop/
  pendant, dense, ring). Battery A: 100 subjects × 100 nulls, full per-node
  CIS per null. Battery B: 200 subjects × 100 nulls at top-50 observed
  positions (battery A reuse for overlapping subjects, identical seeds).
  [T: 05_NULLS/degree_preserving/null_manifest_battery_a.csv,
      null_validation_battery_a.csv (degree preservation 100% required)]
- **Degree/strength control (E03b):** per-subject linear CIS~degree+strength;
  top-decile nodes vs degree-matched controls (±10%); Wilcoxon signed-rank,
  Cliff's δ. [T: 04_CIS/degree_strength_control_results.csv]
- **Statistics (E05):** per-node one-sided empirical p per subject (add-one),
  Stouffer combination, BH-FDR q=.05; fly-E12-template system enrichment with
  control A (label shuffle) and control B (degree-matched peer pools, 10k
  perms); rank stability via 100 seeded half-splits.
- **Robustness (E06):** 9 secondary configurations (4 atlas, 2 extra
  weights, 3 extra costs) on the frozen n=150 cohort (seed 20260922);
  architecture-summary concordance vs primary (top-50 Jaccard, ρ(CIS,degree),
  concentration). [T: 06_ROBUSTNESS/atlas/, weights/, thresholds/]
- **Cross-scale (E07):** frozen fly artifacts only (e10b_final.json δ=0.0979
  z=1.21 p=0.109; e12_strong z_B=5.30 p=1e-4; e14 catalogue). Comparators
  classified DIRECT / NORMALIZED / QUALITATIVE. [T: 07_CROSS_SCALE/]

## 3. Results placeholders (fill after E04/E05/E06)

- E03 observed architecture: E0 median 0.5468; max pop-mean CIS 0.0046
  (node 414); node 400 top-50 in 100% of subjects. [DONE — e03_summary.json]
- E03b residual: positive in 778/801 subjects, sign p=2.6e-197, median
  Cliff's δ=0.100 (fly: 0.0979). [DONE]
- Battery A per-node Stouffer: [T: table_07_null_results.csv]
- System enrichment: [T: e05_statistics.json → system_enrichment]
- Battery B concentration: [T: null_results_battery_b.csv]
- Robustness concordance: [T: 06_ROBUSTNESS/*/, table_08_robustness.csv]
- Cross-scale table: [T: table_09_cross_scale.csv]

## 4. Figures/tables mapping

- fig5 (null distributions), fig6 (enrichment) ← E04/E05 outputs
- fig7 (robustness concordance) ← E06
- table_07/08/09 ← E05/E06/E07; rest built (build_tables.py).

## 5. Report-writing order (after battery lands)

1. E04b battery B (fast, ~1s/subject × 200) → E05 → fill §3 tokens
2. E06 robustness → fill concordance row
3. FINAL_RESULT_DECISION.md (decision matrix §1, no post-hoc edits)
4. FINAL_AUDIT.md (every number → artifact path; rules 1-5 above re-checked)
5. MANUSCRIPT_DRAFT.md from this scaffold
6. README status + RESEARCH_LOG E04-E10 entries
