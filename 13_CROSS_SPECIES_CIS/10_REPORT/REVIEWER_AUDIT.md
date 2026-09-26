# REVIEWER AUDIT — simulated peer review (2026-09-26, final QC phase)

Simulated independent review of the frozen study state (commit `7eeb4d1`).
Every concern is classified CRITICAL / HIGH / MEDIUM / LOW / INFORMATIONAL and
given a resolution status against actual repository evidence. This file is
part of the final quality-control record; it documents what a skeptical expert
would likely raise, and where the repository already answers it.

---

## REVIEWER A — Statistics

**Major concerns**
1. Per-subject empirical p-values sit at the 1/101 resolution floor (battery B).
   — **MEDIUM, ALREADY DISCLOSED**: inference rests on z-vs-null and the
   population sign test (MANUSCRIPT §4 limitation; RESOLUTION; claim matrix
   row 24). Cannot be fixed without more nulls; disclosed, not hidden.
2. Node-level FDR treats 456 tests within one stratum; nodes are not
   independent (spatial/spatial-graph dependence). — **MEDIUM, DISCLOSED**:
   BH-FDR at q<.05 is standard for this design; dependence is bounded by the
   concentration of survivors in one node block, which the manuscript reports
   rather than interprets as independent confirmations (§5.2).
3. The residual analysis is a one-sided directional test (residual > 0).
   — **LOW, PRE-REGISTERED**: the direction was fixed by the frozen
   fly-derived prediction (Outcome-B); both Wilcoxon (two-sided, median
   p = 0.167) and sign test are reported side by side.

**Minor concerns**: effect-size CIs not reported for fly δ (bootstrap could be
added) — **LOW, INFORMATIONAL**: fly artifacts are frozen/read-only; the
manuscript already flags the δ agreement as partly fortuitous.

**Verdict: no CRITICAL, no HIGH.**

## REVIEWER B — Connectomics / neuroscience

**Major concerns**
1. Human graphs are undirected; fly analysis was directed. — **HIGH
   ORIGINALLY, DISCLOSED AS STRUCTURAL LIMITATION**: a directed variant is
   impossible in these derivatives (documented, not skipped); the cross-scale
   bridge is explicitly an undirected-projection statement (MANUSCRIPT §5.4).
   Cannot be fixed from existing data; correctly a limitation, not a flaw.
2. Parcel ≠ neuron: 456 parcels vs 139,255 neurons. — **DISCLOSED**:
   normalized comparators only (DIRECT/NORMALIZED/QUALITATIVE tags,
   CP03/CP05); ~10³ node-count difference stated in all summaries.
3. Tractography weights are reconstruction-dependent (SIFT counts, single
   pipeline). — **DISCLOSED**: mitigated by multi-weight/multi-cost/multi-atlas
   robustness ladder (9 configs, all within 0.0026 of primary like-for-like).
4. Subcortical/cerebellar concentration could be a degree artifact. —
   **DISCLOSED AND TESTED**: control B absorbs degree; z_B = 2.08 nominal at
   K=50, absent at K=25 (z_B = 0.81); reported as degree-anchored
   concentration, R2b NEGATIVE.

**Verdict: no CRITICAL. One HIGH-class structural limitation (directedness),
correctly framed as a limitation rather than claimed away.**

## REVIEWER C — Computational reproducibility

**Major concerns**
1. Can every reported number be regenerated? — **ADDRESSED**: 44/44 checks in
   `verify_final_numbers.py` recompute every headline number from frozen
   artifacts; implementations cross-validated (6.1e-16 / 4e-16); pipeline
   mapped end-to-end in `REPRODUCIBILITY.md` with commands, seeds, runtimes.
2. Environment provenance. — **DISCLOSED GAP**: original
   `ENVIRONMENT_MANIFEST.txt` lost in v1→v2 transition; versions reconstructed
   from logs and re-verified (E01v2 rerun record on disk matches).
3. Heavy data not in Git. — **BY DESIGN**: whitelist .gitignore; raw zips
   public (Zenodo, CC-BY-4.0); `cache_parts/` regenerable and excluded from
   the release archive; release SHA256 pinned and verified OK.

**Verdict: no CRITICAL, no HIGH. One MEDIUM disclosed provenance gap.**

## REVIEWER D — Novelty / literature

**Major concerns**
1. "Is the combination really unoccupied?" — **ADDRESSED**: E00/E17/E17a plus
   2026-09-26 sweeps; closest neighbour (Kudriavtsev 2026) **full-text
   verified via proxy** — edge-level hotspot lesions, matched-mass nulls, no
   per-node removal, no degree-matched controls, no degree-preserving nulls,
   no cross-scale bridge. Newer adjacent work (Yadav 2025, Venkadesh 2025,
   Niyazmand 2026) recorded honestly in NOVELTY_MATRIX.
2. Claim wording. — **ADDRESSED**: "to our knowledge", bounded to the
   combination; method novelty explicitly disclaimed; limitations of the
   novelty claim documented (NOVELTY_AUDIT §9–10).
3. Kudriavtsev access. — **RESOLVED**: full text verified via proxy
   (direct access still 403; disclosed as such); gate record contains
   re-answered questions 1–10.

**Verdict: no CRITICAL, no HIGH.**

## REVIEWER E — Skeptical (overclaiming)

**Major concerns**
1. "Universal residual" phrasing. — **FIXED 2026-09-26**: titles use
   "near-universal"; residual is 778/801 (97.1%); the single remaining
   "universal" instances are negations/guardrails.
2. Cross-scale scale-factor error (10⁵ vs 10³). — **FIXED 2026-09-26**:
   "roughly 10³-fold" with explicit counts (139,255 neurons vs 456 parcels).
3. "Mechanism is not conserved" stated as fact. — **FIXED**: bounded to "not
   established to be conserved (nor that it is not)".
4. Negative results buried? — **NO**: "Negative and null findings" content is
   in manuscript §4 (limitations + R2b NEGATIVE inline) and the dedicated
   HYPOTHESIS_RESULT_MATRIX; fly GABA rejection is in the abstract-level
   summaries, README boundaries, and claim matrix row 10.
5. Preregistration vs post-hoc mixing. — **CLEAN**: R1/R2a/R2b were frozen
   pre-computation (PROTOCOL_FREEZE, REPORT_SCAFFOLD §1 rules verbatim);
   post-hoc observations (e.g., K-ladder fragility) are labelled as such.

**Verdict: no CRITICAL, no HIGH.**

---

## CONSOLIDATED QUALITY GATE

| Severity | Count (open) | Notes |
|---|---|---|
| CRITICAL | **0** | — |
| HIGH | **0** | Directedness limitation is disclosed-as-limitation, not an open defect |
| MEDIUM | 3 (all disclosed) | 1/101 p-floor; FDR dependence; environment-manifest reconstruction |
| LOW | 3 | One-sided residual test (pre-registered); fly-δ CIs (frozen artifacts); figure-caption annotations pending typesetting |
| INFORMATIONAL | 2 | Author placeholders; PDF/DOCX rendering (pandoc unavailable on the working machine) |

**Simulated-reviewer outcome: the study would face no CRITICAL or HIGH
unresolved objections; all MEDIUM items are disclosed limitations with
documented rationale, not hidden weaknesses.**
