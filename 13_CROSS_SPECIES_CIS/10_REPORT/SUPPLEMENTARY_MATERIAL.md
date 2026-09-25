# SUPPLEMENTARY MATERIAL — Cross-Species CIS Study (v1.0, 2026-09-26)

Each section either contains the content inline or points to the frozen
artifact that contains it (append-only; nothing regenerated).

## S1. Dataset provenance
Zenodo 19796783 (AOMIC-ID1000 structural connectomes), CC-BY-4.0; 10 zips,
7,067,175,601 B, byte-exact vs API; CRC clean; 900 subjects × 7 atlases × 4
variants. Verification: `../00_Metadata/AOMIC_VERIFICATION_REPORT.md`;
checksums: `../00_Metadata/CHECKSUMS_AOMIC.sha256`. Raw zips READ-FOREVER.

## S2. QC rules
Pre-registered property-based QC (E02, CIS-blind): dimension mismatch, NaN,
Inf, asymmetry > 1e-9, negative off-diagonals, isolated nodes, strength IQR,
density IQR, multi-component (>1 non-trivial component). Cohort: 801/900 pass;
94 isolated-node + 5 strength-IQR flags; flagged subjects retained, never
deleted. Artifacts: `03_BASELINE/qc_primary.csv`, `BASELINE_RESULTS.md`,
`01_RAW_PROBES/raw_qc_report.csv`.

## S3. CIS mathematical definition
CIS(i) = (E(G) − E(G−i)) / E(G); E(G) = (1/(N(N−1))) Σ_{i≠j} 1/d(i,j) on the
binary undirected thresholded graph; E(G−i) on the induced (N−1)-node
subgraph ((N−1)(N−2) normalization). Exact computation (scipy Dijkstra);
reference-vs-naive validation 6.1e-16
(`04_CIS/REFERENCE_IMPLEMENTATION_VALIDATION.md`); boolean-matmul fast path
used only for null graphs, equivalence-gated at 1e-9 (max dev 4e-16;
`05_NULLS/degree_preserving/FAST_IMPLEMENTATION_VALIDATION.md`).
Implementation: `02_PREPROCESSING/cache_io.py` (single source of truth).

## S4. Null-model algorithm
Undirected Maslov–Sneppen double-edge swaps: canonicalized edge list
(deduplicated symmetric orientations), n_swaps = 10 × |E| attempts per null,
rejecting self-loops, duplicates, degenerate picks; exact per-node degree
verification per null (10,000/10,000 exact; 0 self-loops); rejection redraw
(max 5 attempts). Adversarial regression suite (hub-selfloop/pendant, dense
p=0.6, ring): `regression_tests_undirected.csv/.json`.

## S5. Degree/strength matching
±10% total degree, 1:1 greedy, no replacement; nearest-50 fallback flagged
per pair. 36,846 degree-matched node pairs (top-decile CIS nodes vs matched
controls). Residual defined as observed minus matched-control CIS;
strength association reported alongside (ρ(CIS,strength) median 0.486).
Artifacts: `04_CIS/degree_control.py`, `degree_strength_control_summary.json`,
`DEGREE_STRENGTH_CONTROL.md`.

## S6. Threshold parameters
k = round(c · N(N−1)/2) largest |off-diagonal| weights; diagonal zeroed;
binary output. Primary c = 0.15 (k = 15,561); ladder {0.10, 0.20, 0.25}.
Rationale: raw densities 0.45–0.88 preclude unthresholded path-length
statistics (STUDY_DESIGN §3.2). GE ladder at 4S456: 0.4911/0.5468/0.5877/
0.6203.

## S7. Statistical tests
- Battery B: per-subject z vs null distribution of top-50 median CIS;
  population two-sided sign test (binomial).
- Battery A: per-node empirical one-sided p with add-one correction
  (p = (#{nulls ≥ obs}+1)/(100+1)) → Stouffer z (Σz/√n_subjects) → BH-FDR
  q < .05 (single stratum).
- Enrichment: control A = node-label shuffle (10,000 perms); control B =
  degree-matched peer pools resampled 10,000×; z and empirical p with
  add-one floor.
- Rank stability: 100 seeded half-splits, Spearman of mean-CIS ranks.

## S8. FDR procedure
Benjamini–Hochberg over 456 node p-values (single stratum = primary
configuration), q = 0.05; 43 survivors; censored nodes (all-null ≥ observed;
413 nodes) carry p = 1 and Stouffer z = −inf by construction.

## S9. Robustness configurations
9 conditions on frozen n=150 cohort: atlases {4S256, 4S156, Brainnetome246Ext,
AAL116}, weights {sift_invnodevol, radius2_count}, costs {0.10, 0.20, 0.25}.
All top-50 means within 0.0026 of primary (like-for-like primary row in
RESOLUTION.md). Artifact: `06_ROBUSTNESS/`, `09_TABLES/table_08_robustness.csv`.

## S10. Seeds
Subject samples: one RNG, seed 20260922, nested samples (A ⊂ B). Nulls:
100 + i per graph. Enrichment/rank-stability: 20260922. All recorded in
`null_manifest_battery_a.csv` and script constants.

## S11. Additional distributions
- Null δ/z distributions: `battery_a/*.npz` (100 × 456 null-CIS matrices per
  subject), `null_results_battery_b.csv` (per-subject null mean/sd).
- Per-subject CIS: `04_CIS/subject_cis/sub-XXXX.csv` (456 rows each, 900 files).
- Baseline: `09_TABLES/table_baseline_network_properties.csv`.

## S12. Anatomical mapping
`00_MANIFEST/manifests/atlas_4S456_system_labels.csv` (456 nodes; Vis 61,
SomMot 77, DorsAttn 46, SalVentAttn 47, Limbic 26, Cont 52, Default 91,
Subcortical_Cerebellar 56). Human chokepoint catalogue:
`07_CROSS_SCALE/human_chokepoint_catalogue.csv`.

## S13. Literature novelty matrix
`10_LITERATURE/NOVELTY_MATRIX.md` (+ Kudriavtsev gate record:
`10_LITERATURE/KUDRIAVTSEV_2026_FULLTEXT_REVIEW.md`).

## S14. Reproducibility instructions
1. `git clone` the repository (heavy data excluded; raw zips from Zenodo).
2. Run `02_PREPROCESSING/preprocess_v2.py` (rebuilds `cache_parts/`,
   resume-safe) → `03_BASELINE/baseline.py` → `04_CIS/cis_primary.py` →
   `05_NULLS/degree_preserving/null_models.py --battery a|b` →
   `04_CIS/e05_statistics.py` → `06_ROBUSTNESS/robustness.py` →
   `09_TABLES/build_tables.py` → `08_FIGURES/make_figures.py`.
3. Numeric audit without any recomputation:
   `python 10_REPORT/verify_final_numbers.py` (stdlib-only; 42 checks).
4. Environment: Python 3.13, numpy 2.4.2, scipy 1.18.0, pandas 2.3.3
   (see ANALYSIS_FREEZE.md provenance-gap note).
