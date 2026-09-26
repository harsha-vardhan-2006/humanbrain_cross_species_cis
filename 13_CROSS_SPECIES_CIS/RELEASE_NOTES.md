# RELEASE NOTES — 13_CROSS_SPECIES_CIS v1.0.0 (2026-09-26)

Cross-Scale Control Impact Study: human structural connectomes
(AOMIC-ID1000, 900 subjects, Zenodo 19796783) vs the frozen fly study
(FAFB v783, release v1.0.0, READ-ONLY reference).

## Package contents
- 10_REPORT/         RESOLUTION.md, FINAL_AUDIT.md (FINAL PASS),
                     MANUSCRIPT_DRAFT.md v1.0, FINAL_RESULT_DECISION.md,
                     REPORT_SCAFFOLD.md, fill_report.py
- 09_TABLES/         tables 01-10 (incl. table_07 per-node Stouffer/BH-FDR)
- 08_FIGURES/        fig01-fig09 (PNG + PDF)
- 07_CROSS_SCALE/    table_09_cross_scale.csv, CROSS_SCALE_ANALYSIS.md,
                     human_chokepoint_catalogue.csv, cross_scale.py
- 06_ROBUSTNESS/     E06: 9 configurations (atlas/weight/cost ladders)
- 05_NULLS/          degree-preserving batteries A (100 subj x 100 nulls) and
                     B (200 subj x 100 nulls): npz per-subject nulls, manifests,
                     validation (exact degree preservation 100.00%),
                     regression tests, NULL_MODEL_REPORT.md
- 04_CIS/            per-subject exact CIS (900 files), E03b degree-strength
                     controls, e05_statistics.json, validation reports
- 03_BASELINE/       per-atlas baseline + QC (801/900 pass cohort)
- 02_PREPROCESSING/  cache_io.py (frozen math), preprocess_v2.py, QC reports
                     (cache_parts/ EXCLUDED from ZIP - 4.0 GB, regenerable)
- 00_MANIFEST/       manifests incl. atlas_4S456_system_labels.csv, audit
- RESEARCH_LOG.md, STUDY_DESIGN.md, PROTOCOL_FREEZE.md, README.md,
  RELEASE_NOTES.md, logs/

## Headline results (all artifact-traced; see RESOLUTION.md)
- R1 POSITIVE: top-50 concentration > degree-preserving nulls in 200/200
  subjects (median z = 16.36; sign p = 1.24e-60)
- R2a POSITIVE: 43/456 nodes survive BH-FDR q < .05 (max z = 23.3)
- R2b NEGATIVE: no pre-specified sensory/visual enrichment; only
  Subcortical/Cerebellar nominal (z_B = 2.08, p = .031, 1.25x)
- Cross-scale bridge: Cliff's delta 0.100 (human) vs 0.0979 (fly) -
  the architecture replicates, the anatomy does not.

## Version notes (2026-09-26 novelty-framing audit; no statistic changed)
- `10_REPORT/NOVELTY_AUDIT.md` and `CLAIM_EVIDENCE_MATRIX.md` created:
  bounded novelty wording, claim-by-claim evidence classes, explicit
  NOT-claimed list (no new CIS algorithm, no universal law, no mechanism,
  no homology, no "first ever").
- `10_LITERATURE/NOVELTY_MATRIX.md`: 2026-09-26 sweep appended (Yadav 2025,
  Venkadesh 2025, Niyazmand 2026 recorded as adjacent; verdict retained).
- "Contribution and Novelty" section added to MANUSCRIPT_FINAL and the
  submission-package manuscript (Established methods / Integration / New
  findings / Cross-species interpretation / Limitations of the claim).
- Framing corrections (flagged inline; artifact-verified): "universal" →
  "near-universal" residual (778/801); "10⁵-fold" → "roughly 10³-fold"
  node-count difference (139,255 neurons vs 456 parcels); "SIFT2" →
  "SIFT-filtered counts"; "mechanism is not conserved" bounded to "not
  established to be conserved".
- MANUSCRIPT max-CIS value corrected 0.00463 → 0.00462 to match the frozen
  artifact (`e03_summary.json` cis_mean_pop_max = 0.0046246);
  `verify_final_numbers.py` extended to 44 checks, all PASS.

## Version notes (2026-09-26 documentation-integrity pass; no statistic changed)
- Fixed rewire-acceptance unit bug in fill_report.py (was reported as
  7694144.8%; correct value 49.4% of attempted swaps); RESOLUTION.md and
  NULL_MODEL_REPORT.md corrected with flagged notes.
- RESEARCH_LOG: CORRECTIONS entry + E17a (Kudriavtsev 2026 pre-submission
  literature gate: complete abstract verified via mirror; full text still
  network-blocked; one manual read remains before submission).
- MANUSCRIPT_DRAFT: Section 5 Discussion completed; Section 6 limitations
  extended (null-resolution floor; subcortical residual robustness;
  literature-gate status).
