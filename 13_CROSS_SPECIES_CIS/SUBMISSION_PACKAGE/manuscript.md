# MANUSCRIPT FINAL — v2.0 (submission structure; results identical to frozen v1.0)

> **Provenance:** every number in this document was recomputed from frozen
> artifacts on 2026-09-26 (`10_REPORT/verify_final_numbers.py`, 42/42 PASS).
> This edition restructures presentation per the submission checklist; **no
> scientific conclusion or value differs from MANUSCRIPT_DRAFT.md v1.0 / RESOLUTION.md.**
> Interpretation guardrails are quoted verbatim from HYPOTHESIS_RESULT_MATRIX.md.

---

## Title

**Control-impact architecture of the human structural connectome: degree
dominance, a small near-universal residual, and a cross-scale architectural
comparison with the fly connectome**

## Abstract

**Background.** Network communication in brain connectomes is dominated by
node degree, but whether any degree-independent component of node-level
control impact exists — and whether it is anatomically structured — remains
unresolved, because most node-removal analyses are group-average, lack
matched controls, and lack null-model arbitration.
**Gap.** No prior study, to our knowledge, has combined exact per-node
removal-based control impact with per-subject population-scale statistics,
degree/strength matching, degree-preserving null ensembles, and a
pre-registered cross-scale comparison.
**Data and methods.** We computed the exact Control Impact Score, CIS(i) =
(E(G) − E(G−i))/E(G), for all 456 nodes in each of 801 QC-pass subjects from
the AOMIC-ID1000 structural-connectome resource (N = 900 acquired; 456-node
4S456 parcellation; SIFT streamline counts; 15% proportional threshold), with
degree-matched controls (±10%), 100 degree-preserving (Maslov–Sneppen) nulls
per graph in two batteries (100 × 100 full-CIS; 200 × 100 top-50), BH-FDR
node-level inference, system-enrichment tests with two control levels, and a
9-configuration robustness ladder.
**Main human result.** Top-50 CIS concentration exceeded its degree-preserving
null in 200/200 subjects (median z = 16.36; two-sided sign p = 1.24 × 10⁻⁶⁰).
CIS was strongly degree-related (median ρ = 0.943). A small degree-independent
residual was present in 778/801 subjects (sign p = 2.6 × 10⁻¹⁹⁷; Cliff's
δ = 0.100; median Wilcoxon p = 0.167) and 43/456 nodes survived FDR
(q < .05; max Stouffer z = 23.3).
**Cross-scale result.** Compared with the frozen fly (FAFB v783) study —
Cliff's δ = 0.0979, itself not surviving its degree-preserving null ensemble —
the human architecture is concordant in effect size and degree dominance.
**Anatomical divergence.** The residual's anatomical identity differs: visual
systems hold 2% of the human top 50 versus 80% visual-centrifugal in the fly;
the single nominal human system signal (subcortical/cerebellar, z_B = 2.08,
p = .031, 1.25×) is absent at K = 25 and degree-anchored, and the pre-registered
system-enrichment gate (R2b) was **negative**.
**Interpretation.** Control-impact architecture — a dominant degree component
plus a small, near-universal degree-independent residual — shows cross-scale
architectural similarity while the residual's anatomical identity diverges.
No new biological mechanism, no homology, and no system-specific claim is made.

## 1. Introduction

- **Established knowledge.** Node-removal/efficiency analysis in human
  structural connectomes is classic (Alstott et al. 2009; Crossley et al.
  2014). Degree is the dominant correlate of node importance (ρ ≈ 0.9 here).
- **Unresolved problem.** Whether a degree-independent component of control
  impact exists at the single-subject level, is reproducible across a
  population, and is anatomically structured — prior group-average designs
  cannot answer this.
