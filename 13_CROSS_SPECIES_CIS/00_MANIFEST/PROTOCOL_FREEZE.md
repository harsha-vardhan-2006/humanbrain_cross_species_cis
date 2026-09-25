# PROTOCOL FREEZE — Cross-Scale Control-Impact Study

**Freeze date: 2026-09-22. This document is frozen BEFORE any CIS computation
(Parts 9–14 of the execution prompt). No value below may change after results
are observed. Changes require a new dated addendum section + RESEARCH_LOG entry,
and the primary analysis can never be re-specified post hoc.**

## 1. Primary analysis (frozen)

| Item | Frozen value |
|---|---|
| Primary atlas | `atlas_4S456Parcels` (456 nodes; system labels available) |
| Primary connectivity representation | `sift_radius2_count_connectivity` |
| Primary perturbation | single-node removal, one node at a time, node restored after each measurement |
| Primary outcome | change in whole-network global efficiency |
| Primary cost threshold | **15% network cost** (proportional threshold: keep the top 15% of off-diagonal weights by magnitude, per subject, per matrix) |
| Sensitivity cost ladder | 10%, 15% (primary), 20%, 25% |
| Subject unit | the individual subject is the primary statistical unit; no subject pooling into group graphs for the primary analysis |

Rationale recorded in `STUDY_DESIGN.md` §3 and `CURRENT_STATE_AUDIT.md` §2–3;
selection is justified by the audit (highest-resolution atlas with system labels;
SIFT = bias-corrected streamline counts; 15% as the pre-declared middle rung of
the ladder) — none of these values may be re-tuned after seeing CIS results.

## 2. Exact CIS definition (frozen)

For subject s, atlas a, weight w, cost c:

1. Zero the diagonal of the raw matrix A; take W = symmetrized upper triangle
   (matrices verified symmetric; symmetrization is then exact).
2. Cost(c): binarize by keeping the top ⌊c·N(N−1)/2⌋ off-diagonal entries by
   weight; G = binary undirected graph on that edge set (weights enter ONLY
   through the threshold selection step; efficiency is computed on the binary
   graph — the fly-frozen convention, applied to undirected data as documented
   in STUDY_DESIGN §3.1).
3. Global efficiency: E(G) = (1/(N(N−1))) Σ_{i≠j} 1/d(i,j), d = unweighted
   shortest-path distance; pairs in different components contribute 0.
4. **CIS(i) = (E(G) − E(G − i)) / E(G)**  (freeze-N convention; identical to
   the fly-frozen definition CIS(i) = 1 − S(G−i)/S(G)).
   Range [0, 1]; removing an isolated node yields CIS = 0 by definition.
5. E(G) and each E(G−i) computed EXACTLY (BFS from every node; scipy.sparse.csgraph).
   No source panels. Optimized implementations must pass the reference-
   implementation validation (Part 9) before any production run.

Reported alongside, never substituted: weighted-strength diagnostics; and as a
sensitivity metric (clearly labeled exploratory): reachability drop.

## 3. Degree / strength control (frozen)

