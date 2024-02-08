
# resolva

Simple and fast path template resolver.  
Inspired by and derived from Lucidity.


## What is resolva ?

resolva is a python library that extracts data from a string by matching configurated patterns.

Typical usage:
- for a path or string input,
- loops through a series of configured patterns, 
- once a matching pattern found, 
- extracts data into a dictionary

Instead of bare regex, the pattern has a more readable "format" style syntax.  

resolva can also format the data back to a string.

### Path resolving

Template based path resolving is a typical need in CG pipeline tools.

Examples include:

- [Shotgrid Toolkit](https://github.com/shotgunsoftware/tk-config-default/blob/master/core/templates.yml) - Commercial CG and VFX Project Management and pipeline Toolkit
- [CGWire's kitsu file trees](https://zou.cg-wire.com/file_trees) - Kitsu is an Open Source collaboration platform for Animation and VFX studios. 
- [Lucidity](https://gitlab.com/4degrees/lucidity) - Inspiration and source of resolva
- [spil](https://github.com/MichaelHaussmann/spil) - Uses resolva at its core


## Usage Example

```python
# config
patterns = {'maya_file': ''}

# usage



```

## Features

- simple pattern usage (as in lucidity)
- very simple API
- instance cache to avoid repeated regex compilations
- lru_caches to speed up resolves


## Why not Lucidity ?

Resolva is a simplified version of the Lucidity, a filesystem templating and management library.

Resolva is at the core of [spil](https://github.com/MichaelHaussmann/spil).
A large amount of strings and paths need to be resolved at high speed.

The end goal is to build a rust path template resolver.
(rust development not started yet).

To prepare this in python, we reduced the Lucidity library to its essence (around 100 lines of code).

On top of these essential features, we built a simple Resolver class with an instance cache (to keep regex compiles in memory), and a lru cache, to memoize resolves that have no reason to change.

The result is a very simple to use and fast tool.

Resolva lacks some Lucidity features that were cut out:

- individual template API
- nested data structures
- template discovery
- templates referencing templates

If you need one of these, go for the original :)


### TODO: 
- rename package and repo
- doc & doctests
- add pyproject for pypi release
- rust version with python binding
- black, refurb, etc.


### Acknowledgement

Lucidity

https://gitlab.com/4degrees/lucidity/
https://lucidity.readthedocs.io

copyright: Copyright (c) 2013 Martin Pengelly-Phillips
licence: Apache License, Version 2.0, January 2004, http://www.apache.org/licenses

