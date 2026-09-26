# Code Availability Statement

All analysis code is publicly available at
**github.com/harsha-vardhan-2006/humanbrain_cross_species_cis**
(release tag v1.0.0; also archived as `cross_species_cis_v1.0.0.zip` with
recorded SHA256). **License: MIT** (see `LICENSE` at the repository root;
covers the repository's code and documentation — underlying third-party
data remain under their own terms, see the Data Availability Statement).

Key components (single-source-of-truth implementations, frozen):

| Component | Path |
|---|---|
| Graph math / threshold / exact CIS / fast CIS | `13_CROSS_SPECIES_CIS/02_PREPROCESSING/cache_io.py` |
| Extraction & QC | `13_CROSS_SPECIES_CIS/02_PREPROCESSING/preprocess_v2.py` |
| Null battery (Maslov–Sneppen, verified) | `13_CROSS_SPECIES_CIS/05_NULLS/degree_preserving/null_models.py` |
| Statistics (Stouffer/FDR/enrichment/rank stability) | `13_CROSS_SPECIES_CIS/04_CIS/e05_statistics.py` |
| Degree/strength matching | `13_CROSS_SPECIES_CIS/04_CIS/degree_control.py` |
| Robustness ladder | `13_CROSS_SPECIES_CIS/06_ROBUSTNESS/robustness.py` |
| Cross-scale synthesis | `13_CROSS_SPECIES_CIS/07_CROSS_SCALE/cross_scale.py` |
| Figures / tables / harvest | `08_FIGURES/make_figures.py`, `09_TABLES/build_tables.py`, `10_REPORT/fill_report.py` |
| Independent numeric audit (stdlib-only) | `13_CROSS_SPECIES_CIS/10_REPORT/verify_final_numbers.py` |

Environment: Python 3.13; numpy 2.4.2; scipy 1.18.0; pandas 2.3.3 (see
`ANALYSIS_FREEZE.md` for the disclosed ENVIRONMENT_MANIFEST provenance gap).
Every reported number is recomputable via the audit script without any
package dependency; full pipeline reproduction instructions are in the
supplementary material (§S14).
