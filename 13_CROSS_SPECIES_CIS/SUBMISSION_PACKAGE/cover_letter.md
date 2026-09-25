# Cover Letter — draft for author review

Dear Editors,

We submit our manuscript, "Control-impact architecture of the human
structural connectome: degree dominance, a small universal residual, and a
cross-scale architectural comparison with the fly connectome," for
consideration as a research article.

**What we did.** Using the population-scale AOMIC-ID1000 structural-connectome
resource (900 subjects acquired; 801 QC-pass; 456-node parcellation), we
computed the exact removal-based Control Impact Score (CIS) for every node in
every subject, and asked — with degree-matched controls and degree-preserving
null networks — whether anything beyond degree survives, and whether it
resembles the architecture we previously documented at cell resolution in the
frozen fly (FAFB v783) connectome study.

**Principal findings.**

1. Top-50 CIS concentration exceeds degree-preserving null expectations in
   200/200 subjects (median z = 16.36; two-sided sign p = 1.24 × 10⁻⁶⁰).
2. CIS is strongly degree-dominated (median ρ = 0.943), yet a small
   degree-independent residual is present in 778/801 subjects
   (Cliff's δ = 0.100; sign p = 2.6 × 10⁻¹⁹⁷), and 43/456 nodes survive
   BH-FDR q < .05.
3. The residual is **not** robustly system-specific: the pre-registered
   system-enrichment gate was negative; the single nominal signal
   (subcortical/cerebellar) is degree-anchored and does not replicate at
   K = 25.
4. Compared with the fly study (δ = 0.0979), the human architecture is
   concordant in effect size and degree dominance, while the residual's
   anatomical identity diverges sharply (2% visual in human vs 80%
   visual-centrifugal in fly): **the architecture replicates; the anatomy
   does not.**

**Why it matters.** The contribution is empirical, statistical, architectural,
cross-scale, and methodological. We claim **no** new biological mechanism, no
anatomical homology, and no universal law; individual methods are established,
and the contribution is the bounded combination with pre-registered
arbitration. A methodological lesson generalizes across scales: matched-pair
significance can dissolve in degree-preserving nulls, while degree-matched
residuals survive — both layers of control are necessary.

**Rigor and reproducibility.** The full pipeline is frozen and audited:
42/42 independent numeric checks recompute every reported value from frozen
artifacts; null networks verify exact degree preservation per null
(10,000/10,000); implementations are cross-validated to machine precision;
robustness spans 9 atlas/weight/cost configurations. The complete
reproducibility package is publicly available
(github.com/harsha-vardhan-2006/humanbrain_cross_species_cis); data are
public (Zenodo 19796783, CC-BY-4.0).

This manuscript is not under consideration elsewhere. All authors have
approved the submission.

Sincerely,
Harsha Vardhan Malipeddi
(on behalf of the authors)
