# BigBrain 2015 Acquisition - Integrity Report (FINAL)
Generated: 2026-09-20T11:44:38

## Human dataset (BigBrainRelease.2015)
- Files recorded: 7660 (all OK in download_manifest.csv)
- Bytes: 69,468,208,716 (69.47 GB) — 0 missing, 0 size mismatches, 0 corrupt
- Verification: byte-size vs official FTP (all rows) + gzip-CRC/NIfTI/gii/PNG structural
  checks + SHA-256 (CHECKSUMS_D.sha256 / CHECKSUMS_F.sha256)
- verify_summary.json: total=7660 verified=7660 failed=0 (png=7404 nifti=40 gii=104 other=112)

## Fly dataset (FAFB v783) - read-only reference
- Source manifest: G:\fruitfly\results\tables\e18_manifest.json (6 entries)
- Untouched; used only as reference for cross-species manifests.

## Comparability tagging (mandatory)
- CP01: NOT_DIRECTLY_COMPARABLE
- CP02: APPROXIMATELY_COMPARABLE
- CP03: APPROXIMATELY_COMPARABLE
- CP04: NOT_DIRECTLY_COMPARABLE
- CP05: APPROXIMATELY_COMPARABLE

## Not acquired (recorded, no guessing)
- BigBrain2_PreRelease.2023: server-listable via FTP; HTTPS IP-restricted; out of approved
  scope -> NOT_ACQUIRED_OUT_OF_SCOPE
- BigBrain1_MSM_2023.tar: 264,898,560 B listed; anonymous RETR denied -> NOT_ACQUIRED_ACCESS_DENIED
- 3D A3D hippocampus model (~110 GB), Raw_Data (~1 TB), 40um ROI subsets, STL/JSON/OBJ
  duplicates, fsaverage mirrors: JUSTIFIED_SKIP (per approved plan)

Status: COMPLETE — ACQUISITION FULLY VERIFIED (7660/7660 files OK, 0 failures)
