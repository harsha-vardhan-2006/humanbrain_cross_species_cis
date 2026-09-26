# Reproducibility Statement

1. **Protocol freeze before computation.** Hypotheses, primary configuration
   (4S456 × SIFT count × 15% cost), null design, gate rules (R1/R2a/R2b), and
   outcome classes were frozen in `PROTOCOL_FREEZE.md` before any CIS was
   computed; gates were resolved verbatim from frozen artifacts
   (`10_REPORT/RESOLUTION.md`).
2. **Independent numeric audit.** Every headline number was recomputed from
   raw artifacts by a dependency-free script on 2026-09-26: **42/42 PASS**
   (`10_REPORT/verify_final_numbers.py`; appendix in
   `FINAL_REPRODUCIBILITY_AUDIT.md`).
3. **Implementation cross-validation.** Exact-CIS reference vs naive
   recomputation: max deviation 6.1e-16. Fast (null-graph) estimator vs
   reference: 4e-16, gated at 1e-9 before use
   (`FAST_IMPLEMENTATION_VALIDATION.md`).
4. **Null integrity.** Exact per-node degree preservation verified per null:
   10,000/10,000; 0 self-loops; seeds 100+i; adversarial regression suite
   (hub-selfloop/pendant, dense, ring) passing.
5. **Robustness.** 9 pre-declared configurations; all reproduce the
   primary architecture (max like-for-like top-50-mean deviation 0.00262,
   atlas_AAL116; no pre-registered numeric tolerance — descriptive);
   rank stability median Spearman 0.996 over 100 half-splits.
6. **Traceability.** Every manuscript number maps to a frozen artifact file
   (audit §C and `FIGURE_PROVENANCE.md`); append-only research log; no
   silent corrections (the two documentation fixes of 2026-09-26 are flagged
   in-line and logged).
7. **Known gaps (disclosed).** `ENVIRONMENT_MANIFEST.txt` absent (versions
   reconstructed from logs); Kudriavtsev 2026 full text verified via
   text-extraction proxy 2026-09-26 (direct access network-blocked;
   closest-neighbour assessment now full-text grounded).
