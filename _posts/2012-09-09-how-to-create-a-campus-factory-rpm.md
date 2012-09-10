---
layout: post
title: "How to Create a Campus Factory RPM"
description: "How to Create a Campus Factory RPM"
tagline: 
category: HowTo
tags: ['HowTo']
---
{% include JB/setup %}

## Setting up the Environment

First we need to install the OSG development tools.  The documentation is on the [OSG Twiki](https://twiki.grid.iu.edu/bin/view/Documentation/Release3/YumRepositories).

    $ rpm -Uvh http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-7.noarch.rpm
    $ yum install yum-priorities
    $ rpm -Uvh http://repo.grid.iu.edu/osg-el6-release-latest.rpm
    $ yum install osg-build


