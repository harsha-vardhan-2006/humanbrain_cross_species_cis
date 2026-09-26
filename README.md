# HumanBrain Cross-Species CIS

**Cross-scale control-impact study: human structural connectomes (AOMIC-ID1000)
vs the Drosophila connectome (FAFB v783).**

**Status: frozen scientific result, publication phase (2026-09-26).**
Submission package complete (author fields filled, PDF/DOCX rendered,
figure captions added, MIT license); code licensed MIT (`LICENSE`).
Reviewer-requested analyses, if any, must be added as clearly labeled
post-hoc/secondary analyses — never by modifying the pre-registered
primary results.

## Scientific Objective

Investigate removal-based structural network impact — the Control Impact
Score, CIS(i) = (E(G) − E(G−i))/E(G) — in population-scale human structural
connectomes and in the Drosophila connectome; separate the
connectivity-dependent component of that impact from any degree-independent
residual; and compare the resulting architecture across scales.

## Main Findings

- **Degree dominance.** CIS is strongly associated with degree
  (median Spearman ρ = 0.943; 801 QC-pass subjects of 900 acquired;
  456-node atlas).
- **Concentration beyond nulls.** Top-50 CIS concentration exceeds
  degree-preserving (Maslov–Sneppen) null expectations in 200/200 tested
  subjects (median z = 16.36; sign p = 1.24 × 10⁻⁶⁰).
