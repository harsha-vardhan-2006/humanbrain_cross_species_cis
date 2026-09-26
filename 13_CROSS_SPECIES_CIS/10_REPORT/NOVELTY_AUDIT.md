# Novelty Audit — Cross-Species Control-Impact Study

*(Spec-alias note 2026-09-26: the external audit spec names this file at
`13_CROSS_SPECIES_CIS/NOVELTY_AUDIT.md`; this report was placed in
`10_REPORT/` — the existing report layer — and a pointer file exists at the
spec path. Content is identical; do not duplicate maintenance.)*

**Date:** 2026-09-26 (post-freeze framing audit; no analysis rerun, no numeric change)
**Basis:** project literature verification (E00, E00a, E17, E17a) + updated
2026-09-26 web sweep (documented in `10_LITERATURE/NOVELTY_MATRIX.md`
§2026-09-26 update) + full-document consistency audit of this repository.
Companion documents: `10_LITERATURE/NOVELTY_MATRIX.md` (comparison matrix),
`CLAIM_EVIDENCE_MATRIX.md` (claim-by-claim evidence table).

---

## 1. Established components (NOT claimed as new)

Every individual analytical component of this study is established in the
literature:

| Component | Established by (examples) |
|---|---|
| Node-removal / lesion-based efficiency analysis of structural connectomes | Alstott et al. 2009 (PLoS Comput Biol, doi:10.1371/journal.pcbi.1000408); Crossley et al. 2014 (Brain 137:2382, doi:10.1093/brain/awu132); Lin et al. 2024 performed degree-ordered removal on the fly connectome (Nature 634:124) |
| Structural-connectome hub / rich-club analysis | van den Heuvel & Sporns 2011 (J Neurosci, rich club); de Reus & van den Heuvel 2013–2014 |
| Degree/strength dependence of node importance | Documented across the hub, rich-club, and controllability literatures; Gu et al. 2015 (Nat Commun 6:8414) explicitly show controllability metrics decouple from degree |
| Degree-preserving null models (Maslov–Sneppen rewiring) | Maslov, Sneppen & Zaliznyak 2002/2004 (Pattern detection in complex networks); standard practice in connectomics; used in fly connectome analyses (e.g., Yadav et al. 2025, Network Neuroscience 9:1299, doi:10.1162/netn.a.26) |
| Network controllability of structural connectomes (NCT) | Gu et al. 2015; Betzel et al. 2016; reviews through 2024–2026 (Wu et al. 2024; Niyazmand et al. 2026) — a different metric family (no node removal), cited as adjacent |
| Population-scale human structural-connectome resources | AOMIC-ID1000 derivative (Zenodo 19796783) and predecessors (HCP, UK Biobank) |
| Cross-species connectome comparison | Venkadesh et al. 2025 (bioRxiv 10.1101/2025.09.07.674762, directed connectomes across mouse/marmoset/macaque/human); olfactory-circuit comparisons across fly species (2025); insect-to-mammalian architectural comparisons |
| FDR / multiple-comparison control, Stouffer combination | Standard statistics |
| Degree-preserving nulls + node-removal in a Drosophila connectome | Yadav et al. 2025 compare larval vs adult Drosophila connectomes with degree-preserving random networks and targeted attack ( Network Neuroscience 9(4):1299–1322) — closest fly-side prior work found in the 2026-09-26 sweep |

## 2. Methodological integration (what is distinctive here)

The distinctive element is **not any single component** but the pre-registered
combination and its arbitration order:

1. exact per-node removal-based control impact (CIS) computed for **all
   nodes in each subject** (not group-average, not sequential attack);
2. population scale: 801 QC-pass / 900 acquired individual human structural
   connectomes;
3. explicit degree/strength-controlled decomposition (degree-matched node
   controls ±10%, plus OLS-style residualization on degree + strength);
4. degree-preserving (Maslov–Sneppen) null-model **arbitration** of both the
   concentration claim and the residual claim, with per-null exact degree
   verification;
