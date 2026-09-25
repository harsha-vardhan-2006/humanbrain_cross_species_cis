# SUBMISSION PACKAGE — README (index and build instructions)

Assembled 2026-09-26. All statements reference frozen artifacts; placeholders
are marked **[PLACEHOLDER]** and must be completed by the author before
submission (nothing is fabricated).

## Contents
| File | Purpose | Status |
|---|---|---|
| `cover_letter.md` | venue-agnostic factual cover letter | READY (author review) |
| `highlights.md` | 6 highlight bullets | READY |
| `graphical_abstract_description.md` | designer brief for the graphical abstract | READY |
| `author_contributions.md` | CRediT statement | PLACEHOLDERS (author) |
| `data_availability.md` | data provenance + licenses | READY |
| `code_availability.md` | code paths + environment | READY |
| `reproducibility_statement.md` | audit summary + disclosed gaps | READY |
| `conflict_of_interest.md` | COI declaration | PLACEHOLDER (author) |
| `ethics_statement_if_applicable.md` | secondary-data use note | PLACEHOLDER (author) |
| `novelty_statement.md` | bounded novelty claim | READY (pending Kudriavtsev full-text read) |
| `JOURNAL_OPTIONS.md` | venue scope/policy table (no ranking) | READY (verify APCs at submission) |
| `manuscript.md` | copied final manuscript | READY (source for typesetting) |

## Building manuscript.pdf / .docx
`pandoc` was not installed on the working machine, so rendering was NOT
executed here (do not claim otherwise). On any machine with pandoc + LaTeX:

```bash
pandoc 10_REPORT/MANUSCRIPT_FINAL.md -o manuscript.docx
pandoc 10_REPORT/MANUSCRIPT_FINAL.md -o manuscript.pdf \
  --pdf-engine=xelatex -V geometry:margin=1in
```

Supplementary: `10_REPORT/SUPPLEMENTARY_MATERIAL.md` renders the same way.
Figures: `08_FIGURES/*.png|pdf` (provenance: `10_REPORT/FIGURE_PROVENANCE.md`;
Figure 5 anatomical distribution renders from frozen `table_07` + label
manifest at typesetting time).

## Pre-submission checklist (human)
1. Kudriavtsev 2026 full-text read; co-sign the gate record.
2. Fill [PLACEHOLDER]s: contributions, COI, ethics/IRB note, affiliation.
3. Render PDF/DOCX; attach figures per FIGURE_PROVENANCE.
4. Verify current APC/policies of the chosen venue (JOURNAL_OPTIONS notes).
5. Post bioRxiv preprint (optional; after step 1).
