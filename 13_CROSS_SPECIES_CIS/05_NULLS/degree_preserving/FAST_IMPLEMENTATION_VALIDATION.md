# FAST CIS IMPLEMENTATION VALIDATION (E04)

Date: 2026-09-25 17:47:41
node_cis (scipy all-pairs; used for all OBSERVED results) vs
node_cis_fast (boolean-matmul all-pairs; used for NULL graphs).
Frozen tolerance: max|dCIS| < 1e-9, |dE0| < 1e-12.

| subject | max abs dev CIS | abs dev E0 | pass |
|---|---|---|---|
| 1 | 4.009e-16 | 0.000e+00 | True |
| 3 | 4.048e-16 | 0.000e+00 | True |
| 4 | 4.014e-16 | 0.000e+00 | True |

**VALIDATION: PASS**