5. FDR-controlled per-node residual inference (BH over 456 tests per
   stratum);
6. robustness/rank-stability analysis (9 atlas/weight/cost configurations;
   100 seeded half-splits);
7. a pre-registered cross-scale comparison with the frozen Drosophila
   connectome study under explicit no-homology rules (CP03/CP05,
   APPROXIMATELY_COMPARABLE).

No verified prior study combines these seven elements. The closest works
and the exact overlap boundary are documented in the literature-positioning
table in `10_LITERATURE/NOVELTY_MATRIX.md` and §6 below.

## 3. Human findings (actual, artifact-traced)

All numbers trace to frozen artifacts; independently recomputed 42/42 PASS
(`verify_final_numbers.py`, `FINAL_REPRODUCIBILITY_AUDIT.md`):

- 801 QC-pass subjects of 900 acquired; 456-node 4S456 atlas; 15% cost
  threshold (15,561 edges); exact per-node CIS.
- CIS–degree association: median Spearman ρ = 0.943 (CIS–strength ρ = 0.486).
- Top-50 CIS concentration exceeds degree-preserving null expectations in
  200/200 tested subjects (median z = 16.36; sign p = 1.24e-60) — R1.
- Degree-independent residual > 0 in 778/801 subjects (97.1%; sign
  p = 2.6e-197); Cliff's δ = 0.100 [IQR 0.078–0.129]; median per-subject
  Wilcoxon p = 0.167 (125/801 < .05).
- 43/456 nodes survive BH-FDR q < .05 (max Stouffer z = 23.30) — R2a.
- Human visual share of the population top-50: 2% (obs 1/50).
- System-specific result: pre-registered gate R2b NEGATIVE. The single
  nominal signal (Subcortical/Cerebellar: z_B = 2.08, p = .031, 1.25×) is
  absent at K = 25 (z_B = 0.81) and degree-anchored — **no robust
  canonical-system-specific explanation established**.

## 4. Fly findings (actual, including the rejected hypothesis)

From the frozen fly release (FAFB v783, 139,255 neurons; artifacts
`e10b_final.json`, `e12_strong_results.json`, `e14_v2_summary.json`):

- **The original inhibitory/GABA-specific control hypothesis was NOT
  supported**: the raw matched-pair GABA–ACh effect (δ = 0.111, p = 0.0011)
  did not survive the degree-preserving null ensemble (observed δ = 0.098
  at matched panel size vs null δ = 0.071 ± 0.022; empirical p = 0.109;
  median-difference p = 0.782; z = 1.21). The fly residual δ = 0.0979 is
  itself **not null-surviving**.
- The surviving signal is **visual–centrifugal enrichment after degree
  matching**: 21/50 top chokepoints; 11.7× raw, 2.63× after degree matching
  (z = 5.30, p ≈ 1e-4); consistent at K = 25 (2.47×) and K = 100 (2.15×).
- 13/50 top chokepoints individually exceed their degree-matched peers
  (10 of the 13 visual-system; empirical p < 0.0005–0.01).
- Fly top-50 visual-system fraction: 0.80 (`e14_v2_summary.json`).

## 5. Cross-species finding (two-component architecture)

- Human and fly nervous systems differ by roughly three orders of magnitude
  in analyzed node count (139,255 reconstructed neurons vs 456 parcels) and
  are anatomically non-homologous at the compared resolution.
- Both analyses exhibit the same **qualitative two-component organization**:
  a dominant connectivity/degree-related component plus a smaller
  degree-independent residual (human δ = 0.100; fly δ = 0.0979).
- The anatomical identity of the residual **diverges** (2% visual in human
  vs 80% visual-centrifugal in fly); the R2b system gate was negative in
  human; the fly δ did not survive its own null ensemble.
