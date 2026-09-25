# NULL MODEL REPORT (degree-preserving battery)
Generated 2026-09-26 00:35. Frozen protocol: PROTOCOL_FREEZE §4; rules never amended.

## Implementation validation
- node_cis_fast vs scipy node_cis reference: max deviation 4e-16 (real
  subject graphs), validated BEFORE any null compute
  (FAST_IMPLEMENTATION_VALIDATION.md).
- Maslov-Sneppen undirected port passes the adversarial regression suite
  (hub-selfloop/pendant, dense, ring).

## Battery A (per-node arbiter)
- 100 subjects x 100 nulls = 10000/10000 null graphs.
- Exact per-node degree preservation: 100.00%; edges match:
  100.00%; self-loops: 0.
- Seeds 100+i per graph; rejection redraw on preservation failure
  (acceptance 49.4% of attempted swaps). *[Corrected 2026-09-26: this line
  originally read "7694144.8%" — a unit error in the harvest script that
  printed the accepted-swap COUNT (mean ≈ 76,941 per null) as a percentage.
  True rate ≈ 49.4% of the 155,610 attempted swaps per null (15,561 edges ×
  10× swap factor). Fix applied in fill_report.py; underlying manifest and
  validation data unchanged.]*
- Mean CIS runtime 56.2s/null (matmul implementation).
- Outputs: battery_a/sub-XXXX_nulls.npz, null_manifest_battery_a.csv,
  null_validation_battery_a.csv.

## Battery B (top-50 concentration, n=200)
- Per-subject z and empirical p vs 100 nulls; battery-A reuse for
  overlapping subjects (identical seeds; recorded per subject in
  null_source). Aggregate: null_results_battery_b.csv.

## Outcome of arbitration
- R1 POSITIVE; R2a POSITIVE
  (43 nodes q<.05); R2b NEGATIVE.
- Verdict: Layer-1 replicated (concentration exceeds degree-preserving nulls); layer-2 null evidence absent or not system-structured -> weaker bridge, honest report per the frozen matrix.