Per subject (primary atlas × weight × 15% cost):
1. For every node record: degree (binary, post-threshold), strength (raw SIFT
   count sum of the node's retained edges), and CIS.
2. Matching rule (inherited from the frozen fly protocol): for each node in the
   top CIS decile of that subject, draw degree-matched controls within ±10% of
   total degree, 1:1 greedy, WITHOUT replacement, from the same subject's graph.
3. Where the ±10% pool is empty, fall back to the 50 nearest-degree nodes and
   flag the row (`match_type=nearest50`).
4. Outcome per matched comparison: observed CIS, control CIS distribution,
   residual CIS (obs − control median), effect size (Cliff's δ), Wilcoxon
   signed-rank p, and the subject-level count of nodes beating their matched
   controls.
5. Degree matching alone is NEVER treated as sufficient evidence: the decisive
   arbiter is the degree-preserving null battery (§4).

## 4. Degree-preserving null models (frozen)

- Construction: Maslov–Sneppen double-edge swaps on the binary thresholded
  graph, exact in+out (in undirected case: exact degree sequence) preservation
  VERIFIED per null; rejection redraw for failed repairs. Ported from
  `fruitfly/src/experiments/null_models.py` semantics, adapted to undirected
  graphs, with the fly project's adversarial regression tests (hub-selfloop,
  dense, ring) re-run on the undirected variant before production.
- N nulls: **100** per analyzed graph.
- Scope (compute-bounded, fixed now): null battery on (a) the primary
  configuration for a subject sample of n=100 (seeded subject selection
  documented in the null manifest) for per-node empirical p across the
  population; (b) 200 random subjects × top-50 CIS nodes only, for the
  population-level summary statistic; (c) full 900-subject nulls are NOT
  pre-registered — they may be added later only as clearly-labeled
  exploratory extension.
- Seeds: nulls 100+i per graph; subject-sample seed 20260922; all recorded.
- Verdict rule (pre-locked, Gate-4 pattern): a residual-architecture claim
  SURVIVES only if the observed statistic exceeds the 95th percentile of its
  degree-preserving null ensemble (empirical p < 0.05 after the §6 correction);
  failure ⇒ Result B framing for that claim.

## 5. QC rules (frozen, CIS-blind)

Flag, never delete. A subject×atlas×variant matrix is FLAGGED if any:
- dimensions ≠ atlas expected size; NaN or Inf entries > 0;
- asymmetry beyond float tolerance (|A − Aᵀ| > 1e-9 relative);
- negative off-diagonal weights;
- post-threshold graph has >1 connected component containing >1 node;
- zero-row/zero-column nodes after thresholding;
- density or mean strength > 3 IQR from the atlas-level median (per variant).

Exclusion policy: the primary analysis cohort = subjects whose PRIMARY
configuration (4S456 × sift count) passes all checks. Sensitivity analyses
report both full-cohort and QC-pass-cohort results. No subject is excluded
based on any CIS-derived quantity, ever.

## 6. Statistical strategy (frozen)

- Population tests: one-sample Wilcoxon / t on per-node or per-subject
  statistics across subjects; permutation tests with subject-level label
  shuffling (10,000 reps) for system-level enrichment (fly E12-strong template:
  control A = tested universe, control B = degree-matched expectation, z_B).
- Multiple comparisons: Benjamini–Hochberg FDR (q = 0.05) WITHIN each
  stratum (atlas × variant × cost rung); the primary claim is evaluated on the
  single primary configuration (no correction needed there beyond the null
  ensemble rule).
- Bootstrap CIs: 1,000-resample subject-level bootstrap for population CIS
  summaries.
- Reproducibility metrics: per-node Spearman rank stability across random
  subject splits (median of 100 split halves, seed 20260922).

## 7. Outcome classes (frozen, mirrors execution-prompt Part 23)

- **RESULT A** — residual control-impact architecture survives degree/strength
  matching, degree-preserving nulls, atlas/weight/cost robustness, and
  subject-level replication.
- **RESULT B** — apparent architecture is substantially explained by
  degree/strength/topology (the fly study's own Outcome-B precedent).
- **RESULT C** — mixed: survives some pre-declared controls, fails others;
  boundary conditions documented.
The result class is selected ONLY after E03–E05 complete, in
`10_REPORT\FINAL_RESULT_DECISION.md`.

## 8. Cross-scale comparison rules (frozen)

Categories never blurred: (i) DIRECT (defined identically on both systems:
e.g., null-survival pattern, rank-vs-degree residual structure);
(ii) SCALE-NORMALIZED (enrichment ratios, z-scores, concentration indices);
(iii) QUALITATIVE (architectural descriptions). No anatomical homology claims.
Fly side reads ONLY: `e10b_final.json`, `e12_strong_results.json`,
`e14_chokepoint_catalogue_v2.csv`, `e14_top50_region_mapping.csv`
(paths in CURRENT_STATE_AUDIT §7). Fly repo stays frozen.

## 9. Reproducibility requirements (frozen)

Every experiment logs: date, script + version, git commit if available, Python
+ package versions, seeds, subject count, atlas, variant, cost, null count,
execution time, output path. ENVIRONMENT_MANIFEST.txt generated at E01. All
figures/tables regenerable by script from frozen artifacts.

## 10. Validation of this freeze

- [x] All values specified before any CIS computation (no CIS code exists yet)
- [x] Consistent with STUDY_DESIGN.md v1.0 (no scientific decision changed)
- [x] Consistent with execution-prompt Parts 4–6, 12, 19, 23
- [x] Fly quantities pinned to specific frozen files
- [x] Ambiguities resolved by explicit choice and recorded (binary-graph
      efficiency convention; null compute scope; nearest-50 fallback)

**FREEZE COMPLETE — 2026-09-22. E01 (data extraction + QC) may begin.**
