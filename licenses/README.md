The Lagrange preview adapts the header, page container, typography, and styles
from [Paul Le's Lagrange theme](https://github.com/LeNPaul/Lagrange), downloaded
from its `gh-pages` branch on 2026-11-05. Its original MIT license is retained in
`Lagrange-MIT.md`. The files in `_sass/lagrange/` other than `_site.scss` are
copied from that theme; `_site.scss` integrates the existing academic content.

The optional Texture preview uses [Samarjeet Singh's Texture theme](https://github.com/samarsault/texture),
downloaded from its `master` branch on 2026-11-05. Its original MIT license is in
`Texture-MIT.txt`. The upstream theme styles and texture images are retained in
`_sass/texture/` and `assets/textures/`. Imports are namespaced, the header rule
is scoped to the theme banner, and the existing Font Awesome icons replace
Fontello. `_site.scss` adapts navigation, profiles, and academic content.

Lagrange remains the default appearance in `_config.yml`. To preview Texture,
add `_config.texture.yml` after `_config.yml` in the Jekyll `--config` list and
use a separate destination. Both appearances use the same pages and citation
data, so switching themes or combining selected styles does not require
editing content.
