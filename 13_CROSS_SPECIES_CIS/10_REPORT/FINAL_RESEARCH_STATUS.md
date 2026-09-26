# FINAL RESEARCH STATUS — Cross-Species Control-Impact Study
**Date:** 2026-09-26 · **Status: ANALYSIS FROZEN, AUDIT PASSED, SUBMISSION PACKAGE READY**

## 1. Project objective
Determine whether the control-impact architecture documented in the frozen fly
connectome study (FAFB v783, 139,255 neurons) — a dominant degree component
plus a small degree-independent residual — has a measurable analog in the
human structural connectome, at population scale, under degree-preserving
null arbitration, under explicit no-homology rules.

## 2. Dataset
AOMIC-ID1000 structural-connectome derivative (Zenodo 19796783, CC-BY-4.0):
900 subjects × 7 atlases × 4 variants, checksum-verified. Primary:
4S456Parcels (456 nodes) × `sift_radius2_count_connectivity` × 15% cost.
Cohort: 801 QC-pass (frozen CIS-blind; flags retained, never deleted).

## 3. Methods
Exact per-node CIS (validated to machine precision); degree-matched controls
(±10%, 1:1, nearest-50 fallback); Maslov–Sneppen degree-preserving nulls
(exact per-null verification, 10,000/10,000); Stouffer + BH-FDR node
inference; two-level system enrichment; 9-config robustness ladder; frozen
seeds. Full detail: `10_REPORT/ANALYSIS_FREEZE.md`.

## 4. Main findings (all artifact-traced; 46/46 audit checks PASS)
- **H1 SUPPORTED:** top-50 CIS concentration exceeds degree-preserving nulls
  in 200/200 subjects (median z = 16.36; sign p = 1.24e-60).
- **H2 SUPPORTED:** degree-independent residual in 778/801 subjects
  (sign p = 2.6e-197; Cliff's δ = 0.100 [0.078–0.129]); 43/456 nodes survive
  BH-FDR q<.05 (max Stouffer z = 23.30); ρ(CIS, degree) median 0.943.
- Rank stability 0.996; E06: 9 configs reproduce the primary architecture
  (max like-for-like top-50-mean deviation 0.00262, atlas_AAL116; no
  numeric tolerance was pre-registered for E06 — descriptive comparison).

## 5. Negative findings
- **H3 NOT SUPPORTED (R2b NEGATIVE):** residual is not robustly
  system-specific. Visual systems: obs 1/50 (2%), z_B = −0.38. The single
  nominal signal (Subcortical/Cerebellar: obs 26, z_B = 2.08, p = .031,
  1.25×) is absent at K = 25 (z_B = 0.81) and degree-anchored.
- Per-subject Wilcoxon median p = 0.167: the residual is directionally
  near-universal but individually small — reported, not hidden.

## 6. Cross-species findings
Architecture replicates; anatomy does not. Human δ = 0.100 vs fly
δ = 0.0979 (fly δ itself NOT null-surviving, p = 0.109). Human visual share
2% vs fly 80% visual-centrifugal. No homology claim; the δ agreement is
interesting but partly fortuitous (different units/graphs/designs).

## 7. Novelty
Bounded and verified: **"To our knowledge, no prior study has combined these
analyses in a per-subject population-scale human structural-connectome
framework with a pre-registered cross-scale comparison."** The novelty lies
primarily in the integration of established analyses and the resulting
cross-scale empirical comparison, not in any individual component
(full audit: `10_REPORT/NOVELTY_AUDIT.md`; claim-by-claim:
`CLAIM_EVIDENCE_MATRIX.md`). Closest neighbor (Kudriavtsev 2026): PARTIAL
OVERLAP — matched-mass (not degree-preserving) nulls, ageing framing. Full
text **full-text verified via proxy extraction 2026-09-26** (5th attempt
succeeded; PARTIAL OVERLAP confirmed, all four decisive overlap components
excluded). Matrix:
`10_LITERATURE/NOVELTY_MATRIX.md` (2026-09-26 sweep appended: Yadav 2025,
Venkadesh 2025, Niyazmand 2026 recorded as adjacent; none occupies the
combination).

## 8. Limitations
Undirected graphs (directed variant impossible in these derivatives); single
pipeline/acquisition; residual near CIS noise floor; battery-B per-subject
empirical p at the 1/101 null-resolution floor (inference via z + sign test);
subcortical residual not robust across the K ladder; Kudriavtsev 2026
full text verified via proxy (direct access blocked); ENVIRONMENT_MANIFEST
provenance gap disclosed.

## 9. Reproducibility status
**PASS.** Independent stdlib-only audit recomputed every documented number
from frozen artifacts: 42/42 at freeze; extended to 44/44 on 2026-09-26
(added max-population-mean-CIS checks; manuscript rounding corrected
0.00463 → 0.00462 to match `e03_summary.json` = 0.0046246); extended to
46/46 on 2026-09-26 after the E06 threshold clarification (two full-precision
E06 checks replace a never-triggering gate)
(`10_REPORT/verify_final_numbers.py`, `FINAL_REPRODUCIBILITY_AUDIT.md`).
Implementations cross-validated (4e-16 / 6.1e-16). No unexplained
discrepancy exists anywhere in the tree.

## 10. Repository status
`github.com/harsha-vardhan-2006/humanbrain_cross_species_cis` — main, all
commits authored "Harsha Vardhan Malipeddi", working tree clean. Release
`cross_species_cis_v1.0.0.zip` (6,686 files, ~41 MB, CRC OK, SHA256
recorded). Fruitfly repo: history rewritten solely for author identity
(provenance note appended; old→new SHA map recorded; tip 9a6ac1a).

## 11. Publication readiness
READY. `SUBMISSION_PACKAGE/` contains cover letter, highlights,
graphical-abstract description, contributions (CRediT, author-confirmed),
data/code availability, reproducibility, COI (none to declare), ethics note
(secondary use of public data; no IRB required — author determination),
novelty statement, and journal options. Completed 2026-09-26: author
placeholders (contributions/COI/ethics/affiliation — correspondence
withheld from the public repo by author decision); PDF/DOCX typesetting
(pandoc 3.11 + headless Chrome — `SUBMISSION_PACKAGE/rendered/`); figure
captions (`08_FIGURES/FIGURE_CAPTIONS.md`). Remaining: venue choice/APC
verification and submission itself (human actions). Optional: co-signature
of the (now closed) Kudriavtsev full-text gate record.

## 12. Remaining tasks (all human actions)
1. ~~Read Kudriavtsev 2026 full text; co-sign the gate record.~~ CLOSED
   2026-09-26 (full text verified via proxy; optional co-signature only).
2. ~~Complete the [PLACEHOLDER] fields in the submission package.~~ DONE
   2026-09-26 (CRediT, COI, ethics, affiliation — author-confirmed;
   correspondence withheld from the public repo by author decision).
3. ~~Render manuscript to PDF/DOCX.~~ DONE 2026-09-26
   (SUBMISSION_PACKAGE/rendered/). ~~Finalize Figure 5~~ — DONE 2026-09-26
   (rendered from frozen table_07 by `08_FIGURES/make_fig05_anatomical.py`).
4. Choose venue (see `SUBMISSION_PACKAGE/JOURNAL_OPTIONS.md`); adapt cover
   letter; submit.
5. Optionally: Zenodo DOI for the release archive; GitHub release page.
