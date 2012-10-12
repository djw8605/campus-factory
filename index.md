---
layout: main
title: Campus Factory
tagline: A lightweight glidein factory designed to connect campus resources together into a on-demand Condor cluster
actionbutton: Learn More
actionurl: about.html
---
{% include JB/setup %}

<div class="row-fluid">
<div class="hero-unit">
<h1>Campus Factory</h1>
<p>A lightweight glidein factory designed to connect campus resources together into a on-demand Condor cluster</p>
<p>
<a href="https://github.com/djw8605/campus-factory/zipball/master" class="btn btn-primary btn-large">
Download
</a>
<a class="btn btn-info btn-large" href="about.html">
Learn More
</a>
</p>
</div>
</div>
<div class="row-fluid">
<div class="span4">
<div class="well">
<h2>Build on Production</h2>
<p>
The Campus Factory is built on production software such as Condor and GlideinWMS libraries.
</p>
</div>
</div> <!-- END SPAN -->
<div class="span4">
<div class="well">
<h2>Simple Configration</h2>
<p>
Configuration file is in standard ini format.  Simple to customize the ini style configuration.
</p>
</div>
</div> <!-- END SPAN -->
<div class="span4">
<div class="well">
<h2>Condor Integration</h2>
<p>
The Campus Factory is integrated with <a href="http://research.cs.wisc.edu/condor/">Condor</a>, the High Throughput Computing resource manager
</p>
</div>
</div> <!-- END SPAN -->
</div> <!-- END ROW -->

Read [Jekyll Quick Start](http://jekyllbootstrap.com/usage/jekyll-quick-start.html)

Complete usage and documentation available at: [Jekyll Bootstrap](http://jekyllbootstrap.com)

## Update Author Attributes

In `_config.yml` remember to specify your own data:
    
    title : My Blog =)
    
    author :
      name : Name Lastname
      email : blah@email.test
      github : username
      twitter : username

The theme should reference these variables whenever needed.
    
## Sample Posts

This blog contains sample posts which help stage pages and blog data.
When you don't need the samples anymore just delete the `_posts/core-samples` folder.

    $ rm -rf _posts/core-samples

Here's a sample "posts list".

<ul class="posts">
  {% for post in site.posts %}
    <li><span>{{ post.date | date_to_string }}</span> &raquo; <a href="{{ BASE_PATH }}{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>

## To-Do

This theme is still unfinished. If you'd like to be added as a contributor, [please fork](http://github.com/plusjade/jekyll-bootstrap)!
We need to clean up the themes, make theme usage guides with theme-specific markup examples.


