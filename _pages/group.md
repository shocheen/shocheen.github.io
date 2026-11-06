---
layout: archive
title: "My Group"
permalink: /group/
author_profile: true
redirect_from:
  - /my-group/
---

## Ph.D. Students

<div class="group-grid">
{% for member in site.data.group.students %}
  {% include group-member.html member=member %}
{% endfor %}
</div>

## M.S. Students

<div class="group-grid">
{% for member in site.data.group.masters_students %}
  {% include group-member.html member=member %}
{% endfor %}
</div>

## Alumni

{% assign alumni = site.data.group.alumni | sort: 'graduation_year' | reverse %}
<ul class="alumni-list">
{% for member in alumni %}
  <li><a href="{{ member.url | escape }}">{{ member.name | escape }}</a> — {{ member.detail | escape }}{% if member.note %}; {{ member.note | escape }}{% endif %}</li>
{% endfor %}
</ul>

## Support

We are grateful to Schmidt Sciences, Allen Institute for AI, OSU Center on Responsible AI and Governance (CRAIG), OSU Kirwan Institute, OSU Clinical and Translational Science Institute (CTSI) for their generous funding support, and Amazon, NVIDIA, and NSF National Artificial Intelligence Research Resource (NAIRR), for their generous compute support of our group's research.
