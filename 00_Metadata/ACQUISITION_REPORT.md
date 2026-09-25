# BigBrain 2015 Acquisition - FINAL REPORT
Generated: 2026-09-20T11:44:38

## Verdict: PASS - ACQUISITION COMPLETE AND VERIFIED

## Scope
- Canonical release: BigBrainRelease.2015 (https://ftp.bigbrainproject.org/bigbrain-ftp/BigBrainRelease.2015/)
- Fly reference (read-only): FAFB v783 at G:\fruitfly (untouched; CC BY-NC 4.0)

## Planned vs acquired
| Bucket | Planned files | Planned GB | Acquired OK | GB OK |
|---|---|---|---|---|
| D volumes (NIfTI) | 18 | 3.33 | 18 | 3.33 |
| D small (cls/ROI/surfaces/labels) | 228 | 1.36 | 228 | 1.36 |
| F coronal full-res PNG | 7404 | 64.13 | 7404 | 64.13 |
| TOTAL | 7650 | 68.82 | 7650 | 68.82 |

Plus EXISTING_LOCAL (credited, not re-downloaded): 5 files in G:\humanbrain\full18
(full8_{100,200,300,400,1000}um_optbal.nii.gz, gzip-CRC + NIfTI verified, sizes match official FTP).

## Verification
- Per-file byte-size vs official server: ALL MATCH
- Structural checks (verify_summary.json): total=7660 verified=7660 failed=0
  - gzip CRC for all .nii.gz; NIfTI header dims/zooms/dtype via nibabel; gii load via nibabel;
    PNG signature+IEND for the 7404 coronal histological PNGs
- SHA-256: CHECKSUMS_D.sha256 / CHECKSUMS_F.sha256 (present)
- Quarantined files: 0 (NONE - good)

## Download statuses (download_manifest.csv)
- D:OK: 256
- F:OK: 7404

## Disk state (rule: keep >10 GB free at all times)
- D: 143.9 GB free / 355.8 GB total
- F: 47.3 GB free / 187.8 GB total

## Official metadata archived (size-verified)
- BigBrain_License.txt: 18,985 B (expected 18,985) OK
- BigBrain_Updates.txt: 10,074 B (expected 10,074) OK
- BigBrain_Credits.txt: 5,130 B (expected 5,130) OK
- BigBrain_Welcome.txt: 6,853 B (expected 6,853) OK
- BigBrain2_FAQ.txt: 4,251 B (expected 4,251) OK

## Not acquired / access blocked (see NOT_ACQUIRED.md)
- BigBrain1_MSM_2023.tar (264,898,560 B): listed; anonymous RETR denied (FTP 550 / HTTPS 403) -> NOT_ACQUIRED_ACCESS_DENIED
- BigBrain2_PreRelease.2023: FTP-listable/downloadable but IP-blocked over HTTPS; OUT OF SCOPE (canonical = 2015) -> NOT_ACQUIRED_OUT_OF_SCOPE
- Raw_Data (~1 TB), A3D (~110 GB), 40um ROI tiers, Minc 2D sections, axial/sagittal PNG planes,
  STL/OBJ/MNI-obj duplicates, fsaverage mirrors: JUSTIFIED_SKIP per approved plan

## Post-report addendum (2026-09-22): 12_HumanConnectome_AOMIC batch
Acquired 2026-09-20 (after this report's verdict) and verified separately:
10 zips / 7,067,175,601 B, size-vs-Zenodo 10/10 MATCH, zip-CRC 10/10 clean,
SHA-256 in CHECKSUMS_AOMIC.sha256. See AOMIC_VERIFICATION_REPORT.md.
Does not alter the BigBrain verdict above.

## Cross-species manifests
- cross_species_manifest.json / .csv (tags DIRECTLY / APPROXIMATELY / NOT_DIRECTLY)
- Key tag: BigBrain has NO connectome -> connectome-topology comparisons vs FAFB = NOT_DIRECTLY_COMPARABLE
- Fly neuropils <-> human cortical parcellations = APPROXIMATELY only (no homology claims)

## Provenance chain
1. Official FTP/HTTPS inventory (52 dir listings) -> F:\HumanBrain\00_Metadata\remote_listings\
2. HTTPS size probe (HTTP Range) -> http_sizes.tsv
3. Curated download lists (server-verified names/sizes) -> dl_D_volumes.txt, dl_D_small.txt, dl_F_coronal.txt
4. Resumable download (Range continuation; 15 GB/disk reserve guard) -> download_manifest.csv
5. Structural verification + SHA-256 -> verify_summary.json, CHECKSUMS_*.sha256
6. Cross-species manifests -> cross_species_manifest.json/.csv, dataset_bigbrain.csv
