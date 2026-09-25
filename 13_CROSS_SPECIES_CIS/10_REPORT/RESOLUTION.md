# RESOLUTION — pre-registered gates (appended to frozen decision)
Generated: 2026-09-26 00:35 · rules verbatim from REPORT_SCAFFOLD.md §1 (no amendments)

## Integrity audit (before any gate is read)
- battery A: 10000/10000 nulls, 100 subjects; degree preserved exactly for 100.00% of nulls; self-loops: 0; rewire acceptance 49.4% of attempted swaps *[corrected 2026-09-26: this line originally read "7694144.8%" — a unit error that printed the accepted-swap count as a percentage; underlying data unchanged; see RESEARCH_LOG corrections entry]*; mean CIS runtime 56.2s/null
- battery B: 200 subjects; null sources: {'fresh': 100, 'battery_a_reuse': 100}

## R1 — layer-1 (battery B, n=200)
- subjects with z_vs_null > 0: 200/200 (100.0%)
- sign test (two-sided) p = 1.245e-60; one-sided greater p = 6.223e-61 (reported for completeness)
- median z_vs_null = 16.358; frac emp_p<.05 = 100.0%
- **R1 = POSITIVE** (rule: majority positive AND two-sided p<.05)

## R2a — per-node Stouffer/BH-FDR (battery A)
- nodes with q_bh<0.05: 43/456; max Stouffer z = 23.30 (node 400); min p = 2.176e-120
- **R2a = POSITIVE** (rule: >=1 node survives q<.05)

## R2b — system enrichment z_B (K=50, pre-specified systems)
| system | observed | z_A | p_A | z_B | p_B | enrich_B |
|---|---|---|---|---|---|---|
| Vis | 1 | -2.52 | 0.9995 | -0.38 | 0.7754 | 0.69x |
| SomMot | 2 | -2.59 | 0.9989 | -1.63 | 0.9813 | 0.38x |
| DorsAttn | 3 | -1.03 | 0.9097 | -0.09 | 0.6296 | 0.96x |
| SalVentAttn | 8 | 1.40 | 0.1292 | -0.50 | 0.7524 | 0.86x |
- **R2b = NEGATIVE** (rule: z_B>0 for >=1 pre-specified sensory/visual system at K=50)

## Supporting statistics (frozen E05 outputs)
- rank stability (100 half-splits): median Spearman 0.996 [IQR 0.996-0.997]
- Spearman(CIS, degree) median 0.943; Spearman(CIS, strength) median 0.486
- battery B summary: median z 16.357927087338044, sign p 1.2446030555722283e-60

## E06 concordance (primary row computed like-for-like on the same cohort)
- primary (4S456, sift_r2count, cost .15, n=150): top50 mean 0.0012, gini median 0.4916, rho(CIS,deg) median 0.941
        condition  n_subjects  top50_mean  top50_delta_vs_primary  gini_median  gini_delta_vs_primary  rho_cis_degree_median  rho_delta_vs_primary
          cost_10         150    0.001564                0.000335      0.52647                0.03486                 0.8978               -0.0429
          cost_20         150    0.001029               -0.000200      0.47547               -0.01614                 0.9791                0.0385
          cost_25         150    0.000926               -0.000302      0.45767               -0.03395                 0.9950                0.0544
      atlas_4S256         150    0.001887                0.000658      0.50955                0.01794                 0.9422                0.0015
      atlas_4S156         150    0.003179                0.001951      0.56178                0.07017                 0.9566                0.0159
       atlas_B246         150    0.001704                0.000476      0.45887               -0.03274                 0.9463                0.0057
     atlas_AAL116         150    0.003848                0.002619      0.53892                0.04731                 0.9447                0.0040
weight_invnodevol         150    0.001187               -0.000042      0.48316               -0.00845                 0.9379               -0.0028
   weight_r2count         150    0.001254                0.000026      0.48526               -0.00635                 0.9489                0.0082

## VERDICT
Layer-1 replicated (concentration exceeds degree-preserving nulls); layer-2 null evidence absent or not system-structured -> weaker bridge, honest report per the frozen matrix.

Stamp: D:\humanbrain\humanbrain\13_CROSS_SPECIES_CIS\10_REPORT\_harvest_done.stamp
