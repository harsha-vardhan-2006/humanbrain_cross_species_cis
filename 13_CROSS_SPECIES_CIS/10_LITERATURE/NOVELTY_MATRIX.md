# NOVELTY MATRIX — Cross-Species CIS Study (final, 2026-09-26)

Basis: project literature verification (E00 desk sweep, E00a primary-source
audit, E17 2025-26 sweep, E17a Kudriavtsev abstract-complete verification via
mirror). All rows reflect **verified** sources; "N/R" = not reported.

Legend: CIS = per-node removal-based control impact; per-subj = computed per
subject (not group average); pop = population-scale (N ≥ 100); deg-match =
degree-matched controls; str-match = strength matching; DP-null =
degree-preserving null ensemble; resid = degree-independent residual analysis;
FDR = node-level multiple-comparison control; cross = cross-scale comparison;
fly-hum = fly–human comparison.

| Study | Node-level CIS | per-subj | pop | deg-match | str-match | DP-null | resid | FDR | cross | fly-hum |
|---|---|---|---|---|---|---|---|---|---|---|
| Alstott et al. 2009 (PLoS Comput Biol) | Y (sequential + localized lesions) | N (5 subj, group avg) | N | N | N | N | N | N | N | N |
| Crossley et al. 2014 (Brain) | Y (degree-ordered attack; node drop defines hub) | N (56 subj, group avg) | partial (56) | N | N | N | N | N | N | N |
| Gu/Betzel/Bassett NCT (controllability) | N (different metric: average/modal controllability) | Y (small N) | partial | N | N | some | N | N | N | N |
| Yueh-Hsin et al. 2024 (Sci Rep 14:14573) | Y (multi-node adjacent resections; GE decline) | Y (80 adults) | partial (80) | N | N | N | N | N | N | N |
| Kudriavtsev et al. 2026 (bioRxiv, ageing lesions) | partial (hotspot-constrained lesions; nodewise loss as outcome) | partial (2 datasets, n=144) | Y (n=144) | N (**matched-mass** nulls) | N | N (lesion-placement null, not rewired) | N | N/R (abstract-only verified) | N | N |
| Debona 2026 (bioRxiv, Ollivier-Ricci) | N (curvature, not removal) | Y | partial | N | N | Y (double-edge swaps, standard) | N | N | N | N |
| Treeratana 2026 (bioRxiv, lesion materiality) | partial (lesion maps) | Y | partial | N | N | Y (normative-connectome nulls) | N | N | N | N |
| Fly predecessor (this project, FAFB v783) | Y (exact, 139,255 neurons) | n/a (one brain) | N (n=1) | Y | N | Y (100 nulls) | partial (E14 v2 per-node emp p) | N/A | Y (within-fly regions) | — |
| **THIS STUDY** | **Y (exact, all 456 nodes)** | **Y (801–900)** | **Y (900)** | **Y (±10%, 1:1)** | **Y (CIS~deg+str; strength assoc.)** | **Y (200×100 + 100×100, verified)** | **Y (OLS-style + matched controls, population map)** | **Y (BH-FDR, 456 tests)** | **Y (pre-registered)** | **Y (pre-registered, no-homology)** |

## Verdict

No verified prior study combines per-node CIS + per-subject computation +
population scale + degree/strength matching + degree-preserving null
arbitration + node-level FDR + cross-scale comparison. Kudriavtsev et al. 2026
is the closest neighbour on tools (lesions + efficiency + nulls) but differs
on the arbitrated object (ageing decline vs control-impact architecture) and
the null type (matched-mass vs degree-preserving) — see
`10_LITERATURE/KUDRIAVTSEV_2026_FULLTEXT_REVIEW.md` (PARTIAL OVERLAP; full
text still unread, residual risk documented).

**Canonical claim wording (use this, not "first ever"):**

> To our knowledge, no prior study has combined these analyses in a
> per-subject population-scale human structural-connectome framework with a
> pre-registered cross-scale comparison.

## 2026-09-26 updated sweep (post-freeze framing audit; append-only)

A fresh web sweep (Google-index queries: node-removal/GE + degree-preserving
nulls + population; Drosophila control-impact/chokepoint; cross-species
connectome architecture 2024–2026; NCT 2025–2026) found **no occupation of
the combination**. Three previously unrecorded adjacent works were found and
are recorded honestly:

1. **Yadav, Shinde & Singh 2025**, *Brain rewiring during development: A
   comparative analysis of larval and adult Drosophila melanogaster
   connectomes*, Network Neuroscience 9(4):1299–1322,
   doi:10.1162/netn.a.26 — uses degree-preserving random networks AND
   targeted attack in Drosophila connectomes (larval vs adult, n=1 per
   stage). **Overlap:** the fly-side tool pair (degree-preserving nulls +
   node removal). **Distinction:** no per-subject population framework, no
   degree-matched residual decomposition, no human cohort, no pre-registered
   cross-scale arbitration. This row WEAKENS any hypothetical claim that
   "degree-preserving nulls + node removal in a fly connectome" is
   unoccupied; the study's actual claim (the seven-element human
   population-scale combination, NOVELTY_AUDIT §2) is unaffected.
2. **Venkadesh et al. 2025**, *Directed connectomes across species reveal
   conserved and divergent pathways of neural signaling*, bioRxiv
   10.1101/2025.09.07.674762 (PMC12439989) — directed connectomes across
   mouse/marmoset/macaque/human via tracer polarity + dMRI; path-efficiency
   influence metrics. **Overlap:** cross-species structural comparison
   goal. **Distinction:** no node-removal CIS, no null-arbitrated residual
   decomposition, no fly–human pairing, no pre-registration of the present
   comparison. Confirms cross-species connectomics is an active field
   (supports the "not new" boundary, not a threat to the combination).
3. **Niyazmand et al. 2026** (Network Neuroscience / direct.ms —
   controllability-measure relationships across subjects) — confirms
   average-controllability/connectivity coupling; adjacent NCT metric
   family, no node removal. No threat.

Also re-verified: the Yueh-Hsin et al. 2024 record resolves to Lin,
Yueh-Hsin et al., "Discernible interindividual patterns of global efficiency
decline during theoretical brain surgery", Sci Rep 14:14573,
doi:10.1038/s41598-024-64845-4 (PMC11196730) — consistent with the E17
assessment (per-subject resection GE decline; no matching/nulls/residual
ranking).

**Updated verdict:** the bounded novelty wording is RETAINED. The matrix
rows above are extended by the three works; none occupies the seven-element
combination (see `10_REPORT/NOVELTY_AUDIT.md` §6). Kudriavtsev full-text
read remains the pre-submission condition.

## Pre-submission conditions
1. Human full-text read of Kudriavtsev 2026 (gate record co-signed).
2. If any future full-text read reveals per-subject population CIS-residual
   arbitration with degree-preserving nulls, this matrix and the manuscript
   gap statement must be revised (append-only).
