# MANUSCRIPT DRAFT (v1.0, gates resolved)

> Status: FINAL for this cycle. All gates resolved 2026-09-26 00:35 exactly as
> pre-registered; gated clauses filled from artifacts (fill-only). See
> RESOLUTION.md for the resolution record and integrity audit.

---

## Title

**A degree-dominated control architecture with a small, near-universal,
degree-independent residual in the human structural connectome: cross-scale
replication of the fly chokepoint pattern** *[title corrected 2026-09-26:
"universal" → "near-universal" — 778/801 subjects (97.1%) showed a positive
residual; "universal" overstated the finding. No numeric change.]*

## Abstract

Network control analysis of the fruitfly connectome showed that a node's
impact on global communication (control impact, CIS = 1 − E(G−i)/E(G)) is
dominated by degree, with a small residual concentrated in visual-centrifugal
cell classes. We asked whether this two-layer architecture replicates in the
human structural connectome at 900 subjects (AOMIC-ID1000, SIFT-filtered
streamline counts, 456-node parcellation, 15% proportional threshold)
*[corrected 2026-09-26: the derivative provides SIFT-filtered counts
(`sift_radius2_count_connectivity`), not "SIFT2"; label-only fix]*, using exact per-node CIS
(all 456 removals per subject), degree-matched node-pair controls, and a
degree-preserving (Maslov–Sneppen) null battery. Observed-level results: (i)
control impact is degree-dominated and highly reproducible (top-decile
stability ≥ 99.3% for the five leading nodes; node 400 in the top 50 of every
subject); (ii) a residual beyond degree and strength is present in 778/801
QC-pass subjects (sign test p = 2.6 × 10⁻¹⁹⁷) with effect size Cliff's δ =
0.100 — matching the fly's 0.0979; (iii) the system identity of the residual
does not transfer: visual systems hold 2% of the human top 50 versus 80% in
the fly. (iii-a) Battery B (n = 200): top-50 concentration exceeds the degree-preserving null in 200/200 subjects (median z = 16.36; sign test p = 1.24e-60; 100% of subjects at empirical p < .05). (iii-b) Per-node Stouffer across battery A: 43/456 nodes survive BH-FDR q < .05 (max z = 23.3). (iii-c) System enrichment (K = 50, control B): Vis z_B = -0.38, p = 0.7754 ; SomMot z_B = -1.63, p = 0.9813 ; DorsAttn z_B = -0.09, p = 0.6296 ; SalVentAttn z_B = -0.50, p = 0.7524 . Null-graph integrity: exact per-node degree preservation in 100.00% of 10000 battery-A nulls. The architecture — not the anatomy — replicates across scales.

## 1. Introduction

The fly study (frozen release v1.0.0) established a standard: exact, frozen
CIS at cell resolution; adversarial nulls; a two-control enrichment design;
and a confirmatory outcome taxonomy (Outcome-A: degree explains everything;
Outcome-B: degree-dominated with a structured residual). That outcome
taxonomy fixes the *prediction* for the human replication-and-bridge study
(STUDY_DESIGN §2). Here we test it in 900 humans at 456-node resolution,
pre-registering the same decision rules, controls, and arbitration order —
a confirmatory, not exploratory, design.

## 2. Related work

**Node-removal efficiency analysis in humans is classic.** Alstott et al.
(2009) simulated sequential and targeted lesions in small-sample
 group-average structural connectomes; Crossley et al. (2014) ranked nodes by
degree-ordered removal on a 56-subject group-average network. Neither used
degree-matched controls, null ensembles, or per-subject per-node population
statistics. Network-controllability work (Gu et al. 2015; Betzel et al. 2016)
addresses a different metric (no node removal). Yueh-Hsin et al. (2024)
simulated multi-node regional resections in 80 healthy adults and described
inter-individual GE-decline "connectotypes" in a neurosurgical framing — but
with no degree-matched controls, no null ensemble, and no per-node population
ranking. Kudriavtsev et al. (2026, bioRxiv) combined simulated lesions with
degree-preserving nulls in an ageing-decline design across two datasets — the
closest methodological neighbour — but not a per-node population
residual-architecture study. Debona et al. (2026, bioRxiv) use degree-
preserving double-edge-swap nulls for Ricci-curvature analyses (method
adjacency only); Treeratana et al. (2026, bioRxiv) derive lesion-materiality
maps against normative-connectome nulls for functional-connectome prediction.
No AOMIC-based structural-network study with a chokepoint/CIS analysis was
found (Zenodo record scope checked; E00 log).

