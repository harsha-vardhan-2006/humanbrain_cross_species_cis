# AOMIC-ID1000 Structural Connectomes — Verification Report (Post-Acquisition Addendum)

Generated: 2026-09-22
Scope: `12_HumanConnectome_AOMIC\zenodo_19796783_raw\` — acquired 2026-09-20,
**after** the final BigBrain acquisition report (2026-09-20T11:44:38); this file
completes the provenance chain for that batch.

## Source
- Zenodo record **19796783**: *"Standardized structural connectivity mapping of the
  AOMIC-ID1000 dataset: A multi-scale tractography resource"*
- DOI: 10.5281/zenodo.19796783 · License: **CC-BY-4.0** (attribution required)
- Derivative of AOMIC ID1000 (OpenNeuro ds003097); pipeline: QSIprep + QSIrecon
  (MRtrix3). Full record metadata archived: `aomic_zenodo_record.json`.

## Verification (executed 2026-09-22)
| Check | Result |
|---|---|
| Byte size vs Zenodo API (`dl_D_aomic.txt`) | 10/10 EXACT MATCH |
| Zip internal CRC (`zipfile.testzip`) | 10/10 clean |
| SHA-256 (recomputed this pass) | `CHECKSUMS_AOMIC.sha256` (10 entries) |
| Totals | 7,067,175,601 B (6.58 GiB), 0 quarantined, 0 failures |

## Content inventory (from zip central directories + one full parse)
- 900 members total, all unique: `sub-XXXX_run-1_space-T1w_connectivity.mat`
  (90 per zip × 10 zips); 900 unique subject IDs.
- 100 IDs absent from the 1..1000 range (excluded upstream by the source
  dataset's own QC). NOT a download defect; no rescue attempt per no-guessing rule.
- Per .mat: 7 atlases × {region_ids, region_labels, 4 connectivity matrices} + a
  `command` provenance string.
  - Atlases: AAL116 (116), 4S156Parcels (156), Brainnetome246Ext (256), 4S256Parcels
    (256), AICHA384Ext (394), Gordon333Ext (385), 4S456Parcels (456).
  - Matrices per atlas: `sift_radius2_count_connectivity`,
    `sift_invnodevol_radius2_count_connectivity`, `radius2_count_connectivity`,
    `radius2_meanlength_connectivity`.
- Structural properties verified on sub-0001: all matrices symmetric;
  diagonals mostly nonzero (must be zeroed before graph use); off-diagonal
  densities AAL116 0.879 / Brainnetome246Ext 0.747 / 4S456 0.543.

## Safety-policy compliance
- RAW data untouched (hashes recorded; read-only access throughout).
- No deletes; nothing quarantined (no failures to quarantine).
- No writes to G:; all outputs under D:\humanbrain.

## Status
COMPLETE — AOMIC batch FULLY VERIFIED (10/10 zips OK, 900/900 members intact).

## Downstream use
Study design for the cross-species CIS analysis lives in
`13_CROSS_SPECIES_CIS\STUDY_DESIGN.md` (design only; nothing executed yet).
