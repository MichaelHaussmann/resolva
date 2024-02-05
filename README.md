
# resolva

Path & string resolver inspired by and derived from Lucidity.

## Features
- pattern to regex conversion
- instance cache to avoid repeated regex compilations
- lru_caches to speed up resolves
- very simple API

## Why not Lucidity ?
Resolva is a simplified version of lucidity.

It lacks certain features as:
- individual template handling
- nested data structures
- template discovery

### TODO: 
- optional strict / relaxed (as lucidity)
- optional anchor start / end / both (as lucidity)
- test failing scenarios (duplicated keys with strict)
- test all features with duplicated keys strict and relaxed
- test format behaviour in lucidity
- rename repo and python package
- add pyproject for pypi release
- rust version with python binding