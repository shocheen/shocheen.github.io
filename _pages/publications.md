---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: false
redirect_from:
  - /research/
---

{% if site.author.googlescholar %}
  <div class="wordwrap">You can also find my articles on <a href="{{site.author.googlescholar}}">my Google Scholar profile</a>.</div>
{% endif %}

{% include base_path %}

{% assign publications = site.publications | sort: "publication_order" %}
{% assign current_year = "" %}
{% for publication in publications %}
{% if publication.year != current_year %}
{% assign current_year = publication.year %}
<h2 class="publication-year">{{ current_year }}</h2>
{% endif %}
{% include publication.html publication=publication %}
{% endfor %}
