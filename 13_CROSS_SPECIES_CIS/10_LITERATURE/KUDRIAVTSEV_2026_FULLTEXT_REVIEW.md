# KUDRIAVTSEV ET AL. 2026 — FULL-TEXT REVIEW RECORD (PRE-SUBMISSION GATE)

**Paper:** Kudriavtsev, N.; Rosso, M.; Fernandez-Rubio, G.; Serra, E.;
Kringelbach, M. L.; Vuust, P.; Bonetti, L. (2026-06-02). *Efficient ageing:
Simulated lesion of the structural connectome reveals optimised decline in the
healthy ageing brain.* bioRxiv 10.64898/2026.05.29.728718.

**Review date:** 2026-09-26 (gate attempts: 2026-09-22, 09-24, 09-26 ×2)
**Reviewer:** Buffy (Codebuff agent), on behalf of the project author.

---

## ACCESS RECORD (honest disclosure)

| Source | Date | Result |
|---|---|---|
| biorxiv.org full-text HTML (`v1.full`) | 09-22, 09-24, 09-26 | **403 Forbidden** (network-blocked) |
| biorxiv.org `v1.full-text` | 09-26 | **403 Forbidden** |
| biorxiv.org PDF (`full.pdf`) | 09-26 | **403 Forbidden** |
| preprints.epiforecasts.io mirror | 09-26 | **200 OK** — complete author abstract, full author list, record metadata |
| Search-index snippets (Google, multiple queries) | 09-24, 09-26 | fragments of abstract + PDF text; no methods body |
| PMC / Europe PMC / OSF mirrors | 09-26 | no deposit found (preprint-only, no journal version yet) |

**The full methods/results BODY of the paper was NOT accessible.** This review
is therefore an **abstract-plus-metadata verification**, not a full-text review.
No claim below relies on material beyond the verified abstract and record
metadata. Per project rules (execution rule 6), the paper is NOT recorded as
"read."

---

## WHAT IS VERIFIED (complete abstract, via mirror)

- Design: two independent healthy-cohort dMRI datasets (n = 144 total:
  77 + 67); TBSS fractional-anisotropy analysis identifies age-sensitive
  white-matter hotspots; probabilistic tractography builds connectomes.
- Intervention: **simulated lesions constrained by age-sensitive FA
  hotspots**, applied cross-dataset.
- Null comparator: **matched-mass null lesions** (lesions matched for
  lesion mass/volume, not for node degree).
- Main result: hotspot lesioning reduces global efficiency **less than the
  matched-mass null expectation** ("optimised decline"); proportional degree
  loss strongest at high-degree nodes; **rich-club connections most
  hotspot-dependent**; nodewise losses concentrated in frontal, cingulate,
  subcortical association systems; posterior sensory and temporo-limbic
  regions relatively spared.

---

## THE TEN REQUIRED QUESTIONS

Answers are based on the verified abstract + metadata only. Where the body
could in principle contain something the abstract does not mention, the answer
is marked "per abstract" and the residual risk is stated.

1. **Does the paper calculate node-level removal/control impact?**
   **Partially / not in our sense.** Lesions are hotspot-CONSTRAINED sets of
   connections/regions; nodewise loss is reported as an outcome. No per-node
   exhaustive removal ranking (CIS = 1 − E(G−i)/E(G) for every node) is
   mentioned. *(per abstract; residual risk: low)*
2. **Is the calculation performed per subject?**
   **Partially.** Two-dataset design (n = 144); results reported per dataset
   and jointly. Per-subject per-node vectors are not mentioned. *(per
   abstract)*
3. **Is there a population-level per-subject residual analysis?**
   **No.** No residual-to-degree construct appears in the abstract.
4. **Does it use degree/strength matching?**
   **No** — it uses **matched-mass** lesion nulls (volume-matched), which is a
   different control from degree-matched node controls. *(per abstract)*
5. **Does it use degree-preserving null networks?**
   **No.** The null is a lesion-placement null within the observed network,
   not a rewired degree-preserving null ensemble. *(per abstract; residual
   risk: low — abstract is explicit about the null type)*
6. **Does it test concentration against degree-preserving nulls?**
   **No.** It tests efficiency decline against matched-mass lesion nulls.
7. **Does it perform FDR node-level analysis comparable to ours?**
   **Not mentioned.** *(residual risk: moderate — common in neuroimaging
   papers; does not affect the combination claim by itself)*
8. **Does it perform a fly–human cross-scale comparison?**
   **No.** Human ageing cohorts only.
9. **Does it contain the same combination of methodological components?**
   **No.** Verified components: lesion simulation + efficiency + nulls +
   population n>100. Missing: exact per-node CIS per subject, degree-matched
   (not mass-matched) controls, degree-preserving null arbitration of a
   residual, cross-scale comparison.
10. **Overlap verdict:**
    **PARTIAL OVERLAP** (methods family: simulated lesions + global
    efficiency + null comparators in structural connectomes).
    **What remains distinct (our contribution):** the object of arbitration —
    a per-node, per-subject CIS **residual** (degree-independent component),
    arbitrated against **degree-preserving** null ensembles at population
    scale (N=801–900), with a pre-registered cross-scale bridge. Kudriavtsev
    et al. arbitrate *ageing decline* against *matched-mass* lesion nulls; we
    arbitrate *control-impact architecture* against *degree-preserving*
    nulls. The two studies ask different questions with overlapping tools.

---

## CONSEQUENCE FOR THE NOVELTY CLAIM

- The bounded novelty wording (NOVELTY_MATRIX.md) is **RETAINED UNCHANGED**.
- Preferred wording remains: *"To our knowledge, no prior study has combined
  these analyses in a per-subject population-scale human structural-connectome
  framework with a pre-registered cross-scale comparison."*
- **Remaining action before submission (human, one-time):** read the full text
  from any unblocked network/device (the bioRxiv page or the PDF) and confirm
  question 1–2 answers. Failure modes are bounded: the abstract's explicit
  null type (matched-mass) already rules out the decisive overlap component.
- This record was written by an automated agent from verified sources only;
  the human author should personally perform the final full-text read and
  co-sign this file (add a "Human verification" line) before submission.
