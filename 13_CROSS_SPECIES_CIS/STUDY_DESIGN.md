# STUDY DESIGN — Cross-Scale Control Impact: Human Structural Connectomes (AOMIC-ID1000) vs Fly (FAFB v783)

**Version:** 1.0 (2026-09-22, design draft — nothing executed, nothing pre-registered yet)
**Workspace:** `D:\HumanBrain\13_CROSS_SPECIES_CIS\` (new tree; RAW zips in `12_HumanConnectome_AOMIC\zenodo_19796783_raw\` remain READ-FOREVER, all outputs go under `13_`)
**Predecessor:** frozen fly study `fruitfly/` (scientific freeze commit `fdfafe5`, release tag v1.0.0) — **READ-ONLY reference; no artifact of that repository may be modified.**
**Status of this document:** proposal. Phases below only start after P0 (novelty gate) and a user-approved freeze of the pre-registration.

---

## 0. One-paragraph motivation

The fly project's decisive lesson was methodological: a striking matched-pair effect
(GABA δ = 0.111, p = 0.0011) **died inside a degree-preserving null ensemble**
(p = 0.109 / 0.782), while a different signal — visual-centrifugal chokepoint
architecture, 2.6× enrichment after degree matching — survived. Its two biggest
documented limitations are (a) one brain, one reconstruction, no replication, and
(b) structural CIS is a computational metric with no population-level support.
The AOMIC-ID1000 structural-connectome derivative (900 subjects × 7 atlases) now
sits verified on disk and directly addresses both: it turns "chokepoint analysis"
from an n=1 case study into a population-level, multi-scale, testable framework —
and creates the first legitimate cross-scale bridge under the comparability rules
already recorded in `00_Metadata\cross_species_manifest.json` (CP03/CP05:
APPROXIMATELY_COMPARABLE; no homology claims).

---

## 1. Data inventory (verified on disk 2026-09-22)

Source: Zenodo record **19796783** — *"Standardized structural connectivity
mapping of the AOMIC-ID1000 dataset: A multi-scale tractography resource"*
(DOI 10.5281/zenodo.19796783, license **CC-BY-4.0** — attribution required,
commercial use permitted, no share-alike clause; cite the record + AOMIC ID1000,
OpenNeuro ds003097).

| Property | Value (verified locally, not assumed) |
|---|---|
| Files | 10 × `connectomes_part_N.zip` in `12_HumanConnectome_AOMIC\zenodo_19796783_raw\` |
| Byte size vs Zenodo API | 10/10 exact match |
| Zip internal CRC (`testzip`) | 10/10 clean |
| Total | 7,067,175,601 B (6.58 GiB) |
| Members | 900 × `sub-XXXX_run-1_space-T1w_connectivity.mat`, 90 per zip, 0 duplicates |
| Subjects | 900 unique IDs; 100 IDs absent from 1..1000 (excluded upstream by AOMIC QC — do NOT chase) |
| Per-mat content | 7 atlases × (region_ids + region_labels + 4 connectivity matrices) + `command` provenance string |

**Atlases** (all present in every .mat, verified in sub-0001):

| Atlas | Nodes | Labels carry network/system names? |
|---|---|---|
| 4S456Parcels | 456 | YES (Schaefer-style: Vis 61, SomMot 77, DorsAttn 46, SalVentAttn 47, Limbic 26, Cont 52, Default 91, subcortical…) ← **primary atlas** |
| 4S256Parcels | 256 | YES |
| 4S156Parcels | 156 | YES |
| Brainnetome246Ext | 256 (246 + ext) | L/R anatomical names only |
| AICHA384Ext | 394 | anatomical |
| Gordon333Ext | 385 | anatomical |
| AAL116 | 116 | anatomical ← **coarse/robustness anchor** |

**Connectivity variants per atlas** (all symmetric float64; verified densities:
AAL116 0.879, Brainnetome246Ext 0.747, 4S456 0.543 off-diagonal > 0):

- `sift_radius2_count_connectivity` — SIFT-filtered streamline counts → **primary weight**
- `sift_invnodevol_radius2_count_connectivity` — volume-corrected → sensitivity
- `radius2_count_connectivity` — unfiltered counts → sensitivity
- `radius2_meanlength_connectivity` — mean streamline length → sensitivity

Non-negotiable processing facts (verified): matrices are **symmetric** (0 asymmetric
entries), diagonals are mostly nonzero (must be zeroed), strengths span orders of
magnitude (4S456 median 14.2k, p95 35.2k) → proportional thresholding is required.

---

## 2. Research question

> Do region-level structural chokepoints (per-node control impact, CIS) in the
> human connectome exceed what degree predicts — and does any residual impact
> concentrate in specific functional systems — consistently across 900 subjects
> and 3 parcellation scales? Where the fly showed degree-dominated control with
> a visual-centrifugal residual, does the human brain show the same two-layer
> structure?

This is a **replication-and-bridge** study, not a hunt for a new fly hypothesis:
the fly result fixes the *prediction* (Outcome-B pattern: degree explains most of
CIS; residuals, if any, are system-structured, with sensory/visual systems the
pre-specified candidates). A confirmatory result is as publishable as a
disconfirming one — the fly paper demonstrated that standard.

---

## 3. Design decisions (fixed here so they can't drift post hoc)

1. **Exact CIS, not panels.** At n ≤ 456, per-node removal global efficiency is
   exactly computable: 456 BFS per subject-atlas ≈ seconds in scipy. The fly
   estimator (fixed-source-panel) exists in `fruitfly/src/` and will be ported
   with `panel(k=N) ≡ exact` — so the metric is *the same frozen definition*
   (CIS = 1 − S(G−i)/S(G), freeze-N convention), upgraded to exactness.
   Diagonals zeroed; graph treated as **undirected weighted** (matrices are
   symmetric — a documented modality difference vs the fly digraph; a directed
   variant is impossible, not skipped).
2. **Threshold policy — proportional (cost) thresholding, per subject.**
   Raw densities (0.54–0.88) are incompatible with meaningful path-length
   metrics. Primary: keep top **15%** of off-diagonal weights per subject
   (cost-matched across subjects, standard practice); sensitivity ladder
   {10%, 20%, 30%}. Frozen before E03.
3. **Atlas ladder = the scale axis.** Primary: 4S456 (system labels) +
   AAL116 (coarse anchor). Secondary/sensitivity: 4S256, 4S156,
   Brainnetome246Ext. AICHA/Gordon: archived, unused unless a reviewer asks.
   This mirrors the fly k-ladder logic (k8→k16→k32) with data instead of panels.
4. **Primary weight** = `sift_radius2_count`; the other three are pre-declared
   sensitivity weights. All thresholds pre-declared; no post-hoc atlas shopping.
5. **Statistics — four levels (the fly pipeline, ported and extended):**
   - **L1 within-subject:** exact CIS per node; CIS~degree Spearman; residual CIS
     (OLS on log-strength + degree, per subject).
   - **L2 across subjects:** per-node mean residual CIS > 0 across 900 subjects
     (one-sample t / Wilcoxon, BH-FDR **within** atlas×weight stratum); system
     aggregates from label prefixes (Vis/SomMot/…), permutation tests with
     subject-level labels (10,000 reps — same machinery as fly E12-strong).
   - **L3 degree-preserving nulls (the decisive arbiter, fly E10B pattern):**
     per-subject Maslov–Sneppen configuration-model rewires (exact degree
     preservation verified per null — ported from `fruitfly/src/experiments/null_models.py`
     and its adversarial tests), 100 nulls × representative subject sample
     (n=100 subjects, stratified), full-ensemble for finalists. Per-node z vs
     null; verdict rule pre-locked like Gate 4: **a residual claim survives only
     if it beats the degree-preserving null ensemble**, not merely the OLS control.
   - **L4 cross-scale synthesis (CP03/CP05 rules):** system-level comparison only
     (fly visual-centrifugal ↔ human Vis-network residual share); explicitly
     NO region homology claims; fly artifacts read via their frozen JSON/CSV only.
6. **QC gates before any science (E01 exit criteria):** all 900×7 extractions
   parse; per-subject density/strength distributions reported; subjects failing
   pre-set QC (e.g., density > 3 IQR from atlas median, zero rows, NaN) go to a
   `qc_flagged` table — **never deleted** (workspace no-delete policy applies).
7. **Compute budget:** trivial. Full L1+L2 ≈ minutes-to-hours CPU; L3 nulls the
   only non-trivial piece (bounded: 100 subjects × 100 nulls × 456-node graphs ≈
   low CPU-hours). No cloud, no GPU.
8. **Provenance discipline (inherited, binding):** RAW zips never modified;
   every script under `13_\src\` + `13_\logs\`; append-only `RESEARCH_LOG.md`
   in this folder; every manuscript number traceable to a frozen artifact file;
   verification-only re-runs safe by design.

---

## 4. Phases

| Phase | Content | Exit criterion |
|---|---|---|
| **P0 — Novelty gate** | Structured lit sweep: per-node *removal-based* CIS/efficiency-drop in human macro-connectomes (vs the adjacent Betzel/Bassett *controllability*, de Reus rich-club, lesion-gradient literatures); check the exact four-way combination: removal-CIS + degree-matched controls + degree-preserving nulls + N≥100 population. Verdict written into RESEARCH_LOG before any run. | novelty verdict recorded, four-way gap confirmed or claim re-bounded |
| **P1 — E01 pipeline** | Extract all 900 .mat → tidy per-subject parquet/npz under `13_\data\processed\`; atlas dictionary (incl. the Zenodo description's name→key mapping — archive the full record description); QC tables; SHA256 manifest for the 10 zips (also backfills the acquisition-report gap). | 900×7 parse clean; QC report + manifest in `13_\results\` |
| **P2 — E02 baseline** | Per-atlas density/strength/degree distributions across subjects; threshold curves (efficiency vs cost) → sanity-check the 15% choice; figures. | baseline tables + 2 QA figures |
| **P3 — E03 exact CIS** | All subjects × primary atlas×weight; finalists atlas ladder; residualization. | CIS tables per subject |
| **P4 — E04 nulls + L2 tests** | Degree-preserving null battery; system-level enrichment; pre-locked verdict rules applied. | Gate: residual claims stand or fall vs nulls |
| **P5 — E05 robustness** | Weight variants × cost ladder × atlas ladder concordance (Jaccard of top-K sets, sign stability); QC-flagged-subject exclusion sensitivity. | robustness table, honest-gap list |
| **P6 — E06 cross-scale synthesis** | Fly frozen artifacts (VC catalogue, E10B stats) ↔ human system residuals; comparability-tagged outputs only. | synthesis report; manuscript decision at review |

Pre-registration freeze (hypotheses H1/H2 wording, primary atlas/weight, verdict
rules) happens **once, between P0 and P1**, mirroring the fly v2 freeze discipline.

---

## 5. Risks / honest limitations (pre-declared)

- **Parcel ≠ neuron.** Region-level CIS measures parcel-lesion impact; the
  cross-scale comparison is architectural, not cellular (CP03 tag: APPROXIMATELY).
- **Symmetric/directed mismatch** with the fly digraph — reported, not hidden.
- **Tractography weights are reconstruction-dependent** (QSIprep/MRtrix3 SIFT);
  bias vs the fly's EM synapse counts is structural. The multi-weight + multi-cost
  design is the mitigation.
- **Degree will likely dominate again** (that is the *prediction*, not a failure).
- **The 100 missing subject IDs** are unknown-reason exclusions upstream; no
  rescue attempt (would violate the no-guessing rule).
- **Population covariates (age/sex/motion) are not in this derivative**; any
  demographic claim is out of scope. AOMIC ID1000 raw (OpenNeuro ds003097) would
  be a separate acquisition decision.

---

## 6. Deliverables

`13_\results\` tables/figures; `13_\RESEARCH_LOG.md` (append-only); final report in
the house style; optional manuscript only if the Gate verdict is informative in
either direction. All fly-repo citations point at the frozen release tag.
