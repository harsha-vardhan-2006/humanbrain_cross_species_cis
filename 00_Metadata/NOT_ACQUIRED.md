# Not Acquired / Access Denied - BigBrain FTP (recorded 2026-09-19)

## ACCESS_BLOCKED (server refuses anonymous download; no workaround attempted)
| Item | Size (measured) | Evidence |
|---|---|---|
| BigBrainRelease.2015/BigBrain1_MSM_2023.tar | 264,898,560 B | HTTPS GET/HEAD/range -> 403 Forbidden (all UA, all ranges); FTP SIZE ok (213 264898560) but RETR -> 550 Permission denied |

### Alternative-source attempts for BigBrain1_MSM_2023.tar (2026-09-20, all failed)
| Source | Result |
|---|---|
| FTP RETR (anonymous, both hosts) | 550 Permission denied (server-side ACL; only this one tar is locked, sibling files download fine) |
| HTTPS loris.ca + ftp.bigbrainproject.org | 403 Forbidden |
| Plain HTTP (both hosts) | 200 but returns HTML listing/error page, not the tar |
| OSF mirror (osf.io/download/BigBrain1_MSM_2023/) | 404 file not found |
| Zenodo records 10159314 / 8423140 | 404 no such file |
| EBRAINS data bucket | DNS does not resolve |
| CBRAIN object store / S3 mirror | DNS does not resolve |
| CONP DataLad (BigBrain_BigBrainWarp_Support) | Does NOT contain the tar; only MSM sphere transformations — equivalent content already acquired in D:\HumanBrain\09_BigBrainWarp (60 files incl. sphere.reg.gii for fsLR/fsavg/MNI152) |

Conclusion: the tar is deliberately restricted by the BigBrain project (likely requires MCIN network
or registered access). Its useful content (MSM spherical transformations between BigBrain, fsLR,
fsavg, MNI152 surfaces) is ALREADY covered by the acquired 09_BigBrainWarp set.

## ACCESS_BLOCKED (continued)
| Item | Size (measured) | Evidence |
|---|---|---|
| BigBrain2_PreRelease.2023 via HTTPS | - | HTTPS directory + files -> "Access denied ... outside of the MCIN network" (nginx, IP-based) |

Note: BigBrain2_PreRelease.2023 IS fully listable and downloadable over plain FTP
(anonymous login ok; e.g. FAQ.txt 4251 B RETR 226 success). It was NOT acquired because
it is outside the approved acquisition scope (canonical release = BigBrainRelease.2015).
Listing snapshots: F:\HumanBrain\00_Metadata\remote_listings\BB2_*.txt

## JUSTIFIED_SKIP (approved plan; measured during inventory)
| Item | Measured size | Reason |
|---|---|---|
| Hippocampus_Segmentation/A3D | ~110 GB (dir) | Redundant 3D model format; gii surfaces acquired instead (111 MB set) |
| Raw_Data | ~1 TB | Microscopy raw stack; out of scope |
| 3D_ROIs 40um/20um/60um/80um subsets | ~11+ GB per resolution tier | 100um tier acquired; higher-res subsets skipped per plan |
| 2D_Final_Sections Minc (all 3 planes) | ~477 GB total (16.15+15.73+15.78 GB x ... measured 161.5/157.3/157.8 GB) | .mnc format redundant; .nii volumes + PNGs acquired |
| 2D_Final_Sections Axial/Sagittal PNG Full_Resolution | 61.1 GB / 69.7 GB | Coronal plane (64.1 GB) is the primary histological plane; other planes skippable per plan |
| 3D_Surfaces stl / MNI-obj | 16-18 files each | Redundant surface formats; gii acquired |
| Layer_Segmentation 2D_Sections Coronal Minc/Png | server-side timeout during listing; small | 2D layer maps; PLoS gii surfaces acquired instead |
| Surface_Parcellations fsaverage, Documentation, Brainnetome(gii-mirror dirs) | - | Mirrors of external atlases; canonical BigBrain-space sets acquired |
| MicroDraw 256_DZI / Raw_3500 | 3+2 tiny index files only | Deep-zoom web tiles; not analysis data |

## NOT_DIRECTLY_COMPARABLE (recorded in cross_species_manifest.csv)
- BigBrain has NO connectome: connectome-topology comparisons with FAFB v783 are
  NOT_DIRECTLY_COMPARABLE (CP01, CP04). Fly-neuropil <-> human-parcellation mappings are
  APPROXIMATELY_COMPARABLE only (CP02, CP03, CP05); no homology claims.

## Top required future dataset
- A human connectome (e.g., HCP-derived macro-connectome or future human EM) would be
  required for any DIRECTLY_COMPARABLE connectome-topology analysis.