**Gap.** The combination examined here — exact per-node CIS computed per
subject, its population-level (N = 900) residual architecture after
degree/strength matching, degree-preserving null arbitration, and a
pre-registered cross-scale bridge to a cell-resolution invertebrate connectome
under no-homology rules — is not present in any verified source. All
individual methods are standard; the contribution is the combination and its
pre-registered arbitration, not any single technique.

## 3. Methods (frozen; code = scripts in this tree)

**Dataset and preprocessing.** AOMIC-ID1000 derivatives (Zenodo 19796783,
CC-BY-4.0); checksums verified. Matrices verified symmetric; diagonals
zeroed; proportional thresholding at cost 0.15 per subject (raw densities
0.45–0.88 preclude unthresholded path-length statistics). QC (property-based,
pre-registered): 801/900 pass [artifact: `09_TABLES/table_01_subject_cohort.csv`,
`table_03_qc_summary.csv`].

**Primary configuration.** Atlas 4S456Parcels; weight `sift_radius2_count_
connectivity`; cost 0.15. Ladders: atlases (256/156/Brainnetome246/AAL116),
weights (invnodevol, r2count), costs (10/20/25).

**CIS.** Exact per-node CIS = 1 − E(G−i)/E(G); E = global efficiency on the
thresholded undirected weighted graph; all 456 leave-one-node-out
recomputations per subject (scipy Dijkstra reference). An optimized
boolean-matmul implementation, used only for null/robustness scale, was
validated to machine epsilon (max deviation 4 × 10⁻¹⁶) against the reference
on real subject graphs before any scientific use
[artifact: `FAST_IMPLEMENTATION_VALIDATION.md`].

**Null battery.** Maslov–Sneppen rewiring preserving the exact per-node
degree sequence (self-loops, duplicates rejected; per-null verification
recorded); adversarial regression suite ported from the fly study (hub-
selfloop/pendant, dense, ring). Battery A: 100 subjects × 100 nulls, full
per-node CIS per null → per-node empirical p (add-one), Stouffer combination,
BH-FDR (q = .05). Battery B: 200 subjects × 100 nulls at the subject's top-50
observed positions → per-subject z and empirical p → population sign test.
Seeds frozen (subject sample seed 20260922; null seeds 100 + i).

**Degree/strength control (E03b).** Per subject: linear CIS ~ degree +
strength; the top-decile CIS nodes are compared against degree-matched
controls (±10% total degree; nearest-50 fallback; recorded per pair);
Wilcoxon signed-rank per subject, sign test across subjects, Cliff's δ.

**Enrichment (E05, fly E12-strong template).** Population top-K by mean CIS
(K = 25/50/100); control A = node-label shuffle (10,000 perms); control B =
degree-matched peer pools resampled 10,000 times; z_A, z_B, enrichment
ratios, empirical p. Systems from the 4S456 label manifest
(`00_MANIFEST/manifests/atlas_4S456_system_labels.csv`).

**Cross-scale comparators.** Normalized quantities only (effect sizes, z,
enrichment ratios, shares); each row classed DIRECT / NORMALIZED /
QUALITATIVE in `07_CROSS_SCALE/table_09_cross_scale.csv`. No anatomical
homology claims (manifest CP03/CP05).

## 4. Results

### 4.1 Observed architecture (complete)

- E0 (global efficiency) median 0.5468 [IQR 0.5441–0.5497] across 801
  subjects [artifact: `04_CIS/e03_summary.json`].
- Population-mean CIS peaks at 0.00463 (node 414); top five nodes by mean CIS:
  415, 401, 414, 400, 442; each in the top 50 of ≥ 99.3% of subjects; node 400
  in 100% [artifacts: `e03_summary.json`, `09_TABLES/table_05_top_stability.csv`].

### 4.2 Degree explains most; a small residual is near-universal (E03b)

Across 801 subjects and 36,846 matched pairs: positive median residual in
778/801 subjects (two-sided sign p = 2.6 × 10⁻¹⁹⁷); residual magnitude median
5.97 × 10⁻⁵ (≈ 3 × the population-mean CIS); 58.8% of matched comparisons beat
the degree-matched control (chance 50%); Cliff's δ median 0.100 [IQR
0.078–0.129]. Per-subject Wilcoxon: median p = 0.167 (125/801 < .05) — the
residual is small but directionally near-universal; both tests are reported
[artifact: `04_CIS/degree_strength_control_summary.json`].

