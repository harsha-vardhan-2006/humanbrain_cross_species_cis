# 13_CROSS_SPECIES_CIS — Cross-Scale Control Impact Study

Study asking whether the network-level control-impact architecture found in the
frozen fly connectome study (`G:\fruitfly`, release tag v1.0.0 — READ-ONLY
reference) has an analogous, measurable organization in the 900-subject human
structural connectome (AOMIC-ID1000 derivative, Zenodo 19796783, CC-BY-4.0).
**No anatomical homology claims** — network-level architectural comparison only
(cross_species_manifest CP03/CP05: APPROXIMATELY_COMPARABLE).

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
