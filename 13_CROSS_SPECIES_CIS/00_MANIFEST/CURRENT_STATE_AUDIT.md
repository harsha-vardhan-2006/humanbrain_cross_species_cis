# CURRENT STATE AUDIT — Phase 0.5

Date: 2026-09-22 · Executor: Buffy (Freebuff) · Scope: read-only inspection; NO scientific decisions modified, NO analysis run.

## 1. Data available (verified on disk this session)

| Item | Value |
|---|---|
| RAW location | `D:\HumanBrain\12_HumanConnectome_AOMIC\zenodo_19796783_raw\` |
| ZIP files | 10 (`connectomes_part_1..10.zip`) |
| Total bytes | 7,067,175,601 (6.58 GiB) |
| Members | 900 × `sub-XXXX_run-1_space-T1w_connectivity.mat` (90/zip, 0 duplicates) |
| Subjects | 900 unique IDs; 100 IDs absent from 1..1000 (upstream exclusions; documented, not chased) |
| Provenance | Zenodo record 19796783, DOI 10.5281/zenodo.19796783, license cc-by-4.0, archived in `aomic_zenodo_record.json` (10 files listed) |

## 2. Atlas inventory (verified in sub-0001, 2026-09-22)

| Atlas key | Nodes | Labels carry system names | Role (proposed) |
|---|---|---|---|
| `atlas_4S456Parcels` | 456 | YES (Vis 61, SomMot 77, DorsAttn 46, SalVentAttn 47, Limbic 26, Cont 52, Default 91, subcortical) | **PRIMARY** |
| `atlas_4S256Parcels` | 256 | YES | sensitivity |
| `atlas_4S156Parcels` | 156 | YES | sensitivity |
| `atlas_Brainnetome246Ext` | 256 | anatomical L/R | sensitivity |
| `atlas_AICHA384Ext` | 394 | anatomical | archived |
| `atlas_Gordon333Ext` | 385 | anatomical | archived |
| `atlas_AAL116` | 116 | anatomical | coarse anchor |

## 3. Connectivity variants (per atlas, per subject)

1. `sift_radius2_count_connectivity` — **PRIMARY weight**
2. `sift_invnodevol_radius2_count_connectivity` — sensitivity
3. `radius2_count_connectivity` — sensitivity
4. `radius2_meanlength_connectivity` — sensitivity

Structural facts verified: all matrices symmetric (0 asymmetric entries); diagonals
mostly nonzero (must be zeroed before graph construction); off-diagonal raw
densities AAL116 0.879 / Brainnetome246Ext 0.747 / 4S456 0.543; strengths span
orders of magnitude (4S456 median 14.2k, p95 35.2k) → cost thresholding required.

## 4. Provenance status

- [x] Byte-size vs Zenodo API: 10/10 MATCH
- [x] Zip CRC (`testzip`): 10/10 clean
- [x] SHA-256 recomputed and recorded: `00_Metadata\CHECKSUMS_AOMIC.sha256`
- [x] Verification report: `00_Metadata\AOMIC_VERIFICATION_REPORT.md`
- [x] Catalog/README/ACQUISITION_REPORT addenda written (2026-09-22)
- [x] Safety policy: RAW untouched; no deletes; G: untouched

## 5. Existing scripts

None yet in `13_CROSS_SPECIES_CIS\` — only planning documents
(`STUDY_DESIGN.md`, `RESEARCH_LOG.md`, `README.md`) and the directory skeleton.
E01 pipeline is the first code to be written (after the freeze).

## 6. Existing study-design decisions (from STUDY_DESIGN.md v1.0 — unchanged)

- Exact CIS (no source panels; n ≤ 456 makes exactness cheap) — same frozen
  definition as the fly study, upgraded from panel-BFS to exact.
- Proportional (cost) thresholding per subject; primary 15%; ladder {10, 20, 25}%.
- Atlas ladder: 4S456 primary + AAL116 anchor; 4S256/4S156/B246 sensitivity;
  AICHA/Gordon archived.
- Statistics: L1 within-subject → L2 across subjects → L3 degree-preserving
  nulls (decisive arbiter) → L4 cross-scale synthesis (CP03/CP05 rules).
- QC: flag, never delete; exclusion rules must be CIS-blind.
- Log discipline: append-only; manuscript numbers traceable to frozen artifacts.

## 7. Drosophila quantities available for comparison (READ-ONLY, `G:\fruitfly`)

Verified present this session; only these frozen artifacts will be read in P7:

| Artifact | Path | Frozen content relevant to cross-scale synthesis |
|---|---|---|
| E10B final | `results\final\e10b_final.json` | 100 degree-preserving nulls; observed Cliff's δ = 0.0979 vs null 0.0713±0.0220; z = 1.21; empirical p(δ) = 0.109; p(median diff) = 0.782; `all_nulls_degree_verified: true` — the **null-survival template** |
| E12-strong | `results\tables\e12_strong_results.json` | Top-K system enrichment with tested-universe control (A) and per-slot degree-matched control (B): K=50 obs 21, E(B)=7.98, z_B=5.30, p_B=1e-4, enrichment 2.63×; K=25 → 2.47× (z=3.26); K=100 → 2.15× (z=4.93) |
| E14-v2 catalogue | `results\tables\e14_chokepoint_catalogue_v2.csv` (50 rows) | Per-node columns: cis, total/in/out degree, emp_p_degree_matched, peer_pool_n, peer_median_cis, cis_excess_ratio, class_label — the **per-node residual template** |
| Metric definition | `results\final\FINAL_REPORT.md` §6 | CIS(i) = 1 − S(G−i)/S(G), freeze-N convention, unweighted shortest paths |

Comparison categories (pre-declared): fly quantities enter only as
**distributional/normalized** comparators (enrichment ratios, z-scores,
null-survival patterns, residual-vs-degree structure). No raw-CIS numeric
comparison (node counts 456 vs 138,584; weights streamlines vs synapses).

## 8. Unresolved issues (carried forward, none blocking the freeze)

1. Kudriavtsev 2026 bioRxiv (ageing lesion + nulls): full text 403 from this
   network — **pre-submission gate**, re-verify before manuscript (E00 boundary).
2. Dedicated 2025–26 preprint sweep with the exact query set — pre-submission gate.
3. Atlas dictionary: full name→key mapping from the Zenodo description must be
   extracted in E01 from the archived record JSON (partially read in audit).
4. The 100 missing subject IDs: excluded upstream by AOMIC QC; reason unknown;
   documented, no rescue (no-guessing rule).
5. `networkx` 3.6.1 is installed but will NOT be used (fly convention: scipy only).

## 9. Environment (verified this session)

Python 3.13.2, Windows 11 (10.0.26200), numpy 2.4.2, pandas 2.3.3,
scipy 1.18.0, pyarrow 23.0.1, matplotlib 3.11.2. Full manifest to be written
by E01 into `00_MANIFEST\ENVIRONMENT_MANIFEST.txt`.

## Verdict

**PHASE 0.5 EXIT: PASS.** All Part-2 audit items satisfied; nothing modified;
proceed to Phase 1 (PROTOCOL_FREEZE.md) before any computation.
