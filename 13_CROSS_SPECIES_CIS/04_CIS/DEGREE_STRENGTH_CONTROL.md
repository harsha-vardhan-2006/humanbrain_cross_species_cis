# DEGREE/STRENGTH CONTROL (E03b) — frozen protocol §3

Cohort: 801 QC-pass subjects; 36846 matched pairs (top CIS decile per subject; ±10% degree, 1:1 greedy; 1068 nearest-50 fallback rows).

| quantity | value |
|---|---|
| residual CIS (obs − control), median across subjects | 5.97e-05 |
| residual IQR | [3.54e-05, 8.66e-05] |
| subjects with positive median residual | 778/801 (sign test p=2.64e-197) |
| mean fraction of pairs beating control | 0.588 |
| Cliff's δ (median across subjects) | 0.100 |
| subjects with Wilcoxon p<0.05 | 125/801 |

Interpretation rule (frozen): degree matching is a necessary but not
sufficient control — the decisive arbiter is the degree-preserving
null battery (E04/E05). Positive residuals indicate CIS structure
beyond degree at FIXED topology; the null battery tests structure
beyond degree at RANDOMIZED topology.

Reproducible via: py 04_CIS/degree_control.py
