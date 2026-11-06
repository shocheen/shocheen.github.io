# Appearance previews

Lagrange remains the default in `_config.yml`. Texture is an optional override
in `_config.texture.yml`; load that file after `_config.yml` to select it.
Build each appearance into a separate directory so the previews can be compared.

Both appearances use the existing `_pages`, `_data`, and `_publications` content.
The profile arrangement is shared in `_includes/bio-profile.html` and
`_sass/_bio-profile.scss`: portrait alongside name, affiliation, email, and
labeled social links, followed by the original biography. Its arrangement was
requested from the visual reference at https://saisuryadv.com/; the site's
wording and links remain Sachin's own.

The theme-specific headers are `_includes/lagrange/header.html` and
`_includes/texture/header.html`. Typography and theme overrides live in
`assets/css/lagrange.scss` and `assets/css/texture.scss`, with supporting Sass
under the corresponding `_sass/` directory. Keeping the shared profile separate
allows the two appearances to reuse it or combine selected styles.

The upstream theme licenses and source notes are in `licenses/`.
Pushing to `master` publishes the default appearance through GitHub Pages.
Texture remains available for future comparison without changing the default.
