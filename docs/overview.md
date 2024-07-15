# Overview

## What is resolva ?

**resolva** is a simple and fast **path template resolver**:<br>
A python library that extracts data from a string by matching configured patterns.  

It is inspired by and derived from [Lucidity](https://gitlab.com/4degrees/lucidity), which in turn is loosely inspired by [Shotgrid Toolkit (SGTK) templating](https://github.com/shotgunsoftware/tk-config-default/blob/master/core/templates.yml). 

### How does it work ?

- For a configured pattern, eg: `/mnt/prods/{prod}/shots/{seq}` 
- Given a path, eg: `/mnt/prods/hamlet/shots/sq010`  
- Resolva will extract and return this: `{"prod": "hamlet", "seq": "sq010"}`

### Process

1. for a path or string input,
2. the resolver loops through a series of configured patterns, 
3. once a matching pattern found, 
4. extracts data and returns a dictionary

Instead of bare regex, the pattern uses a simpler "format" style syntax.  

**resolva** can also format the data back to a string.

### Path resolving

Template based path resolving is a typical need in CG pipeline tools.

Examples include:

- [Shotgrid Toolkit (SGTK)](https://github.com/shotgunsoftware/tk-config-default2/blob/master/core/templates.yml) - Leading commercial CG and VFX Project Management and pipeline toolkit
- [CGWire's kitsu file trees](https://zou.cg-wire.com/file_trees) - Kitsu is an Open Source collaboration platform for Animation and VFX studios. 
- [Lucidity](https://gitlab.com/4degrees/lucidity) - Inspired by SGTK templating, in turn inspiration and base of **resolva**
- [spil](https://github.com/MichaelHaussmann/spil) - Uses **resolva** at its core


## Usage Example

Configuration:
```python
from resolva import Resolver

template = {"maya_file": "/mnt/prods/{prod}/shots/{seq}/{shot}_{version:(v\d\d\d)}.{ext:(ma|mb)}",
            "hou_file": "/mnt/prods/{prod}/shots/{seq}/{shot}_{version:(v\d\d\d)}.{ext:(hip|hipnc)}"}
Resolver("id", template)  # create the Resolver in an instance cache
```
Usage:
```python
from resolva import Resolver
r = Resolver.get("id")  # read the Resolver from the instance cache

input = "/mnt/prods/hamlet/shots/sq010/sh010_v012.ma"
label, data = r.resolve_first(input)

# result:
print(f'Detected type "{label}" and extracted "{data}"')
```
Output:
```
Detected type "maya_file" and extracted 
{"prod": "hamlet", "seq": "sq010", "shot": "sh010", "version": "v012", "ext": "ma"}
```

## Features

- Simple template format     
  - Example: `/{shot}/{version}/{name}.{extension:(ma|mb)}`
  - handles duplicate placeholders
- Very simple API
  - resolve with one, first, or all patterns
  - format with one, first, or all patterns
- High speed thanks to caches
  - instance cache (keep regex compilations in memory)
  - lru_caches (speed up immutable resolves)


## Why not Lucidity ?

**resolva** is a simplified version of [Lucidity](https://gitlab.com/4degrees/lucidity), a filesystem templating library.

**resolva** is now used at the core of [spil](https://github.com/MichaelHaussmann/spil).  
A large amount of strings and paths need to be resolved at high speed.

The end goal is to build a rust path template resolver.  
Rust development not started yet - contributions are highly welcomed :)

To prepare this in python, we reduced the Lucidity library to its essence (around 100 lines of code).

On top of these essential features, we built a simple Resolver class with an instance cache (to keep regex compiles in memory), and a lru cache, to memoize resolves that have no reason to change.

The result is a fast and very simple toolset.

**resolva** keeps essential Lucidity's features:

- simple template format 
- handles duplicate placeholders
- pattern anchoring (start:`^`,end:`$`)

**resolva** lacks some Lucidity features, that were left out:

- individual template API
- nested data structures
- template discovery
- templates referencing templates
- python 2 support

If you need one of these, go for the original :)


## Installation

**resolva** works in Python >=3.7.<br>
It is available on pypi and can be installed using `pip install resolva`,  

**resolva** is open source, License: MIT.


## Acknowledgements

**resolva** is inspired by, and derived from **Lucidity**.

### Lucidity 

[https://gitlab.com/4degrees/lucidity](https://gitlab.com/4degrees/lucidity)<br>
[https://lucidity.readthedocs.io](https://lucidity.readthedocs.io)<br>
copyright: Copyright (c) 2013 Martin Pengelly-Phillips<br>  
licence: Apache License, Version 2.0

### resolva

[https://github.com/MichaelHaussmann/resolva](https://github.com/MichaelHaussmann/resolva)<br>
(c) 2024 Michael Haussmann<br>
licence: MIT


## Interested ?

We'd love to hear from you.<br>
We are interested in any kind of feedback: comments, questions, issues, pull requests.

Do not hesitate to [start a discussion on github](https://github.com/MichaelHaussmann/resolva/discussions/new/choose).

<br>
  
![python](https://img.shields.io/badge/PYTHON-blue?style=for-the-badge&logo=Python&logoColor=white)
![type checker](https://img.shields.io/badge/Type%20checker-MYPY-dodgerblue?style=for-the-badge&labelColor=abcdef)
![gitHub release](https://img.shields.io/github/v/release/MichaelHaussmann/resolva?style=for-the-badge&color=orange&labelColor=sandybrown)
