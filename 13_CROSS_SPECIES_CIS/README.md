# 13_CROSS_SPECIES_CIS — Cross-Scale Control Impact Study

Study asking whether the network-level control-impact architecture found in the
frozen fly connectome study (`G:\fruitfly`, release tag v1.0.0 — READ-ONLY
reference) has an analogous, measurable organization in the 900-subject human
structural connectome (AOMIC-ID1000 derivative, Zenodo 19796783, CC-BY-4.0).
**No anatomical homology claims** — network-level architectural comparison only
(cross_species_manifest CP03/CP05: APPROXIMATELY_COMPARABLE).

## What this study establishes (2026-09-26 framing audit)

**ESTABLISHED (analysis results, artifact-traced):**
- Population-scale human structural-connectome CIS analysis: exact per-node
  removal-based control impact, all 456 nodes × 801 QC-pass subjects
  (AOMIC-ID1000, Zenodo 19796783).
- Degree dependence of CIS: median Spearman ρ = 0.943 (CIS–strength 0.486).
- Degree-preserving null testing: top-50 concentration exceeds null
  expectations in 200/200 tested subjects (median z = 16.36;
  sign p = 1.24e-60); Maslov–Sneppen nulls verified degree-exact
  (10,000/10,000).
- Degree-independent residual analysis: residual > 0 in 778/801 subjects
  (Cliff's δ = 0.100; sign p = 2.6e-197); 43/456 nodes survive BH-FDR q<.05.
- Fly comparison (frozen FAFB v783 study): the original inhibitory/
  GABA-specific hypothesis did NOT survive degree-preserving null testing
  (p = 0.109); the surviving signal is visual–centrifugal enrichment after
  degree matching (≈2.6×, z = 5.30; 13/50 chokepoints beat matched peers);
  fly residual δ = 0.0979, itself not null-surviving.
- Cross-species two-component pattern: a dominant connectivity-dependent
  component plus a smaller degree-independent residual appears in both
  analyses; the residual's anatomical identity diverges (2% visual in human
  vs 80% visual-centrifugal in fly); the pre-registered human system-
  enrichment gate (R2b) was NEGATIVE — no robust canonical-system-specific
  explanation established.

**NOVEL / POTENTIALLY NOVEL (the contribution):**
- The integrated analytical framework: per-node removal CIS + population-
  scale per-subject computation + degree/strength-controlled decomposition
  + degree-preserving null arbitration + FDR-controlled residual inference
  + robustness/rank-stability analysis + pre-registered cross-species
  comparison (see `10_REPORT/NOVELTY_AUDIT.md`).
- Population-scale per-subject decomposition of control impact into
  connectivity-dependent and degree-independent components.
- The cross-scale comparison itself, and the empirical recurrence of the
  two-component organization across a ~10³-fold node-count difference.

**NOT CLAIMED:**
- No new CIS algorithm (node-removal efficiency analysis is classic:
  Alstott 2009; Crossley 2014).
- No new null model (Maslov–Sneppen; standard).
- No universal law, no "first ever", no proof of scale-invariance.
- No new biological mechanism; no anatomical homology (CP03/CP05 rules).
- No autonomous causal interpretation (structural sensitivity only).

Canonical wording: *"To our knowledge, no prior study has combined these
analyses in a per-subject population-scale human structural-connectome
framework with a pre-registered cross-scale comparison."* —
`10_LITERATURE/NOVELTY_MATRIX.md`; `10_REPORT/NOVELTY_AUDIT.md`;
`CLAIM_EVIDENCE_MATRIX.md`.

## Status (2026-09-26, post-freeze audit)

- P0 provenance: DONE (see `..\00_Metadata\AOMIC_VERIFICATION_REPORT.md`,
  `CHECKSUMS_AOMIC.sha256`, `aomic_zenodo_record.json`)
- P0 novelty gate: **GO, precisely bounded** — see `RESEARCH_LOG.md` E00 and
  `10_LITERATURE/NOVELTY_MATRIX.md`
- P1 protocol freeze: DONE (`00_MANIFEST/PROTOCOL_FREEZE.md`, pre-computation)
- E01-E10: COMPLETE. Null arbitration resolved (see 10_REPORT/RESOLUTION.md):
  R1 POSITIVE | R2a POSITIVE | R2b NEGATIVE.
- Final verdict: Layer-1 replicated (concentration exceeds degree-preserving nulls); layer-2 null evidence absent or not system-structured -> weaker bridge, honest report per the frozen matrix.
- 2026-09-26 finalization: independent numeric audit 42/42 PASS
  (`10_REPORT/FINAL_REPRODUCIBILITY_AUDIT.md`), ANALYSIS_FREEZE recorded,
  submission package assembled (`SUBMISSION_PACKAGE/`), gate report
  (`10_REPORT/FINAL_GATE_REPORT.md`). Release archive remains v1.0.0
  (verified; newer audit documents live in git, not in the ZIP).
- 2026-09-26 novelty-framing audit: `10_REPORT/NOVELTY_AUDIT.md` +
  `CLAIM_EVIDENCE_MATRIX.md` created; literature-positioning table updated
  in `10_LITERATURE/NOVELTY_MATRIX.md` (new adjacent work recorded: Yadav
  2025, Venkadesh 2025, Niyazmand 2026); "Contribution and Novelty" section
  added to the manuscripts; framing overclaims corrected (universal →
  near-universal; 10⁵ → 10³ fold; SIFT2 → SIFT-filtered counts;
  "not conserved" bounded). No numeric result changed; no analysis rerun.

## Key documents

- `STUDY_DESIGN.md` — data inventory, design decisions, phases, limitations
- `RESEARCH_LOG.md` — append-only experiment log (E00 = novelty gate)
- `..\00_Metadata\AOMIC_VERIFICATION_REPORT.md` — RAW batch verification

## Layout

```
00_MANIFEST/      subject / atlas / analysis manifests
01_RAW_PROBES/    raw structure + QC reports (no .mat data copied here)
02_PREPROCESSING/ extraction + QC pipeline and report
03_BASELINE/      per-atlas network statistics across subjects
04_CIS/           exact control-impact analysis (subject_cis/ per subject)
05_NULLS/         degree-matched + degree-preserving null batteries
06_ROBUSTNESS/    atlas / weight / threshold sensitivity matrices
07_CROSS_SCALE/   fly <-> human synthesis (frozen fly artifacts only)
08_FIGURES/       figures
09_TABLES/        tables
10_REPORT/        final report + manuscript
logs/             run logs (append-only discipline)
```

## Rules (inherited, binding)

1. RAW AOMIC zips (`..\12_HumanConnectome_AOMIC\zenodo_19796783_raw\`) are
   READ-FOREVER: nothing written, moved, or deleted there.
2. Frozen fly repository (`G:\fruitfly`) is READ-ONLY; only its published
   result artifacts (JSON/CSV tables) may be read for the synthesis phase.
3. No deletes anywhere in this tree; superseded outputs are quarantined and
   labeled.
4. No scientific computation before the P1 freeze entry exists in
   `RESEARCH_LOG.md`.
5. All scripts under this tree; every manuscript number must trace to a
   frozen artifact file.
