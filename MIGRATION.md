# Google Sites → GitHub Pages

The existing AcademicPages/Jekyll site contains the migrated website, published
through the repository's existing GitHub Pages build from `master`. The Google
Site and custom-domain settings are managed separately and have not been changed.

## Migrated content

- All 56 publications from the Google Sites research page, in the original order.
- All 92 original resource links, plus six recovered links verified against primary sources.
- Complete author lists, venues, award text, and equal-contribution markers.
- 105 news entries; eight appear initially and earlier news expands on the homepage.
- Six current Ph.D. students, five alumni, the group support statement, and five courses.
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
fields. Resource labels retain their meaning: code is never stored as slides.
The generator writes the individual `_publications` documents. Their URLs remain
stable; six former malformed author-name documents redirect to the correct papers.

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

Normal future edits only require the generator. Re-importing intentionally replaces
the data with the Google Sites content plus the reviewed overrides.

## Reviewed corrections and remaining details

- The accent-bias paper uses its published title, **The Cost of Sounding Different:
  Accent Bias in Audio Language Models**, verified against ACL Anthology. Its
  original title remains in `source_citation` for traceability.
- Recovered paper links for Connecting the Dots, the 2021 paraphrasing paper, and
  Risk Cards, plus code links for Connecting the Dots and paraphrasing.
- Corrected Alexander Metzger's name against the paper's arXiv record.
- Source year groupings are preserved. In particular, the vMF paper is listed
  under 2018 on the Google Site, while its venue is ICLR 2019. Several papers
  first listed in 2025 have 2026 venues. These are not silently re-dated.
- Machine Translation with Continuous Outputs (2018 workshop) has no resource URL
  on the source site. Its citation is retained without an invented link.
- Yi Yu's Google Sites portrait could not be copied; the group page uses initials.
  Muge and Yusen's portraits were copied from their linked public homepages.
- The existing July 2025 CV remains linked. Replace it when a newer CV is available.

## Publication

The public GitHub Pages destination is https://shocheen.github.io/. Future changes
publish through the existing Pages build when pushed to `master`. Confirm that
the repository's "pages build and deployment" run succeeds after each publication.
The custom-domain cutover will be performed manually by the site owner later.
No custom-domain, DNS, or Google Sites changes are part of this publication.

The pre-migration working tree and existing uncommitted diff were backed up at
`/tmp/sachin-site-before-migration/` before editing. That temporary backup is local
to this machine and should not be treated as permanent storage.