- Correct summary phrase: **"Architecture replicates; anatomy does not."**
  This is a cross-scale architectural observation, not evidence of
  anatomical homology, not evidence of a conserved biological mechanism,
  and not a universal law. It motivates the hypothesis that a two-component
  control-impact organization (connectivity-dominated + degree-independent
  residual) may recur across nervous systems at very different scales; that
  generalization remains untested beyond two species and two pipelines.

## 6. Literature overlap (closest prior work and distinctions)

See the full literature-positioning table in
`10_LITERATURE/NOVELTY_MATRIX.md`. Closest works, honestly stated:

1. **Kudriavtsev et al. 2026** (bioRxiv 10.64898/2026.05.29.728718) —
   simulated lesions + efficiency + null comparators in ageing (n=144).
   PARTIAL OVERLAP: matched-**mass** lesion nulls (not degree-preserving),
   ageing-decline framing, no per-node population CIS-residual
   architecture, no cross-scale bridge. **Full text still unread
   (4 documented 403 attempts; abstract-complete verification on file)** —
   this is the principal residual novelty risk, carried as a pre-submission
   gate.
2. **Yueh-Hsin (Lin) et al. 2024** (Sci Rep 14:14573, doi:10.1038/s41598-024-64845-4)
   — per-subject GE decline during simulated resections in 80 adults;
   inter-individual patterns; no degree-matched controls, no null ensemble,
   no per-node residual ranking, no cross-scale bridge.
3. **Yadav, Shinde & Singh 2025** (Network Neuroscience 9(4):1299,
   doi:10.1162/netn.a.26) — degree-preserving random networks + targeted
   attack in larval vs adult Drosophila connectomes. Overlaps the
   fly-side tool pair (degree-preserving nulls + node removal) at n=1 per
   stage; no per-subject population framework, no residual decomposition,
   no human population, no pre-registered cross-scale arbitration. **Does
   weaken any claim that "degree-preserving nulls + node removal in a fly
   connectome" is unoccupied** — such a claim was never made; it does not
   occupy the human population-scale combination.
4. **Venkadesh et al. 2025** (bioRxiv 10.1101/2025.09.07.674762) — directed
   cross-species connectomes (mouse/marmoset/macaque/human) with path
   efficiency. Overlaps the cross-species comparative goal; uses no
   node-removal CIS, no null-arbitrated residual decomposition. Supports
   the broader context that cross-species connectome comparison is an
   active field; does not occupy the present combination.
5. **Alstott 2009 / Crossley 2014 / Gu-Betzel NCT / Debona 2026 /
   Treeratana 2026** — as assessed in E00/E17 (classic removal analyses,
   different metric, method adjacency, different question).

None of these papers, individually or in combination, is verified to
combine the seven elements in §2.

## 7. Defensible novelty claim (final recommended wording)

> **To our knowledge, no prior study has combined per-node removal-based
> network-impact analysis, population-scale individual human structural
> connectomes, explicit degree-controlled residualization, degree-preserving
> null-model arbitration, FDR-controlled residual inference, and a
> pre-specified cross-species comparison with the Drosophila connectome in a
> single analytical framework.** The novelty therefore lies primarily in
> the integration of these analyses and the resulting cross-scale empirical
> comparison, rather than in any individual analytical component.

This wording is (a) hedged ("to our knowledge"), (b) bounded to the
combination, (c) consistent with every verified source on file, and (d)
carries the documented Kudriavtsev full-text condition.

## 8. Claims explicitly NOT supported (must not appear)

- that node-removal CIS was invented here (it was not; Alstott 2009,
  Crossley 2014, Lin 2024);
- that degree-preserving null models are new (Maslov–Sneppen; standard);
- that brain hubs are newly discovered (rich-club literature);
- that network controllability is new (Gu 2015; Betzel 2016);
- that cross-species connectomics is new (Venkadesh 2025 and earlier);
- that nobody has ever studied degree effects (the degree–importance
  coupling is the best-established fact in this literature);
