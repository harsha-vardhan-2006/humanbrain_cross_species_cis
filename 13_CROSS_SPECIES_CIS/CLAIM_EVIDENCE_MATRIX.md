# CLAIM–EVIDENCE MATRIX — Cross-Species Control-Impact Study

**Created:** 2026-09-26 (post-freeze framing audit). Every row cites the
authoritative artifact; "Strength" uses the classes: **Established**
(literature) · **Supported by current data** · **Suggestive** ·
**Hypothesis-generating** · **Not supported** · **Should not be claimed**.
Future manuscript edits should only use the "Allowed wording" column.

| # | Claim | Evidence | Source / artifact | Strength | Allowed wording |
|---|---|---|---|---|---|
| 1 | 900 AOMIC-ID1000 subjects acquired; 801 QC-pass; 456-node atlas; 15,561 edges at 15% cost | Manifests, QC tables, byte-verified zips | `00_MANIFEST/`, `03_BASELINE/qc_primary.csv`, `table_01/03` | Supported by current data | "801 QC-pass subjects (900 acquired)" |
| 2 | Exact per-node CIS computed for all 456 nodes per subject | Reference-vs-naive validation 6.1e-16; fast path 4e-16 | `04_CIS/REFERENCE_IMPLEMENTATION_VALIDATION.md`, `e03_summary.json` | Supported by current data | "exact per-node CIS for all 456 nodes in each subject" |
| 3 | CIS is strongly degree-related | Median Spearman ρ = 0.943 (CIS–strength 0.486) | `e05_statistics.json`; RESOLUTION.md supporting stats | Supported by current data | "strongly associated with degree (median ρ = 0.94)" |
| 4 | Top-50 CIS concentration exceeds degree-preserving null expectations (H1) | 200/200 subjects; median z = 16.36; sign p = 1.24e-60 | `null_results_battery_b.csv`; RESOLUTION.md R1 | Supported by current data | "exceeded in 200/200 tested subjects" |
| 5 | A small degree-independent residual exists and is directionally near-universal (H2) | 778/801 subjects (97.1%); δ = 0.100 [0.078–0.129]; sign p = 2.6e-197; 36,846 matched pairs | `degree_strength_control_summary.json`; table_06 | Supported by current data | "detectable in 778/801 subjects; δ = 0.100" — NOT "universal" (22/801 not positive) |
| 6 | 43/456 nodes survive FDR (R2a) | BH-FDR q<.05; max Stouffer z = 23.30 (= analytic ceiling) | `table_07_null_results.csv`; RESOLUTION.md R2a | Supported by current data | "43/456 nodes survive FDR" |
| 7 | The residual is robustly system-specific (H3) | R2b NEGATIVE; Vis z_B = −0.38; only Subcortical/Cerebellar nominal (z_B 2.08, p .031, 1.25×), absent at K=25 (z_B 0.81), degree-anchored | `e05_statistics.json`; RESOLUTION.md R2b | **Not supported** | "no robust canonical-system-specific explanation was established" — never "system-specific residual" |
| 8 | The subcortical/cerebellar nominal signal is a system mechanism | Degree-anchored; K-ladder fragile; R2b rule not met | MANUSCRIPT_DRAFT §5.2; HYPOTHESIS_RESULT_MATRIX guardrail 1 | **Should not be claimed** | "degree-anchored subcortical concentration" at most |
| 9 | Human visual contribution of top-50 is 2% | obs 1/50 Vis | `e05_statistics.json`; CROSS_SCALE_ANALYSIS.md | Supported by current data | "2% of the human top 50" |
| 10 | Fly: GABA-specific control hypothesis (original H1 of fly study) | Rejected under degree-preserving nulls: p_δ = 0.109, p_median = 0.782, z = 1.21 | `fruitfly/results/final/e10b_final.json` | **Not supported** | "the original inhibitory/GABA-specific hypothesis did not survive degree-preserving null testing" |
| 11 | Fly: visual–centrifugal enrichment survives degree matching | 21/50; 2.63× (z = 5.30, p ≈ 1e-4); consistent K=25/K=100 | `e12_strong_results.json` | Supported by current data | "≈2.6× enrichment after degree matching" |
| 12 | Fly: 13/50 chokepoints individually beat degree-matched peers | 13/50 (10/13 visual); emp p < 0.0005–0.01; 9 tiny pools flagged | `e14_v2_summary.json`; catalogue v2 | Supported by current data | "13/50 matched peers exceeded" — actually "13/50 exceeded their peers"; pools <10 flagged |
| 13 | Fly residual effect size | δ = 0.0979, **not null-surviving** (p = 0.109) | `e10b_final.json` | Supported by current data | "fly δ = 0.0979, itself not null-surviving" |
| 14 | Fly dataset scale | 139,255 neurons (FAFB v783); analysis graph 138,584 nodes / 3,732,460 edges | `e10b_input/build_report.json`; fly paper | Supported by current data | "139,255-neuron FAFB v783 connectome" |
| 15 | Cross-scale: qualitatively similar two-component organization | Human δ 0.100 vs fly δ 0.0979; both degree-dominated; anatomical identity diverges (2% vs 80%) | `table_09_cross_scale.csv` (DIRECT rows); H4 | Supported by current data (architecture only) | "architecture replicates; anatomy does not" — architecture ONLY |
| 16 | Cross-scale: node-count difference | 139,255 neurons vs 456 parcels ≈ 3×10²-fold (analysis graph: 138,584/456 ≈ 304) | arithmetic from artifacts 1+14 | Supported by current data | "roughly three orders of magnitude in analyzed node count" — NOT "10⁵-fold" |
| 17 | Anatomical homology between fly and human residual architecture | Explicitly excluded by comparability rules; anatomy diverges | `cross_species_manifest.json` CP03/CP05; HYPOTHESIS_RESULT_MATRIX guardrail 3 | **Should not be claimed** | "no anatomical homology is claimed" |
| 18 | Conserved biological mechanism selecting residual chokepoints | Fly δ not null-surviving; anatomy diverges; R2b negative | HYPOTHESIS_RESULT_MATRIX guardrail 4; MANUSCRIPT_DRAFT §5.3 | **Should not be claimed** | "the mechanism selecting residual chokepoints is not established to be conserved" — at most; prefer "no conserved mechanism is claimed" |
| 19 | Two-component organization generalizes across nervous systems | Two species, two pipelines, one reconstruction each side | HYPOTHESIS_RESULT_MATRIX H4; MANUSCRIPT_DRAFT §5.6 | **Hypothesis-generating** | "motivates the hypothesis that…" — never "demonstrates" or "law" |
| 20 | The four-way/seven-element methodological combination is unoccupied | Literature audit E00/E17/E17a + 2026-09-26 sweep; NOVELTY_MATRIX | `10_LITERATURE/NOVELTY_MATRIX.md`; KUDRIAVTSEV review | Suggestive (bounded; "to our knowledge") | "To our knowledge, no prior study has combined…" |
| 21 | Node-removal CIS, degree-preserving nulls, hubs, NCT, cross-species connectomics invented here | All established in literature (see NOVELTY_AUDIT §1) | Alstott 2009; Crossley 2014; Maslov–Sneppen; Gu 2015; Venkadesh 2025 | **Should not be claimed** | "individual methods are established" |
| 22 | "First ever" / "first in the world" / universal law / new mechanism | Not demonstrated by any audit on file | — | **Should not be claimed** | never appears |
| 23 | Robustness of the human architecture | 9 configs reproduce the primary architecture; max like-for-like top-50-mean deviation 0.00262 (atlas_AAL116; no pre-registered numeric tolerance — descriptive); rank stability 0.996 | `table_08_robustness.csv`; RESOLUTION.md E06 | Supported by current data | "9 configurations reproduce the primary architecture; max deviation 0.00262; rank stability 0.996" — do not state a 0.0026 pass/fail gate (none was pre-registered) |
| 24 | Per-subject empirical p-values (battery B) resolve the tail | All at 1/101 floor | RESOLUTION.md; MANUSCRIPT_DRAFT §6 | Not supported (as stated) | "per-subject inference rests on z and the population sign test" |
| 25 | Dataset is "SIFT2" | Weight is `sift_radius2_count_connectivity` (SIFT-filtered counts); "SIFT2" is a different algorithm | `02_PREPROCESSING/cache_io.py`; Zenodo record | **Should not be claimed** | "SIFT-filtered streamline counts" |
| 26 | Limitations register is complete and preserved | Undirected graphs (directed variant impossible); single pipeline/acquisition; residual near CIS noise floor; battery-B p at the 1/101 floor; subcortical residual K-ladder-fragile; ENVIRONMENT_MANIFEST provenance gap; Kudriavtsev 2026 full text verified via proxy only (direct access blocked) | MANUSCRIPT_FINAL §4.10; FINAL_RESEARCH_STATUS §8 | Established (as disclosed limitations) | state each limitation as documented; do not omit any |

## Interpretation guardrails (binding, from HYPOTHESIS_RESULT_MATRIX.md)

1. H3 stays negative; guardrail 1 applies to any future edit.
2. No mechanism, homology, or universal-law claims (guardrails 2–3).
3. The fly–human δ similarity is partly fortuitous (guardrail 4).
4. H2 support does not soften H3 (guardrail 5).
