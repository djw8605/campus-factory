---
layout: page
title: "How To"
tagline: List of How To Guides
description: ""
group: navigation
---
{% include JB/setup %}

This is a list of How To Guides:

<ul>
   {% assign pages_list = site.pages %}
   {% assign group = 'HowTo' %}
   {% include JB/pages_list %}
</ul>

