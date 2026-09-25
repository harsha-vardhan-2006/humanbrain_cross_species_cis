# Data Availability Statement

**Primary human data.** All structural connectomes analyzed in this study are
publicly available and were used unmodified:

- AOMIC-ID1000 standardized structural connectivity mapping
  (900 subjects × 7 atlases × 4 connectivity variants), Zenodo record
  **19796783**, DOI 10.5281/zenodo.19796783, license **CC-BY-4.0**.
  Byte-exact local verification against the Zenodo API is documented
  (`00_Metadata/AOMIC_VERIFICATION_REPORT.md`; SHA256 checksums in
  `00_Metadata/CHECKSUMS_AOMIC.sha256`).

**Reference (fly) data.** The frozen fly study's published result artifacts
(FAFB v783, FlyWire/Princeton release; Dorkenwald et al. 2024) were read as
normalized comparators only. FAFB v783 is publicly available via FlyWire
(CC BY-NC 4.0); the fly repository is
github.com/harsha-vardhan-2006/fruitfly_paper (release tag v1.0.0).

**Derived data.** All derived matrices, per-subject CIS tables, null-network
CIS matrices, manifests, and checksums are included in the repository and in
the release archive `cross_species_cis_v1.0.0.zip`
(SHA256 in `dist/SHA256SUMS_cross_species_cis.txt`), with the exception of
regenerable intermediate caches (`cache_parts/`, reproducible via
`02_PREPROCESSING/preprocess_v2.py`).
