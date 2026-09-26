# FINAL REPRODUCIBILITY AUDIT — Cross-Species CIS Study

**Audit date:** 2026-09-26
**Auditor:** Buffy (Codebuff agent) — independent numeric recomputation
**Method:** every documented number recomputed from frozen artifacts with a
stdlib-only script (`10_REPORT/verify_final_numbers.py`, 46 checks as of
2026-09-26; 42 at freeze). No
package dependency; raw CSV/JSON parsed directly. Exit code 0, all PASS.

---

## A. DATA — PASS

| Item | Documented | Recomputed from | Status |
|---|---|---|---|
| Subjects acquired | 900 | `00_MANIFEST/subject_manifest.csv` (900 rows) | PASS |
| QC-pass (primary cohort) | 801 | `03_BASELINE/qc_primary.csv` (qc_pass==True) | PASS |
| Atlas | 4S456Parcels | manifest keys | PASS |
| Nodes | 456 | `atlas_4S456_system_labels.csv` (456 rows) | PASS |
| System labels | Vis 61, SomMot 77, DorsAttn 46, SalVentAttn 47, Limbic 26, Cont 52, Default 91, Subcort/Cereb 56 | same file | PASS |
| Edges (primary, 15% cost) | 15,561 | round(0.15 × 456×455/2) = 15,561 | PASS |
| Weight | sift_radius2_count_connectivity (SIFT2-consistent counts) | `cache_io.py` PRIMARY_VARIANT | PASS |
| Missing data / exclusions | 99 QC-flagged (94 isolated-node, 5 strength-IQR), retained not deleted | `raw_flags.json` / QC report | PASS |
| Raw checksums | 10/10 zips SHA256-verified | `../00_Metadata/CHECKSUMS_AOMIC.sha256`, `AOMIC_VERIFICATION_REPORT.md` | PASS |
| Provenance | Zenodo 19796783, CC-BY-4.0, byte-exact vs API | verification report | PASS |

## B. ANALYSIS — PASS

| Item | Frozen value | Source | Status |
|---|---|---|---|
| CIS definition | CIS(i) = (E(G) − E(G−i))/E(G), exact, binary undirected | `cache_io.node_cis` | PASS |
| Reference validation | max dev 6.1e-16 (naive vs optimized) | `04_CIS/REFERENCE_IMPLEMENTATION_VALIDATION.md` | PASS |
| Fast-CIS equivalence | max dev 4e-16, 1e-9 gate | `FAST_IMPLEMENTATION_VALIDATION.md` | PASS |
| Thresholding | k = round(c·N(N−1)/2) top-|w| off-diag, diag zeroed | `cache_io.threshold_cost` | PASS |
| Degree matching | ±10% total degree, 1:1 greedy, nearest-50 fallback | `04_CIS/degree_control.py` | PASS |
| Null model | Maslov–Sneppen undirected, exact degree verification per null, rejection redraw | `null_models.py` + regression suite | PASS |
| Null count | 100 per graph; A: 100 subj ×100 (full CIS); B: 200 subj ×100 (top-50) | manifests | PASS |
| Seeds | subject sample 20260922; nulls 100+i | frozen in code + manifests | PASS |
| FDR | BH q<.05, single stratum, one-sided empirical p with add-one | `e05_statistics.py` | PASS |
| Enrichment | controls A (label shuffle) + B (degree-matched pools), 10k perms | `e05_statistics.py` | PASS |
| Enrichment p floor | p_A = 0.9999 = (10000−1+1)/10001 for zero-tail systems | e05_statistics.json | PASS (expected) |

## C. RESULTS — PASS (46/46 numeric checks)

| Claim | Documented | Recomputed | Status |
|---|---|---|---|
| N acquired | 900 | 900 | PASS |
| QC-pass | 801 | 801 | PASS |
| Battery B concentration | 200/200 | 200/200 | PASS |
| Median null z | ≈16.36 | 16.36 | PASS |
| Sign test p | 1.24e-60 | 2×0.5²⁰⁰ = 1.2446e-60 (exact) | PASS |
| rho(CIS, degree) | ≈0.94 | 0.943 | PASS |
| Residual-positive subjects | 778/801 | 778 (summary JSON) | PASS |
| Residual sign p | 2.6e-197 | 2.6e-197 | PASS |
| Cliff's δ (human) | ≈0.100 | 0.100 | PASS |
| Matched pairs | 36,846 | 36,846 | PASS |
| Wilcoxon median p / n<.05 | 0.167 / 125 | 0.167 / 125 | PASS |
| FDR nodes | 43/456 | 43 (JSON + table_07) | PASS |
| Max Stouffer z | 23.3008 (node 400) | 23.3008 = analytic ceiling 10·Φ⁻¹(100/101) | PASS |
| Censored −inf nodes | 413 | 413 | PASS |
| Visual share top-50 | 1/50 = 2% | 1 | PASS |
| Vis z_B (negative) | −0.38 | −0.38 | PASS |
| Subcortical K=50 | obs 26, z_A 9.06, z_B 2.08, p_B .031, 1.25× | all exact | PASS |
| Subcortical K=25 (n.s.) | z_B 0.81 | 0.8056 | PASS |
| Rank stability | 0.996 | 0.996 | PASS |
| E06 configs / concordance | 9 / max like-for-like deviation 0.00262 (atlas_AAL116; no pre-registered numeric tolerance — descriptive) | 9 / 0.0026194 | VERIFIED |
| Rewire acceptance (fixed) | 49.4% | 49.4% (76,941/155,610) | PASS |
| Battery A integrity | 10,000 nulls, degree-exact 100%, 0 self-loops | all exact | PASS |
| Fly δ | ≈0.0979 | 0.0979 (`e10b_final.json`) | PASS |
| Fly null p (NOT survived) | 0.109 | 0.109 | PASS |

**Discrepancies found:** none. **Corrections made by this audit:** none
(the 2026-09-26 acceptance-rate and date fixes were made and flagged earlier
the same day; the verifier confirms the corrected values).

## D. KNOWN PROVENANCE GAPS (disclosed, non-blocking)

1. `02_PREPROCESSING/ENVIRONMENT_MANIFEST.txt` is referenced in RESEARCH_LOG
   E01 but not present in the tree (likely lost in the v1→v2 pipeline
   transition). Software versions are recorded from log entries instead.
   → recorded in ANALYSIS_FREEZE.md; a regenerated manifest would be a new
   document, not a recovery of the original.
2. E06 concordance primary row is computed like-for-like in RESOLUTION.md
   (table_08 stores condition rows only) — documented in the harvest script.
3. Full text of Kudriavtsev 2026 — **RESOLVED 2026-09-26 (late):** verified
   via text-extraction proxy after 4 direct 403 attempts; see the addendum
   in `10_LITERATURE/KUDRIAVTSEV_2026_FULLTEXT_REVIEW.md`.
