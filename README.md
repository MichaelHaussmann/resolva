
# resolva

Simple and fast path template resolver.  
Inspired by and derived from Lucidity.


## What is resolva ?

**resolva** is a python library that extracts data from a string by matching configurated patterns.

`"/mnt/prods/hamlet/shots/sq010"` => 
`"/mnt/prods/{prod}/shots/{seq}"` => 
`{"prod": "hamlet", "seq": "sq010"}`

Typical usage:
- for a path or string input,
- loops through a series of configured patterns, 
- once a matching pattern found, 
- extracts data and returns a dictionary

Instead of bare regex, the pattern uses a simpler "format" style syntax.  

**resolva** can also format the data back to a string.

### Path resolving

Template based path resolving is a typical need in CG pipeline tools.

Examples include:

- [Shotgrid Toolkit (SGTK)](https://github.com/shotgunsoftware/tk-config-default/blob/master/core/templates.yml) - Leading commercial CG and VFX Project Management and pipeline toolkit
- [CGWire's kitsu file trees](https://zou.cg-wire.com/file_trees) - Kitsu is an Open Source collaboration platform for Animation and VFX studios. 
- [Lucidity](https://gitlab.com/4degrees/lucidity) - Inspired by SGTK templating, in turn inspiration and base of **resolva**
- [spil](https://github.com/MichaelHaussmann/spil) - Uses **resolva** at its core


## Usage Example

Configuration:
```python
from resolva import Resolver

template = {"maya_file": "/mnt/prods/{prod}/shots/{seq}/{shot}_{version:(v\d\d\d)}.{ext:(ma|mb)}",
            "hou_file": "/mnt/prods/{prod}/shots/{seq}/{shot}_{version:(v\d\d\d)}.{ext:(hip|hipnc)}"}
Resolver("id", template)
```
Usage:
```python
from resolva import Resolver
r = Resolver.get("id")

input = "/mnt/prods/hamlet/shots/sq010/sh010_v012.ma"
_type, data = r.resolve_first(input)

# result:
print(f'Detected type "{_type}" and extracted "{data}"')
```
Output:
```
Detected type "maya_file" and extracted 
{"prod": "hamlet", "seq": "sq010", "shot": "sh010", "version": "v012", "ext": "ma"}
```



## Features

- simple template format     
  - Example: `{shot}/{version}/{extension:(ma|mb)}`
  - handles duplicate placeholders
- very simple API
  - resolve with one, first, or all patterns
  - format with one, first, or all patterns
  - format including reverse resolve check
- high speed using caches
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

The result is a fast and very simple to use toolset.

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


### TODO:

- "label" instead of "name" ? or "key" ? 
- should fails return (None, None) ? tuple[None] ? (replace "found" by "result")
- docstrings (+doctests) 
- pytests calling the existing tests
- fix test logging
- documentation + API documentation (readthedocs or github?)
- black, refurb, etc.
- pip installable and python bound rust implementation 


### Acknowledgements

**resolva** is inspired by, and derived from **Lucidity**.

#### Lucidity 

https://gitlab.com/4degrees/lucidity/  
https://lucidity.readthedocs.io  
copyright: Copyright (c) 2013 Martin Pengelly-Phillips  
licence: Apache License, Version 2.0

#### resolva

https://github.com/MichaelHaussmann/resolva  
(c) 2024 Michael Haussmann  
licence: MIT
