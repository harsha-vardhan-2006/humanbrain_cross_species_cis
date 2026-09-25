# ANALYSIS FREEZE — Cross-Species CIS Study

**Freeze date:** 2026-09-26
**Precondition:** FINAL_REPRODUCIBILITY_AUDIT.md = PASS (42/42 numeric checks).

> **Primary scientific results are frozen. Any future analytical change must
> be documented as a new analysis rather than silently replacing the frozen
> result.**

## Dataset
- Source: AOMIC-ID1000 structural-connectome derivative, Zenodo record
  **19796783** (DOI 10.5281/zenodo.19796783), license CC-BY-4.0.
- Version: as published at acquisition (2026-09-20); 10 zips,
  7,067,175,601 bytes, byte-exact vs Zenodo API; SHA256 in
  `../00_Metadata/CHECKSUMS_AOMIC.sha256`; raw zips READ-FOREVER.
- Subjects: 900 acquired; **801 QC-pass** primary cohort (frozen CIS-blind at
  E02); 99 flagged retained for sensitivity.
- Atlas: **4S456Parcels** (456 nodes, system labels archived in
  `00_MANIFEST/manifests/atlas_4S456_system_labels.csv`).

## Frozen analysis parameters
| Parameter | Value |
|---|---|
| Weight (primary) | `sift_radius2_count_connectivity` |
| Threshold/cost | 15% proportional (k = round(0.15 × 456·455/2) = 15,561 edges); ladder 10/20/25% |
| Graph | undirected, binary for CIS; symmetric input verified; diagonals zeroed |
| CIS definition | CIS(i) = (E(G) − E(G−i))/E(G), E = unweighted global efficiency; exact per node |
| Estimators | scipy Dijkstra reference (observed) + boolean-matmul fast path (nulls), equivalence-gated at 1e-9 |
| Degree/strength matching | ±10% total degree, 1:1 greedy, nearest-50 fallback (flagged) |
| Null model | Maslov–Sneppen undirected degree-preserving rewiring; exact per-node degree verification per null; rejection redraw (max 5) |
| Null count | 100 per graph. Battery A: 100 subjects × 100 (full 456-node CIS per null). Battery B: 200 subjects × 100 (top-50 positions) |
| Seeds | subject samples: 20260922 (single RNG, nested A⊂B); nulls: 100+i per graph; enrichment/rank-stability: 20260922 |
| Statistics | per-node empirical p (add-one, one-sided) → Stouffer (per subject) → BH-FDR q<.05 (single stratum); battery B z + two-sided sign test; system enrichment controls A/B, 10,000 perms; rank stability 100 half-splits |
| Primary endpoints | R1 (battery B concentration), R2a (per-node FDR), R2b (system enrichment z_B at K=50) — rules verbatim in REPORT_SCAFFOLD.md §1 |
| Secondary endpoints | rank stability, degree/strength association, E06 robustness ladder |
| Robustness | 9 configurations: atlases {4S256, 4S156, Brainnetome246Ext, AAL116} × weights {invnodevol, r2count} × costs {10, 20, 25}, n=150 cohort |

## Resolved outcome (2026-09-26 00:35 harvest; RESOLUTION.md)
- **R1 POSITIVE** — 200/200 subjects above null (median z 16.36, sign p 1.24e-60)
- **R2a POSITIVE** — 43/456 nodes q<.05 (max z 23.30)
- **R2b NEGATIVE** — no pre-specified sensory/visual system enriched;
  only Subcortical/Cerebellar nominal (z_B 2.08, p .031, 1.25×; absent at K=25)
- Verdict: layer-1 replicated; layer-2 weak/not system-structured — honest
  weaker-bridge report per the frozen matrix.

## Software
- Python 3.13.2 (study runs); numpy 2.4.2, scipy 1.18.0, pandas 2.3.3
  (versions per RESEARCH_LOG E01/E18-era log entries; see provenance gap
  note below), Windows 11 AMD64.
- Audit verifier: stdlib-only Python 3.12 (`verify_final_numbers.py`).

## Result-generation scripts (traceability)
| Result | Script |
|---|---|
| Graph math / CIS | `02_PREPROCESSING/cache_io.py` |
| Extraction/QC | `02_PREPROCESSING/preprocess_v2.py` |
| Baseline/QC gate | `03_BASELINE/baseline.py`, `baseline_report.py` |
| Per-subject CIS | `04_CIS/cis_primary.py` |
| Degree/strength control | `04_CIS/degree_control.py` |
| Null batteries | `05_NULLS/degree_preserving/null_models.py` |
| Statistics | `04_CIS/e05_statistics.py` |
| Robustness | `06_ROBUSTNESS/robustness.py` |
| Cross-scale | `07_CROSS_SCALE/cross_scale.py` |
| Tables / figures | `09_TABLES/build_tables.py`, `08_FIGURES/make_figures.py` |
| Harvest/gates | `10_REPORT/fill_report.py` |
| Final audit | `10_REPORT/verify_final_numbers.py` |

## Provenance gap (disclosed)
`02_PREPROCESSING/ENVIRONMENT_MANIFEST.txt` was logged (E01) but is absent
from the tree (presumed lost in the v1→v2 pipeline transition). Software
versions above are reconstructed from log entries. No statistical artifact
depends on this file.

**Final commit SHA at freeze:** recorded in RESEARCH_LOG SESSION CLOSE (this
freeze commit; see `git rev-parse HEAD` at analysis-freeze commit).
