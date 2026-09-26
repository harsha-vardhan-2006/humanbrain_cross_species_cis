# FIGURE CAPTIONS — Cross-Species CIS Study (submission edition, 2026-09-26)

Captions for the figure sequence defined in `10_REPORT/FIGURE_PROVENANCE.md`.
Every number is quoted from frozen artifacts; nothing was recomputed. File
numbering vs paper numbering is documented in the provenance table.

## Main figures

**Figure 1. Study design and pipeline.** From the population-scale
AOMIC-ID1000 structural-connectome resource (900 subjects acquired; 801
QC-pass on frozen, CIS-blind flags), exact per-node Control Impact Scores
were computed for all 456 nodes in every subject, followed by degree-matched
controls (±10% total degree), degree-preserving (Maslov–Sneppen) null
ensembles in two batteries, BH-FDR node-level inference, two-level
system-enrichment tests, a 9-configuration robustness ladder, and a
pre-registered cross-scale comparison with the frozen fly (FAFB v783)
study. *(File: `fig01_workflow.png|pdf`.)*

**Figure 2. CIS architecture and its degree relation (801 subjects).**
(A) Population-mean CIS across all 456 nodes; CIS is unitless — the fraction
of baseline global efficiency E(G) lost on node removal — with a maximum
population-mean CIS of 0.00462 (node 414). (B) CIS tracks node degree
(median Spearman ρ = 0.943) far more closely than strength
(ρ = 0.486), motivating the degree-controlled residual analysis of Fig. 4.
*(Files: `fig03_population_cis.png|pdf`, `fig04_cis_vs_degree_strength.png|pdf`.)*

**Figure 3. Degree-preserving null arbitration.** (A) Per-node Stouffer z
against the 100-null battery (battery A): 43 of 456 nodes carry finite
z (maximum 23.30, node 400); the remaining 413 nodes sit at the
add-one empirical-p floor and are explicitly counted as censored (−inf),
not hidden. (B) Per-subject top-50 concentration z (battery B): all
200/200 subjects lie above their null ensembles. All per-subject empirical
p-values sit at the 1/101 null-resolution floor; inference therefore rests
on the z statistics and the population sign test (two-sided
p = 1.24 × 10⁻⁶⁰). *(Files: `fig06a_stouffer.png|pdf`,
`fig06b_battery_b.png|pdf`.)*

**Figure 4. Degree-independent residual architecture (801 subjects).**
Subject-median CIS residual against degree- and strength-matched controls
(36,846 pairs), and the per-subject Cliff's δ distribution: the residual is
positive in 778/801 subjects (sign p = 2.6 × 10⁻¹⁹⁷) with median
δ = 0.100 [IQR 0.078–0.129]; 58.8% of individual matched comparisons beat
the control, and the median paired Wilcoxon p is 0.167 — small in effect
size, directionally near-universal across subjects.
*(File: `fig05_degree_controlled.png|pdf`.)*

**Figure 5. Anatomical distribution of the 43 FDR-surviving nodes.**
System counts of the 43/456 nodes surviving BH-FDR q < .05 (maximum
Stouffer z = 23.30): Subcortical/Cerebellar 39, Limbic 2, Default 2. The
pre-registered system-enrichment gate (R2b) itself was negative: visual
cortex holds 1 of the top 50 (2%), and the single nominal system signal
(Subcortical/Cerebellar, z_B = 2.08, p = .031, 1.25×) is degree-anchored
and absent at K = 25. Rendered from the frozen `table_07_null_results.csv`
plus the atlas label manifest; no statistics were recomputed.
*(File: `fig05_fdr_anatomical.png|pdf`.)*

**Figure 6. Cross-scale comparison (human vs fly), normalized comparators
only.** Effect-size (Cliff's δ), enrichment (z_B), and concentration
comparators, normalized per the cross-scale discipline tags: human
δ = 0.100 vs fly δ = 0.0979 (the fly value did not survive its own
degree-preserving null ensemble, p = 0.109); human visual share of the top
50 is 2% versus 80% visual-centrifugal in the fly. Absolute CIS values are
never compared across species (different units, graphs, and designs).
*(File: `fig08_cross_scale.png|pdf`.)*

## Supplementary figures

**Figure S1. Population QC (900 subjects).** QC flag distributions for the
full acquired cohort; 99 subjects carry flags (94 isolated-node, 5
strength-IQR), retained rather than deleted; 801 subjects pass. Cohort
selection was frozen before any CIS computation.
*(File: `fig02_population_qc.png|pdf`.)*

**Figure S2. Robustness ladder (9 configurations, n = 150 per
configuration).** Top-50 mean-of-means and Gini across atlases
{4S256, 4S156, Brainnetome246Ext, AAL116}, weights
{sift_invnodevol, radius2_count}, and costs {0.10, 0.20, 0.25}. All 9
configurations reproduce the primary architecture; the maximum like-for-like
top-50-mean deviation is 0.00262 (atlas_AAL116; no numeric tolerance was
pre-registered for E06 — descriptive comparison).
*(File: `fig07_robustness.png|pdf`.)*

**Figure S3. Conceptual schematic.** Two-layer architecture: a dominant
connectivity-dependent component plus a smaller degree-independent residual,
arbitrated by matched controls and degree-preserving nulls. Schematic only;
no data are plotted. *(File: `fig09_conceptual.png|pdf`.)*