- **Degree confounding.** Raw comparisons of node importance are
  degree-confounded; matched controls and degree-preserving nulls are both
  required (the fly study's decisive lesson, re-confirmed here).
- **Literature gap.** The four-way combination (per-node CIS + per-subject +
  population scale + degree-preserving null arbitration) is unoccupied
  (NOVELTY_MATRIX.md).
- **Purpose and hypotheses.** H1: concentration exceeds degree-preserving
  null expectations. H2: a degree-independent residual remains after
  degree/strength adjustment. H3: the residual is robustly system-specific.
  H4: comparable architecture appears across fly and human scales.
  Pre-registered in PROTOCOL_FREEZE.md before any computation.

## 2. Methods

Condensed; full frozen detail in ANALYSIS_FREEZE.md and supplementary.

- **Dataset and QC.** AOMIC-ID1000 derivatives (Zenodo 19796783, CC-BY-4.0);
  900 subjects × 7 atlases extracted and verified (25,200 matrices; 0 NaN/Inf/
  asymmetry); QC cohort 801/900 (frozen CIS-blind; flags retained, never
  deleted).
- **Primary configuration.** 4S456Parcels; `sift_radius2_count_connectivity`;
  15% proportional threshold (k = 15,561 edges).
- **CIS.** Exact per-node CIS = (E(G) − E(G−i))/E(G); 456 exact leave-one-out
  recomputations per subject; reference implementation validated to 6.1e-16;
  fast estimator (null graphs only) to 4e-16 under a mandatory 1e-9 gate.
- **Matching.** ±10% total degree, 1:1 greedy, nearest-50 fallback (flagged).
- **Null batteries.** Maslov–Sneppen undirected rewiring preserving the exact
  per-node degree sequence (verified per null, 10,000/10,000 exact, 0
  self-loops); seeds 100+i; subject samples nested, seed 20260922.
- **Statistics.** Per-node empirical p (add-one) → Stouffer → BH-FDR (q=.05);
  battery B z + sign test; enrichment controls A/B (10,000 perms);
  rank stability (100 half-splits); effect sizes Cliff's δ.
- **Cross-scale discipline.** Normalized comparators only (DIRECT/
  NORMALIZED/QUALITATIVE tags); no homology claims (CP03/CP05).

## 3. Results

*(order per submission checklist)*

1. **Data/QC.** 900 acquired, 801 pass; E0 median 0.5468 [0.5441–0.5497];
   mean degree 68.2; 15,561 edges.
2. **CIS distribution.** Max population-mean CIS 0.00462 (node 414;
   `e03_summary.json` cis_mean_pop_max = 0.0046246); top-50 rate 1.00 for
   node 400; small magnitudes at 15% cost as expected for a redundant
   68-degree-mean graph. *[Value corrected 2026-09-26 from "0.00463" — a
   rounding slip; the frozen artifact gives 0.0046246 → 0.00462 at 3 s.f.]*
3. **Degree relationship.** Median ρ(CIS, degree) = 0.943; CIS vs strength
   ρ = 0.486.
4. **Degree-preserving null test (H1).** 200/200 subjects above null;
   median z = 16.36; sign p = 1.24e-60; 100% of subjects at the 1/101
   empirical-p floor (inference via z + sign test).
5. **Residual analysis (H2).** 778/801 subjects positive (sign p = 2.6e-197);
   δ = 0.100 [0.078–0.129]; 36,846 matched pairs; 58.8% of comparisons beat
   controls; Wilcoxon median p = 0.167 (125/801 < .05) — small but
   directionally near-universal.
6. **FDR node characterization (R2a).** 43/456 nodes q<.05; max z = 23.30
   (node 400); cluster spans nodes 400–451.
7. **System/enrichment (H3/R2b).** Pre-registered gate NEGATIVE: Vis obs 1
   (2%), z_B = −0.38; only Subcortical/Cerebellar nominal (obs 26, z_A 9.06,
   z_B 2.08, p .031, 1.25×), absent at K = 25 (z_B 0.81) — degree-anchored.
8. **Robustness.** 9 configurations within 0.0026 of primary top-50 mean;
   rank stability median Spearman 0.996.
9. **Cross-species comparison (H4).** δ 0.100 (human) vs 0.0979 (fly);
   both degree-dominated; human visual share 2% vs fly 80% visual-centrifugal
   — architecture replicates; anatomy does not.

## 4. Discussion

1. **Principal findings.** Degree-dominated control impact with a small,
   near-universal degree-independent residual; topological concentration
   exceeds degree-preserving nulls in every tested subject.
2. **Degree-dominated architecture.** ρ ≈ 0.94 replicates the known
   degree–importance coupling at population scale, now with per-subject
   resolution.
3. **Degree-independent residual.** Small (δ = 0.100), directionally
   near-universal (778/801), and measurable above the CIS noise floor only
   through matched controls plus null arbitration.
4. **Population-level concentration.** The 200/200 result with z ≈ 16 shows
   concentration is a stable property of individual connectomes, not a
   group-average artifact.
5. **Cross-scale comparison.** Same effect-size statistic, same sign, same
   degree-anchored interpretation across a roughly 10³-fold node-count
   difference (139,255 reconstructed neurons vs 456 parcels).
6. **Architecture replicates but anatomy diverges.** Fly: visual-centrifugal
   residual (80% of top 50). Human: not visual (2%); nominal subcortical/
   cerebellar signal is degree-anchored and K-ladder-fragile. **R2b was
   negative**; the present data do not establish that the mechanism
   selecting residual chokepoints is conserved (nor that it is not).
7. **Relationship to previous literature.** Alstott/Crossley: classic
   removal analysis, group-average, no matched controls or nulls.
   Kudriavtsev 2026: closest neighbour (lesions + nulls) but matched-mass
   nulls and ageing framing — PARTIAL OVERLAP (10_LITERATURE/). NCT
   literature: different metric. Yueh-Hsin 2024: resection simulations,
   no matching/nulls.
8. **Biological interpretation.** None beyond architecture: no new mechanism
   is claimed; no homology is claimed; the subcortical localization is
   degree-anchored; the fly–human δ similarity is interesting but partly
   fortuitous (different units, graphs, designs; fly δ not null-surviving).
9. **Methodological implications.** Individual methods are established; the
   contribution is the bounded combination and its arbitration. Matched-pair
   significance without null arbitration can mislead — both layers of control
   are necessary (fly E10B lesson, replicated).
10. **Limitations.** Undirected graphs (directed variant impossible in these
    derivatives); no homology; single pipeline/acquisition; residual near the
    CIS noise floor (hence null arbitration); battery-B per-subject p-values
    at the 1/101 null-resolution floor (inference via z + sign test);
    subcortical residual not robust across the K ladder; Kudriavtsev 2026
    full text verified via proxy extraction (direct access blocked);
    ENVIRONMENT_MANIFEST
    provenance gap disclosed.
11. **Future work.** Directed human connectomes; multi-shell/higher-quality
    tractography; replication in BANC/larval connectomes and independent
    human cohorts; test of the two-component architectural hypothesis
    beyond two species.

## 5. Contribution and Novelty

**A. Established methods.** Node-removal/efficiency analysis of structural
connectomes (Alstott 2009; Crossley 2014; degree-ordered removal on the fly
connectome, Lin 2024), hub/rich-club analysis (van den Heuvel & Sporns
2011), degree-preserving null models (Maslov–Sneppen), network
controllability (Gu 2015; Betzel 2016), and cross-species connectome
comparison (Venkadesh 2025; larval–adult Drosophila null + attack analyses,
Yadav 2025) are each established.

**B. Methodological integration.** To our knowledge, no prior study has
combined per-node removal-based network-impact analysis, population-scale
individual human structural connectomes, explicit degree-controlled
residualization, degree-preserving null-model arbitration, FDR-controlled
residual inference, and a pre-specified cross-species comparison with the
Drosophila connectome in a single analytical framework. The novelty
therefore lies primarily in the integration of these analyses and the
resulting cross-scale empirical comparison, rather than in any individual
analytical component.

**C. New empirical findings.** (i) Top-50 CIS concentration exceeds
degree-preserving null expectations in 200/200 tested subjects; (ii) a
small degree-independent residual is detectable in 778/801 subjects
(δ = 0.100) with 43/456 nodes surviving FDR; (iii) the residual is not
robustly system-specific (pre-registered gate negative).

**D. Cross-species interpretation.** A qualitatively similar two-component
organization — a dominant connectivity-dependent component plus a smaller
degree-independent residual — appears in both the human and Drosophila
analyses despite roughly three orders of magnitude difference in analyzed
node count and non-homologous anatomy. These results motivate the
hypothesis that two-component control-impact organization recurs across
nervous systems of very different scale; they do not establish anatomical
homology, a conserved biological mechanism, or a universal law.

**E. Limitations of the novelty claim.** The claim is bounded by the
documented literature audit (`10_LITERATURE/NOVELTY_MATRIX.md`; E00/E17/
E17a plus the 2026-09-26 updates). The closest neighbour (Kudriavtsev et
al. 2026) has been full-text verified via proxy extraction as PARTIAL
OVERLAP, with none of the four decisive components present (no per-node
removal ranking, no degree-matched controls, no degree-preserving nulls,
no cross-scale bridge). The audit cannot exclude occupation of the
combination in sources not surfaced by the queries used. Full audit:
`10_REPORT/NOVELTY_AUDIT.md`.

## 6. Data and code availability

Data: AOMIC-ID1000 (Zenodo 19796783, CC-BY-4.0). Fly reference: frozen
release v1.0.0 artifacts (read-only). All human-side code, manifests,
validation reports, and append-only logs in
`github.com/harsha-vardhan-2006/humanbrain_cross_species_cis`; every number
traces to an artifact (`FINAL_REPRODUCIBILITY_AUDIT.md`).
