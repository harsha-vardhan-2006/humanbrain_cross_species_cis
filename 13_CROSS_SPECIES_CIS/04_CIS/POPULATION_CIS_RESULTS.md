# POPULATION CIS RESULTS (primary configuration)
Generated 2026-09-26 00:35. Artifacts: e05_statistics.json,
09_TABLES/table_population_cis_summary.csv, 09_TABLES/table_07_null_results.csv.

- Cohort: 801 QC-pass subjects (primary atlas 4S456, cost .15).
- Rank stability (100 seeded half-splits): median Spearman
  0.996 [IQR 0.996-0.997].
- Spearman(CIS, degree) median 0.943;
  Spearman(CIS, strength) median 0.486.
- Per-node null arbitration: 43/456 nodes survive BH-FDR q<.05;
  max Stouffer z 23.30.

## Top-10 nodes by population-mean CIS
| node | mean CIS | top-50 rate |
|---|---|---|
| 414 | 0.00456 | 1.00 |
| 400 | 0.00429 | 1.00 |
| 415 | 0.00375 | 1.00 |
| 401 | 0.00342 | 1.00 |
| 451 | 0.00206 | 0.99 |
| 442 | 0.00199 | 0.99 |
| 444 | 0.00182 | 0.99 |
| 286 | 0.00145 | 0.70 |
| 97 | 0.00122 | 0.97 |
| 432 | 0.00109 | 0.94 |

System identity and enrichment: see RESOLUTION.md and
05_NULLS/degree_preserving/NULL_MODEL_REPORT.md.
