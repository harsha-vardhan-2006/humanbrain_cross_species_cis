# REFERENCE IMPLEMENTATION VALIDATION (E03)

Date: 2026-09-23 01:15:41
Frozen tolerance: max|CIS_ref - CIS_fast| < 1e-9 and |E0_ref - E0_fast| < 1e-12.
Reference: naive per-removal all-pairs recomputation with scalar efficiency sums; Optimized: cache_io.node_cis.

| subject | max abs dev | E0 ref | E0 fast | pass |
|---|---|---|---|---|
| 1 | 2.005e-16 | 0.553957008 | 0.553957008 | True |
| 3 | 6.072e-16 | 0.548533192 | 0.548533192 | True |
| 4 | 4.014e-16 | 0.553238866 | 0.553238866 | True |

**VALIDATION: PASS** on 3 subject graphs (primary configuration).

Production run gated on this validation per PROTOCOL_FREEZE.
