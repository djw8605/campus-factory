---
layout: page
title: "About"
description: "Features of the Campus Factory"
---
{% include JB/setup %}

<p class="lead">
The Campus Factory builds off of production software such as <a href="http://research.cs.wisc.edu/condor/">Condor</a> and <a href="http://www.uscms.org/SoftwareComputing/Grid/WMS/glideinWMS/">GlideinWMS</a>.  Together, this builds a strong foundation for a powerful Campus Factory.
</p>


## Simple Configuration

The Campus Factory uses the simple configuration.  Using the common .ini format:

```
# The main section
[general]

#
# Things you need to edit
#

# Logging directory
#logdirectory = /home/swanson/dweitzel/campus_factory/share
logdirectory = ./


# The directory that is local to the worker node. This will
# be where condor places the intermediate job data and
# the glidein logs
# Default: /tmp
#worker_tmp = /state/partition1/tmp

```

## Integration with Condor / <a href="http://bosco.opensciencegrid.org/">BOSCO</a>



