# Google Sites → GitHub Pages

The existing AcademicPages/Jekyll site contains the migrated website, published
through the repository's existing GitHub Pages build from `master`. The Google
Site and custom-domain settings are managed separately and have not been changed.

## Migrated content

- All 56 publications from the Google Sites research page, in the original order.
- All 92 original resource links, plus six recovered links verified against primary sources.
- Complete author lists, venues, award text, and equal-contribution markers.
- 105 news entries; eight appear initially and earlier news expands on the homepage.
- Six current Ph.D. students, two current M.S. students, six alumni, the group
  support statement, and five courses.
- Updated advisor links, prospective-student instructions, and social profile links.

## Updating publications

Edit `_data/publications.json`, then run from the repository root:

```sh
python3 scripts/generate_publications.py
python3 scripts/generate_publications.py --check
python3 scripts/verify_migration.py
bundle exec jekyll build
```

Each record contains separate `title`, `authors`, `year`, `venue`, and `links`
fields. `year` is the verified publication year when a final record is available,
and the preprint year otherwise. The archive groups papers by this year, then
uses the original `order` within each year. IDs and permalinks remain stable
when a paper is accepted in a later year. Resource labels retain their meaning:
code is never stored as slides.
The generator writes the individual `_publications` documents. Their URLs remain
stable; six former malformed author-name documents redirect to the correct papers.

The generator also creates BibTeX from each paper's metadata. Conference years
come from the venue when the homepage's year grouping differs. Equal-contribution
markers and award/presentation notes stay in the displayed citation, while the
BibTeX uses clean author and venue fields. An optional `bibtex` field can retain
an official entry verbatim. Each paper page shows its BibTeX; the publications
archive provides a disclosure and copy button for every entry.

The original importer and generator entry points now use the new workflow.
The old TSV/notebooks are historical and are no longer the source of truth.

`migration/google-sites-publications.json` preserves the original citation text
and links for a complete comparison. `migration/publication-overrides.json`
records reviewed corrections and the primary sources supporting them. To repeat
the Google Sites import from a downloaded research page:

```sh
python3 scripts/import_google_sites.py /path/to/research.html
python3 scripts/generate_publications.py
```

Normal future edits only require the generator. Re-importing replaces the Google
Sites entries with the source content plus reviewed overrides, and retains papers
added separately from other sources.

New papers can use the primary paper page for `source_url` and retain the supplied
citation in `source_citation`. A lower `order` value appears earlier; EliteReplay,
added after migration, uses `-1` so the original 56 records remain unchanged.

## Selected research

`_data/selected_research.json` chooses the homepage papers and figure assets.
Titles, venues, author names, and resource links are read from the canonical
publication records. Figure-source links retain the source attribution. Changing
this selection does not change the full publications archive.

## Reviewed corrections and remaining details

- The accent-bias paper uses its published title, **The Cost of Sounding Different:
  Accent Bias in Audio Language Models**, verified against ACL Anthology. Its
  original title remains in `source_citation` for traceability.
- Recovered paper links for Connecting the Dots, the 2021 paraphrasing paper, and
  Risk Cards, plus code links for Connecting the Dots and paraphrasing.
- Corrected Alexander Metzger's name against the paper's arXiv record.
- Original source citations and import order are preserved. Verified final
  publication years are recorded as reviewed overrides: vMF is grouped under
  ICLR 2019, and FlexiTokens, instruction-hierarchy reasoning, and LayRA under
  their 2026 publication venues.
- Machine Translation with Continuous Outputs (2018 workshop) has no resource URL
  on the source site. Its citation is retained without an invented link.
- Alumni appear as a text list. Current students retain their portraits; Muge
  and Yusen's portraits were copied from their linked public homepages.
- Alumni are sorted by `graduation_year` in descending order. Current M.S.
  students are maintained separately in `_data/group.json`.
- The existing July 2025 CV remains linked. Replace it when a newer CV is available.

## Publication review — 6 November 2026

- Updated 15 existing paper records against ACL Anthology, PMLR, OpenReview,
  the NeurIPS program, and author-maintained publication records. Evidence URLs
  are retained in `migration/publication-overrides.json`.
- Added the missing **End-to-End Differentiable GANs for Text Generation**
  workshop paper from PMLR, bringing the archive to 58 papers.
- Added published EMNLP, ACL Findings, EACL demonstration, COLM, and TMLR links
  and citation metadata while retaining all 92 original resource links.
- Updated the hallucination position paper to the final ICML title and complete
  author list. Corrected the homepage EMNLP announcement to two main-conference
  papers and one Findings paper.
- Updated OGCaReBench to its verified ICML 2026 Structured Data for Health
  workshop poster venue. Workshop acceptance is kept distinct from main-track
  acceptance.
- HalluWorld and the SLT paper remain marked “To appear”; the other remaining
  preprints have no newly verified archival acceptance in this review.
- The generator and rendered-site check now verify one descending year group
  per publication year. Copyable citations use journal entries for TMLR and
  retain supplied publisher metadata where available.

## Publication

The public GitHub Pages destination is https://shocheen.github.io/. Future changes
publish through the existing Pages build when pushed to `master`. Confirm that
the repository's "pages build and deployment" run succeeds after each publication.
The custom-domain cutover will be performed manually by the site owner later.
No custom-domain, DNS, or Google Sites changes are part of this publication.

The pre-migration working tree and existing uncommitted diff were backed up at
`/tmp/sachin-site-before-migration/` before editing. That temporary backup is local
to this machine and should not be treated as permanent storage.
