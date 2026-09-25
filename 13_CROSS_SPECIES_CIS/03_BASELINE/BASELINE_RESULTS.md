# BASELINE RESULTS (E02) — intact networks before perturbation

Configuration: sift_radius2_count (PRIMARY weight), proportional cost
threshold, ladder {10, 15, 20, 25}%; binary undirected graphs;
efficiency on unweighted shortest paths (PROTOCOL_FREEZE §2).
Cohort: 900 subjects × 7 atlases (25,200 thresholded graphs).

## 1. Primary configuration (4S456 × sift count × 15% cost)

- Global efficiency: median 0.5468, IQR [0.5441, 0.5497]
- Mean degree: mean 68.2 (SD 0.0); edges median 15561
- Giant component: median fraction 1.0000 (graphs with giant_frac<1: 94/900)

## 2. Atlas × cost structure

| atlas | GE median @15% | GE IQR | mean degree | edges med | giant med |
|---|---|---|---|---|---|
| atlas_4S156Parcels | 0.5154 | [0.5093, 0.5205] | 23.3 | 1814 | 0.9808 |
| atlas_4S256Parcels | 0.5345 | [0.5314, 0.5373] | 38.2 | 4896 | 0.9961 |
| atlas_4S456Parcels | 0.5468 | [0.5441, 0.5497] | 68.2 | 15561 | 1.0000 |
| atlas_AAL116 | 0.4809 | [0.4729, 0.4882] | 17.2 | 1000 | 0.9655 |
| atlas_AICHA384Ext | 0.5417 | [0.5389, 0.5438] | 58.9 | 11613 | 1.0000 |
| atlas_Brainnetome246Ext | 0.5302 | [0.5281, 0.5325] | 38.2 | 4896 | 1.0000 |
| atlas_Gordon333Ext | 0.5483 | [0.5462, 0.5506] | 57.6 | 11088 | 1.0000 |

### Cost ladder (4S456, GE median)

| cost | 10% | 15% | 20% | 25% |
|---|---|---|---|---|
| GE | 0.4911 | 0.5468 | 0.5877 | 0.6203 |

## 3. QC gate (CIS-blind, PROTOCOL_FREEZE §5)

- QC PASS: 801/900 subjects (flagged: 99)
- Flag counts: flag_density_iqr=0, flag_strength_iqr=5, flag_components=0, flag_isolated=94
- Flags are recorded, never deletions; QC-pass cohort is used for the
  primary analysis, and sensitivity analyses report both cohorts.

## 4. Notes

- All 25,200 raw matrices passed structural QC (0 NaN/Inf, 0 dim
  mismatches, 0 asymmetry > 1e-9, 0 negative off-diagonals) — see
  01_RAW_PROBES/raw_flags.json.
- Post-threshold isolated nodes (94 subjects) are the dominant flag:
  expected at 15% cost in sparse parcellations; CIS(i)=0 is forced for
  isolated i by definition, and these subjects remain in the QC-pass
  cohort unless the frozen >1-multi-node-component rule triggers
  (0 subjects).

Reproducible via: py 03_BASELINE/baseline_report.py