- **Degree-independent residual.** A smaller residual component remains
  detectable in 778/801 subjects (Cliff's δ = 0.100; sign p = 2.6 × 10⁻¹⁹⁷);
  43/456 nodes survive BH-FDR q < .05.
- **Not system-specific.** The pre-registered system-enrichment gate was
  negative; visual systems hold only 2% of the human top-50; no robust
  canonical-system-specific explanation was established.

## Cross-Species Finding

**"Architecture replicates; anatomy does not."** A broadly similar
two-component organization — a dominant connectivity-dependent component plus
a smaller degree-independent residual — appears in both the human
(δ = 0.100) and fly (δ = 0.0979, itself not null-surviving) analyses, across a
roughly 10³-fold node-count difference, while the residual's anatomical
identity diverges (human 2% visual vs fly 80% visual-centrifugal).

## Contribution and Novelty

The individual components are established methods (node-removal efficiency
analysis, cost thresholding, matched controls, configuration-model nulls,
FDR, cross-species connectomics). The contribution is the **integrated
framework** — per-node removal CIS + population-scale per-subject computation
+ explicit degree/strength-controlled residualization + degree-preserving
null-model arbitration + FDR-controlled residual inference +
robustness/rank-stability analysis + a pre-specified cross-species comparison
with Drosophila — and the resulting cross-scale empirical comparison. Full
audit: `13_CROSS_SPECIES_CIS/NOVELTY_AUDIT.md`;
claim-by-claim evidence: `13_CROSS_SPECIES_CIS/CLAIM_EVIDENCE_MATRIX.md`.

## Scientific Boundaries

- No anatomical homology is claimed (explicit no-homology rules,
  CP03/CP05).
- No conserved biological mechanism, no universal law, and no causal
  mechanism is established.
- The cross-scale similarity is an architectural observation and a
  hypothesis-generating finding: it motivates, but does not prove, that
  hierarchical organization of network impact may recur across
  nervous-system scales.
- Negative results are preserved: the fly study's original
  GABA/inhibitory-specific hypothesis was **rejected** under degree-preserving
  null testing, and the human residual yielded **no** robust
  canonical-system-specific interpretation.

## Data and Reproducibility

Human data: AOMIC-ID1000 structural connectomes (Zenodo 19796783, CC-BY-4.0;
900 subjects × 7 atlases, checksum-verified). Fly reference: frozen FAFB v783
release (139,255 neurons; CC BY-NC 4.0). Every manuscript number traces to a
frozen artifact; an independent stdlib-only audit recomputes all headline
values (`13_CROSS_SPECIES_CIS/10_REPORT/verify_final_numbers.py`, 44/44 PASS).
Full pipeline, manifests, and append-only research log:
`13_CROSS_SPECIES_CIS/` (see also `13_CROSS_SPECIES_CIS/10_REPORT/
FINAL_RESEARCH_STATUS.md` and `RESOLUTION.md`).

---

## Workspace safety policy

*(The sections below are the original acquisition-workspace documentation.
They are retained unchanged: the study tree `13_CROSS_SPECIES_CIS/` depends on
these datasets and protection rules.)*

Safety policy (binding for all tooling in this workspace):
- G: is strictly READ-ONLY. Nothing may be written, moved, or deleted there.
  (Verified: G:\fruitfly untouched at 261 files / 17,521,318,473 bytes throughout.)
- No deletes anywhere. Suspicious/failed files go to *_QUARANTINE folders only.
- RAW data untouched; conversions only under 11_DERIVED (D:) or 05_DERIVED (F:).
- Disk rule: stop downloads if a drive falls below 15 GB free (enforced in downloader).

## Layout
- D:\HumanBrain\00_Metadata  manifests, checksums, license, reports, download lists
- D:\HumanBrain\01..09       BigBrain 2015 core data (volumes, classified, MRI, surfaces, ROIs,
                             layers, hippocampus, parcellations, BigBrainWarp)
- D:\HumanBrain\10_MSM_2023  EMPTY (BigBrain1_MSM_2023.tar is access-denied anonymously; see
                             00_Metadata\NOT_ACQUIRED.md)
- D:\HumanBrain\11_DERIVED   derived products only (never touch RAW)
- D:\HumanBrain\12_HumanConnectome_AOMIC  AOMIC-ID1000 structural connectomes
                             (Zenodo 19796783, CC-BY-4.0; 10 zips / 6.58 GiB / 900
                             subjects × 7 atlases) — downloaded 2026-09-20, verified
                             2026-09-22 (CHECKSUMS_AOMIC.sha256 +
                             AOMIC_VERIFICATION_REPORT.md)
- D:\HumanBrain\13_CROSS_SPECIES_CIS  cross-scale CIS study tree (STUDY_DESIGN.md;
                             RAW zips in 12_ stay READ-FOREVER)
- F:\HumanBrain\01_Histology 7404 coronal full-resolution PNG sections (64.1 GB)
- F:\HumanBrain\00_Metadata\remote_listings  52 official FTP directory listing snapshots
- G:\humanbrain\full18       5 pre-existing full8 volumes (EXISTING_LOCAL; verified, credited)
- G:\fruitfly                FAFB v783 fly dataset (READ-ONLY reference; CC BY-NC 4.0)

## Key reports (D:\HumanBrain\00_Metadata)
- ACQUISITION_REPORT.md      final acquisition report (PASS when all verified)
- INTEGRITY_REPORT.md        integrity/comparability summary
- cross_species_manifest.*   FAFB <-> BigBrain comparability map (mandatory tags)
- NOT_ACQUIRED.md            access-blocked + justified skips (no guessing)
- dataset_catalog.md         what lives where
- CHECKSUMS_D.sha256 / CHECKSUMS_F.sha256 / CHECKSUMS_G_reference.sha256
- CHECKSUMS_AOMIC.sha256 + AOMIC_VERIFICATION_REPORT.md  (12_HumanConnectome_AOMIC batch)

## License
- BigBrain 2015: CC BY-NC-SA 4.0 (research-only; attribution + share-alike; no commercial use).
  Official text archived: 00_Metadata\BigBrain_License.txt (18,985 B, size-verified).
- FAFB v783: CC BY-NC 4.0 (see G:\fruitfly LICENSE_NOTES.md).

## Reproducibility
All acquisition tooling is under D:\HumanBrain\99_Logs (downloaders, probes, verifiers,
report generators). Re-running any script is safe: downloads resume, verification re-runs,
reports regenerate.