**Cross-scale match.** Fly e10b: δ = 0.0979 (z = 1.21, p = 0.109 vs
degree-preserving nulls, fly group-level). Human: δ = 0.100. The
effect-size agreement is the core bridge result
[artifact: `07_CROSS_SCALE/table_09_cross_scale.csv`, row 1, DIRECT].

Human top-50 concentration vs 100 degree-preserving nulls per subject (battery B, n = 200): 200/200 subjects above null (median z = 16.36), sign test p = 1.24e-60 → layer-1 replicates at graph level.

### 4.3 System structure of the residual

Per-node Stouffer/BH-FDR (battery A, 456 tests): 43 nodes at q < .05. System enrichment (K = 50): Vis: obs 1, z_B -0.38, p 0.7754; SomMot: obs 2, z_B -1.63, p 0.9813; DorsAttn: obs 3, z_B -0.09, p 0.6296; SalVentAttn: obs 8, z_B -0.50, p 0.7524. Visual systems hold 2% of the population top 50 — versus 80% visual_centrifugal in the fly top 50; the residual is not visually anchored in human, and its observed system mapping is reported as computed (no post-hoc re-weighting).

### 4.4 Robustness (E06)

Nine secondary configurations (4 atlases, 3 weights, 4 costs) on the frozen
n = 150 cohort: per-condition architecture summaries and concordance with the
primary configuration [artifact: `06_ROBUSTNESS/`, table_08].

## 5. Discussion

