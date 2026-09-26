# REPRODUCIBILITY — Cross-Species Control-Impact Study

**Created:** 2026-09-26 (final packaging phase). Maps the full pipeline
DATA → PREPROCESSING → QC → CIS → NULLS → RESIDUAL → STATISTICS → FIGURES →
TABLES → MANUSCRIPT, with scripts, inputs, outputs, parameters, and seeds.
Complements: `10_REPORT/ANALYSIS_FREEZE.md` (frozen parameters),
`10_REPORT/SUPPLEMENTARY_MATERIAL.md` (S1–S14), `FINAL_REPRODUCIBILITY_AUDIT.md`
(46/46 numeric checks).

## 1. Environment (verified from `00_MANIFEST/ENVIRONMENT_MANIFEST.txt`)

- Python 3.13.2, Windows 11 AMD64
- numpy 2.4.2 · scipy 1.18.0 · pandas 2.3.3 · pyarrow 23.0.1 · matplotlib 3.11.2
- CPU-only. No GPU required. Peak RAM concern is the extraction stage
  (worker-per-zip design, ~1 zip in memory at a time).
- Provenance note: the original `ENVIRONMENT_MANIFEST.txt` was reconstructed
  from run logs after the v1→v2 pipeline transition (disclosed in
  ANALYSIS_FREEZE.md); the file on disk contains the E01/E01v2 generation
  records with matching version strings.

## 2. Pipeline map (scripts are read-only truth; run order matters)

| Stage | Script (relative to `13_CROSS_SPECIES_CIS/`) | Input | Output | Key parameters / seeds |
|---|---|---|---|---|
| DATA acquisition | (acquisition tooling, `99_Logs/`) | Zenodo 19796783 | `../12_HumanConnectome_AOMIC/zenodo_19796783_raw/` (10 zips, READ-FOREVER) | SHA256 in `../00_Metadata/CHECKSUMS_AOMIC.sha256` |
| PREPROCESSING | `02_PREPROCESSING/preprocess_v2.py` (+ `cache_io.py` = frozen math) | 10 raw zips | `02_PREPROCESSING/cache_parts/cache_part_NN.npz` (10), `cache_keys.csv`, `raw_qc_report.csv`, `raw_flags.json` | 900 subj × 7 atlases × 4 variants; symmetric matrices, diagonals zeroed; resume-safe per zip |
| QC / BASELINE | `03_BASELINE/baseline.py`, `baseline_report.py` | cache parts | `03_BASELINE/baseline_network_properties.csv`, `qc_primary.csv`, `BASELINE_RESULTS.md` | cost ladder {10,15,20,25}%; QC gate CIS-blind; cohort 801/900 fixed at E02 |
| CIS | `04_CIS/cis_primary.py` | cache parts | `04_CIS/subject_cis/sub-XXXX.csv` (900), `e03_summary.json`, `population_cis_summary.csv` | exact CIS = (E(G) − E(G−i))/E(G), binary undirected, all 456 nodes/subject; reference validated 6.1e-16 |
| DEGREE CONTROL | `04_CIS/degree_control.py` | subject_cis | `degree_strength_control_results.csv` (36,846 pairs), `degree_strength_control_summary.json`, `DEGREE_STRENGTH_CONTROL.md` | ±10% degree, 1:1 greedy, nearest-50 fallback flagged |
| NULLS | `05_NULLS/degree_preserving/null_models.py --battery a\|b` | cache parts (subject samples) | `battery_a/*.npz` (100 subj × 100 nulls), `null_results_battery_b.csv` (200 subj × 100 nulls), manifests + `null_validation_battery_a.csv` | Maslov–Sneppen undirected; exact per-node degree verification per null; null seeds 100+i; subject-sample seed 20260922 (nested A⊂B); rejection redraw max 5 |
| STATISTICS | `04_CIS/e05_statistics.py` | battery A/B outputs, degree-control summary | `e05_statistics.json`, `table_07_null_results.csv` | per-node empirical p (add-one) → Stouffer → BH-FDR q<.05; battery-B z + two-sided sign test; enrichment controls A/B, 10,000 perms; rank stability 100 half-splits (seed 20260922) |
| ROBUSTNESS | `06_ROBUSTNESS/robustness.py` | cache parts | `06_ROBUSTNESS/`, `table_08_robustness.csv` | 9 configs (4 atlases × 2 weights × 3 costs), n=150 frozen cohort |
| CROSS-SCALE | `07_CROSS_SCALE/cross_scale.py` | human E03/E03b/E05 + frozen fly artifacts (`e10b_final.json`, `e12_strong_results.json`, `e14_v2_summary.json`) | `table_09_cross_scale.csv`, `CROSS_SCALE_ANALYSIS.md` | normalized comparators only (DIRECT/NORMALIZED/QUALITATIVE); no absolute CIS across species |
| FIGURES | `08_FIGURES/make_figures.py`, `make_fig05_anatomical.py` | frozen outputs | `08_FIGURES/fig01–fig09` (+ `fig05_fdr_anatomical.*`) | PNG 300 dpi + PDF; no manual edits |
| TABLES | `09_TABLES/build_tables.py` | frozen outputs | `09_TABLES/table_01–table_10` | — |
| HARVEST/GATES | `10_REPORT/fill_report.py` | chain artifacts | `RESOLUTION.md`, gated manuscript clauses (fill-only) | refuses partial artifacts; stamped |
| FINAL AUDIT | `10_REPORT/verify_final_numbers.py` | frozen artifacts | stdout (44 checks) | stdlib-only; read-only |

