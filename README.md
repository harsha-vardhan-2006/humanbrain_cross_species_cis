# HumanBrain Acquisition Workspace

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