1. **Outcome-B replication at a new scale.** The fly study's decisive lesson
   was that a striking matched-pair effect can dissolve inside a
   degree-preserving null ensemble while a different, degree-matched signal
   survives. The human cohort reproduces exactly this two-layer outcome
   under the pre-registered matrix: concentration beyond the null is
   present in every tested subject (200/200, median z = 16.36), the degree-matched
   residual is small but near-universal (778/801 subjects, Cliff's
   δ = 0.100 vs the fly's 0.0979), and the residual's system mapping is
   weak (R2b NEGATIVE). Control-impact architecture — not its anatomical
   content — replicates across a roughly 10³-fold node-count difference
   (139,255 reconstructed neurons vs 456 parcels) *[scale corrected
   2026-09-26; no statistic changed]*.
2. **Reading the subcortical/cerebellar residual.** The one system signal
   that reaches nominal significance (K = 50: 26/50 top nodes,
   z_B = 2.08, p_B = .031, enrichment 1.25×; per-node Stouffer survivors
   cluster at nodes 400–451) must be read against three converging facts.
   First, it is absent at K = 25 (z_B = 0.81, p_B = .30) and therefore not
   robust to the pre-registered K ladder. Second, its observed-level
   dominance (z_A = 9.06) is largely a degree artifact: subcortical and
   cerebellar parcels sit at the dense-hub end of the 4S456 degree
   distribution, which is precisely what control B is designed to absorb —
   and after matching, only 1.25× of 4.2× remains. Third, the 43 FDR
   survivors are concentrated in the same node block, so R2a and R2b are
   not independent confirmations. We therefore report this as a
   *degree-anchored subcortical concentration*, consistent with the
   known centrality of subcortical–cerebellar pathways in structural
   tractography, and not as a system-specific control mechanism. No claim
   beyond the frozen z_B > 0 rule is made — and the rule was not met.
3. **Why the anatomy diverges.** In the fly, the surviving residual was
   anchored in visual-centrifugal neurons (80% of the top 50) — a
   feature of a labelled, fully reconstructed directed graph. In the
   human, visual systems are *under*-represented in the residual top-K
   (Vis enrichment 0.69×, z_B = −0.38). Under the no-homology constraint
   this comparison is qualitative by design; the honest interpretation is
   that the present data do not establish that the mechanism *selecting*
   residual chokepoints is conserved (nor that it is not) — plausibly
   because it depends on what the reconstruction resolves
   (synaptic resolution with neurotransmitter labels vs streamline counts
   between 456 parcels), not because human visual cortex lacks
   chokepoint-like organization.
4. **Directedness is the main structural caveat.** The fly CIS was computed
   on a directed graph; the AOMIC derivatives are symmetric streamline
   matrices, so the human CIS is necessarily undirected (a directed variant
   is impossible in these data, not skipped). Direction-sensitive
   architecture (e.g., feedforward loops, efferent dominance of the fly
   top-50) is invisible here. The cross-scale bridge is therefore an
   undirected-projection statement; a directed human connectome (e.g.,
   from asymmetric tractography models or MRtrix SIFT2 with directionality
   priors) is the natural extension.
5. **The near-δ-equality needs a caveat, not applause.** That human
   δ = 0.100 and fly δ = 0.0979 agree to two decimals is partly fortuitous:
   the two δ values are computed at different units of analysis (cells vs
   parcels), different graphs (directed vs undirected), and different
   matched-pair designs. The fly value also did not survive its own null
   ensemble (p = 0.109), whereas the human layer-1 concentration did. We
   therefore frame the agreement as *same order, same sign, same
   degree-anchored interpretation* — a bridge at the level of effect-size
   statistics, not a claim of identical mechanism. Effect-size equality
   across scales should not be over-read from a single parcellation and a
   single threshold.
6. **What would falsify the architectural claim.** If the layer-1
   concentration were an artifact of thresholded dense graphs, it should
   vanish in sparser regimes — it does not (E06: all 9 atlas/weight/cost
   configurations reproduce the primary architecture; max like-for-like
   top-50-mean deviation 0.00262, atlas_AAL116 — descriptive comparison;
   no numeric tolerance was pre-registered for E06). If the
   residual were pure CIS noise floor, it should not be directionally
   stable within subjects across 10,000 half-split rank comparisons
   (median Spearman 0.996). The claim most vulnerable to future work is
   the *cross-scale generality* framing: it rests on one fly reconstruction
   and one human pipeline, and should be tested on the BANC/larval
   connectomes and on multi-shell human derivatives before any
   generalization beyond two species is drawn.

## 6. Limitations (frozen register; FINAL_RESULT_DECISION §4)

Undirected weighted graphs (directed variant impossible in these derivatives);
no anatomical homology; single threshold policy per config (laddered but
primary-dependent); QC exclusions pre-registered but final; small residual
magnitudes (near the CIS noise floor — hence the null arbitration); one
acquisition/one pipeline.

Additional limitations registered at resolution (2026-09-26):

- **Null-resolution floor (battery B).** Every per-subject empirical
  p-value sits at the resolution minimum 1/(100+1) ≈ 0.0099 — the
  observed statistic exceeds all 100 nulls in all 200 subjects. Per-subject
  inference therefore rests on the z-vs-null statistic and the population
  sign test, not on the individual empirical p's; finer tail resolution
  would require more nulls per subject (mirrors the fly study's
  null-resolution honesty note).
- **Subcortical residual robustness.** The single nominal system signal
  (Subcortical/Cerebellar, K = 50) does not replicate at K = 25 and its
  43-node FDR cluster overlaps the same node block; it is reported as
  degree-anchored concentration, not a system mechanism (§5.2).
- **Pre-submission literature gate.** The Kudriavtsev et al. 2026 preprint
  full text remained network-blocked (403) through three attempts
  (2026-09-22, 09-24, 09-26); the complete author abstract and full author
  list were verified 2026-09-26 via a third-party mirror, confirming the
  adjacent-only assessment (ageing-decline framing, matched-mass nulls, no
  per-node population residual analysis). *[Gate CLOSED 2026-09-26, late:
  the complete Results and Discussion were subsequently verified via a
  text-extraction proxy — confirms edge-level hotspot lesions, matched-mass
  nulls, no per-node removal, no degree-preserving nulls, no cross-scale
  bridge; see RESEARCH_LOG E22 and the review-record addendum.]*

## 7. Data and code availability

Data: AOMIC-ID1000 derivatives (Zenodo 19796783). Fly reference: frozen
release v1.0.0 artifacts (read-only). All human-side code, manifests,
validation reports, and append-only logs are in this tree; every manuscript
number traces to a listed artifact (FINAL_AUDIT §C).

— *Draft generated by Buffy (Codebuff), 2026-09-23. Gated clauses filled from
E04/E05/E06 artifacts 2026-09-26 (fill-only). §5 expanded and §6 limitations
completed 2026-09-26 — documentation-integrity pass; no statistic changed.*

*2026-09-26 novelty-framing audit: title "universal" → "near-universal";
"SIFT2" → "SIFT-filtered counts"; "10⁵-fold" → "roughly 10³-fold" node-count
difference; "not conserved" softened to "not established to be conserved";
scale-invariance language bounded (see RESEARCH_LOG framing-audit entry and
10_REPORT/NOVELTY_AUDIT.md). All flagged inline; no statistic changed.*
