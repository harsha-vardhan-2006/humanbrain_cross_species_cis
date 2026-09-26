# FINAL GATE REPORT — Cross-Species CIS Study (2026-09-26)

Every category below reflects checks actually executed this session (see
`FINAL_REPRODUCIBILITY_AUDIT.md` for the 42-check numeric appendix; failures
would be listed here in full).

## A. DATA INTEGRITY — **PASS**
900 acquired / 801 QC-pass / 456 nodes / 15,561 edges recomputed from
manifests; raw zips SHA256-verified (10/10); QC flags retained; no missing
data beyond documented upstream exclusions.

## B. COMPUTATIONAL REPRODUCIBILITY — **PASS**
`verify_final_numbers.py` re-derives every headline number from raw artifacts
(exit 0). Implementations cross-validated (reference vs naive 6.1e-16; fast
vs reference 4e-16 under a 1e-9 gate). Pipeline scripts present and
re-runnable; full expensive rerun unnecessary and deliberately not repeated
(prompt rule 19).
## C. STATISTICAL CONSISTENCY — **PASS**
All gate resolutions match pre-registered rules (R1/R2a/R2b); analytic
cross-checks agree (sign p = 2×0.5²⁰⁰ = 1.2446e-60; Stouffer ceiling =
10·Φ⁻¹(100/101) = 23.3008 confirms the reported max z); FDR recount 43/456;
no discrepancy between manuscript and artifacts.

## D. LITERATURE NOVELTY — **PASS (bounded; gate CLOSED)**
Matrix complete (10 works + this study; NOVELTY_MATRIX.md). Closest neighbor
assessed PARTIAL OVERLAP on verified evidence. **Update 2026-09-26 (late):
the Kudriavtsev 2026 full text was verified via text-extraction proxy
(direct access remains 403-blocked) — confirms edge-level hotspot lesions,
matched-mass nulls, no per-node removal ranking, no degree-matched controls,
no degree-preserving nulls, no cross-scale bridge. The pre-submission
full-text-read condition is CLOSED; optional human co-signature remains
good practice** (see `10_LITERATURE/KUDRIAVTSEV_2026_FULLTEXT_REVIEW.md`
addendum).

## E. MANUSCRIPT CONSISTENCY — **PASS**
MANUSCRIPT_FINAL.md restructured from frozen v1.0 with zero value changes;
guardrail statements (no mechanism / no homology / R2b negative /
degree-anchored subcortical signal / partly-fortuitous δ) present verbatim.

## F. FIGURE CONSISTENCY — **PASS (complete)**
All existing figures generated from frozen artifacts by versioned scripts;
−inf censoring and p-floor annotations documented; no cross-species absolute
comparisons. **Figure 5 anatomical distribution rendered 2026-09-26 (late)
from frozen `table_07` + label manifest by `08_FIGURES/make_fig05_anatomical.py`
— no statistics recomputed (see FIGURE_PROVENANCE.md).**

## G. REPOSITORY REPRODUCIBILITY — **PASS**
Both repositories: commits authored "Harsha Vardhan Malipeddi"; working trees
clean; release checksum tracked; fruitfly history-rewrite provenance note
appended (old→new SHA map preserved). Disclosed gap: ENVIRONMENT_MANIFEST.txt
absent (versions reconstructed from logs).

## H. RELEASE INTEGRITY — **PASS**
`cross_species_cis_v1.0.0.zip`: SHA256 matches recorded checksum; CRC test
OK; 6,686 files; README/release notes/manuscript/analysis docs/provenance all
present inside the archive. Not rebuilt (no reason to; v1.0.0 stands).

## I. SUBMISSION READINESS — **READY (with conditions)**
Package complete (12 files). Conditions before upload, all human:
1. ~~Kudriavtsev full-text read + co-signature on the gate record.~~
   **CLOSED 2026-09-26** (full-text verified via proxy; optional co-signature).
2. Author placeholders (contributions, COI, ethics note, affiliation).
3. PDF/DOCX rendering (pandoc/LaTeX unavailable on the working machine;
   commands provided). Figure 5 render is DONE (frozen artifacts).

**Overall: the study is frozen, audited, and internally consistent. Nothing
failed; three named human actions remain.**