- "first ever" / "first in the world" (not established by the audit);
- discovery of a new biological mechanism (no mechanism is demonstrated);
- a universal law or "proof" of scale-invariant organization (two species,
  two pipelines; the residual's fly counterpart is not null-surviving);
- anatomical homology between fly and human findings (explicitly excluded
  by the comparability rules CP03/CP05);
- a robust canonical-system-specific explanation of the human residual
  (R2b was negative).

## 9. Remaining uncertainty (what the literature audit cannot exclude)

1. **Kudriavtsev et al. 2026 full text** — **RESOLVED 2026-09-26:** the
   complete Results and Discussion were verified via a text-extraction
   proxy (direct bioRxiv access remains network-blocked; see the addendum
   in `10_LITERATURE/KUDRIAVTSEV_2026_FULLTEXT_REVIEW.md`). The full text
   confirms: edge-level hotspot lesions (not per-node removal), matched-mass
   nulls (not degree-preserving), no degree-matched controls, no
   cross-scale bridge. The closest-neighbour assessment no longer rests on
   abstract-only verification.
2. **Coverage of the 2025–2026 preprint stream is incomplete by nature:**
   the sweep covered bioRxiv/arXiv/journal-index queries on 2026-09-22,
   09-24, and 09-26; a dedicated pre-submission re-sweep at submission
   date is recommended.
3. **Gray literature / non-indexed venues** (theses, workshop papers,
   non-English publications) were not systematically covered.
4. The exact phrase-level combination could exist in a paper whose
   abstract/index terms do not surface under the queries used
   (vocabulary mismatch risk).

## 10. Recommended manuscript wording (publication-ready)

**Contribution and Novelty (§, manuscript):**

> **A. Established methods.** Node-removal efficiency analysis of structural
> connectomes (Alstott 2009; Crossley 2014), hub and rich-club analysis
> (van den Heuvel & Sporns 2011), degree-preserving null models
> (Maslov–Sneppen), network controllability (Gu 2015; Betzel 2016), and
> cross-species connectome comparison (Venkadesh 2025) are each established.
>
> **B. Methodological integration.** To our knowledge, no prior study has
> combined per-node removal-based network-impact analysis, population-scale
> individual human structural connectomes, explicit degree-controlled
> residualization, degree-preserving null-model arbitration, FDR-controlled
> residual inference, and a pre-specified cross-species comparison with the
> Drosophila connectome in a single analytical framework. The novelty lies
> primarily in this integration and its pre-registered arbitration order,
> not in any individual component.
>
> **C. New empirical findings.** (i) Top-50 control-impact concentration
> exceeds degree-preserving null expectations in 200/200 subjects;
> (ii) a small degree-independent residual is detectable in 778/801
> subjects (δ = 0.100) with 43/456 nodes surviving FDR; (iii) the residual
> is not robustly system-specific (pre-registered gate negative).
>
> **D. Cross-species interpretation.** A qualitatively similar two-component
> organization — dominant connectivity-dependent component plus smaller
> degree-independent residual — appears in both the human and Drosophila
> analyses despite ~10³-fold differences in analyzed node count and
> non-homologous anatomy. These results motivate the hypothesis that
> two-component control-impact organization recurs across scales; they do
> not establish anatomical homology, a conserved mechanism, or a universal
> law.
>
> **E. Limitations of the novelty claim.** The claim is bounded by a
> documented literature audit (E00/E17/E17a + 2026-09-26 updates). The
> closest neighbour (Kudriavtsev et al. 2026) has been full-text verified
> (via proxy extraction) as PARTIAL OVERLAP with none of the four decisive
> components present. The audit cannot exclude occupation of the
> combination in sources not surfaced by the queries used.

---
*This audit was prepared by Buffy (Codebuff agent) from verified in-repo
artifacts and primary-source literature records. It preserves all negative
findings (fly GABA hypothesis rejection; human R2b negative) and changes no
numeric result.*