## 3. Exact commands (Python ≥3.13 with the versions above)

```bash
# 0) obtain raw data (public, CC-BY-4.0): Zenodo record 19796783 (10 zips)
#    place under 12_HumanConnectome_AOMIC/zenodo_19796783_raw/ and verify:
sha256sum -c 00_Metadata/CHECKSUMS_AOMIC.sha256

# 1) extraction + QC (resume-safe; regenerates cache_parts/)
python 02_PREPROCESSING/preprocess_v2.py

# 2) baseline + QC gate
python 03_BASELINE/baseline.py && python 03_BASELINE/baseline_report.py

# 3) exact per-subject CIS (all 900 subjects)
python 04_CIS/cis_primary.py

# 4) degree/strength-matched controls (E03b)
python 04_CIS/degree_control.py

# 5) null batteries (A: 100 subj x 100 nulls full CIS; B: 200 subj x 100 top-50)
python 05_NULLS/degree_preserving/null_models.py --battery a
python 05_NULLS/degree_preserving/null_models.py --battery b

# 6) statistics (FDR, enrichment, rank stability)
python 04_CIS/e05_statistics.py

# 7) robustness ladder (9 configs)
python 06_ROBUSTNESS/robustness.py

# 8) tables + figures
python 09_TABLES/build_tables.py
python 08_FIGURES/make_figures.py
python 08_FIGURES/make_fig05_anatomical.py

# 9) cross-scale synthesis (requires frozen fly artifacts at ../fruitfly/)
python 07_CROSS_SCALE/cross_scale.py

# 10) numeric audit WITHOUT recomputation (stdlib-only, read-only)
python 10_REPORT/verify_final_numbers.py
```

## 4. Runtime expectations (from the logged runs)

- Extraction (10 zips, 25,200 matrices): ~1–2 h wall (8 workers; resume-safe)
- Exact CIS per subject: ~15–100 s depending on estimator; full cohort ran
  overnight across workers
- Null battery A: ~28 min/subject single-core (chunked, resumable); battery B
  reuses battery-A nulls for the 100 shared subjects
- Statistics/robustness/figures/tables: minutes
- Numeric audit: seconds (stdlib-only, read-only)

## 5. Reproduction status

- The frozen artifacts in this repository ARE the outputs of the pipeline
  above; no output is hand-edited (documented exceptions: two 2026-09-26
  documentation corrections, flagged inline and logged in RESEARCH_LOG).
- `verify_final_numbers.py` (44 checks) recomputes every headline number from
  the frozen artifacts: **44/44 PASS** (2026-09-26).
- Fly-side artifacts live in the separate frozen `fruitfly` repository
  (release v1.0.0); the human tree reads only their result JSON/CSV files.
- The release archive `dist/cross_species_cis_v1.0.0.zip` excludes
  `cache_parts/` (4.0 GB, regenerable) and quarantines by design; its
  SHA256 is pinned in `dist/SHA256SUMS_cross_species_cis.txt` (verified OK
  2026-09-26).
