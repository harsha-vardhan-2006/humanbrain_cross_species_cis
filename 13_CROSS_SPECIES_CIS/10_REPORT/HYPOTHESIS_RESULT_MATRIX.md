# HYPOTHESIS–RESULT MATRIX (final, locked 2026-09-26)

Status values are the pre-registered resolutions; negative results are NOT
converted to positive claims.

| # | Hypothesis / question | Result | Evidence (artifact) | Status |
|---|---|---|---|---|
| H1 | Does top-50 CIS concentration exceed degree-preserving null expectations? | Yes — 200/200 subjects above null; median z = 16.36; two-sided sign p = 1.24e-60 | `null_results_battery_b.csv`; RESOLUTION.md R1 | **SUPPORTED** |
| H2 | Does a degree-independent residual remain after degree/strength adjustment? | Yes — residual > 0 in 778/801 subjects (sign p = 2.6e-197); Cliff's δ = 0.100 [0.078–0.129]; 43/456 nodes survive FDR | `degree_strength_control_summary.json`; `table_07_null_results.csv`; R2a | **SUPPORTED** |
| H3 | Is the residual robustly system-specific? | No — R2b NEGATIVE: no pre-specified sensory/visual system enriched (Vis z_B = −0.38); only Subcortical/Cerebellar nominal (z_B 2.08, p .031, 1.25×) and absent at K=25 (z_B 0.81); FDR cluster degree-anchored | `e05_statistics.json` K=25/50; RESOLUTION.md R2b | **NOT SUPPORTED** |
| H4 | Does comparable control-impact architecture appear across fly and human scales? | Architectural similarity with anatomical divergence — δ 0.100 (human) vs 0.0979 (fly, itself NOT null-surviving, p=0.109); both degree-dominated; human residual not visual (2% vs fly 80%); no homology claimed | `table_09_cross_scale.csv` (DIRECT rows); CROSS_SCALE_ANALYSIS.md | **SUPPORTED (architecture only)** |

## Guardrails (binding interpretation)
1. H3 stays negative: the subcortical/cerebellar signal is reported as
   degree-anchored concentration, **not** a system-specific mechanism.
2. No mechanism claim: the study establishes an architectural/statistical
   pattern, not a causal biological process.
3. No homology claim: cross-scale rows are normalized comparators only
   (DIRECT/NORMALIZED/QUALITATIVE tags, CP03/CP05).
4. The fly–human δ similarity is reported as interesting but **partly
   fortuitous** (different units of analysis, graphs, and designs; the fly
   δ did not survive its own null ensemble).
5. The residual's existence (H2) is distinct from its interpretation (H3):
   support for H2 does not soften H3.
