# Usage

## Quickstart

### General process

- For a configured pattern, eg: `/mnt/prods/{prod}/shots/{seq}` 
- Given a path, eg: `/mnt/prods/hamlet/shots/sq010`  
- Resolva will extract and return this: `{"prod": "hamlet", "seq": "sq010"}`

### Simple complete usage example

Configuration:
```python
from resolva import Resolver

template = {"maya_file": "/mnt/prods/{prod}/shots/{seq}/{shot}_{version:(v\d\d\d)}.{ext:(ma|mb)}",
            "hou_file": "/mnt/prods/{prod}/shots/{seq}/{shot}_{version:(v\d\d\d)}.{ext:(hip|hipnc)}"}
Resolver("id", template)  # create the Resolver in an instance cache
```
Resolving:
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

## Configuration

### Pattern syntax

Instead of using regex, the pattern syntax is simplified and resembles the string format syntax.

Pattern example:  
`/mnt/prods/{prod}/shots/{seq}/{shot}_{version:(v\d\d\d)}.{ext:(ma|mb)}`

Syntax notes:  
- pattern "keys" are between braces: `/mnt/prods/{prod}`
- required values can optionally be set after a colon, for example:
  - a choice ("ma" or "mb"): `{ext:(ma|mb)}`
  - a pattern ("v" followed by 3 digits): `{version:(v\d\d\d)}`
  - a plain value ("asset"): `{type:asset}`

### Patterns dictionary

When resolving, we usually need to check multiple patterns, until one matches.

Thus, the configuration is a sorted dictionary containing multiple `label: pattern` mappings.

The **pattern order** is important. The most *precise* pattern should come before a more generic one, so the resolver hits it first.

Patterns dictionary example:

```python
patterns = {"maya_file": r"/mnt/prods/{prod}/shots/{seq}/{shot}_{version:(v\d\d\d)}.{ext:(ma|mb)}", 
            "any_file":  r"/mnt/prods/{prod}/shots/{seq}/{shot}_{version:(v\d\d\d)}.{ext}", 
            "sequence":  "/mnt/prods/{prod}/shots/{seq}", 
            "project":   "/mnt/prods/{prod}" }
```

In this example, the narrower `maya_file` pattern comes before the generic `any_file`.  
Since a maya file is also a generic file, we want the `maya_file` pattern to be matched before `any_file`.

### Pattern options

There are 3 advanced pattern options:
- duplicate placeholders
- anchor_start
- anchor_end

These options are arguments of the Resolver instantiation.
Please refer to the API.

#### Duplicate placeholders

If a pattern contains a placeholder twice, the resolver checks if the values are equal.

Example:  

In this example `shot` appears twice:  
`/mnt/prods/{prod}/shots/{seq}/{shot}/{shot}_{version}.{ext}`

The following input will raise a *ResolvaException*:  
`/mnt/prods/hamlet/shots/sq010/sh010/010_v001.ma` because `sh010` and `010` both match `shot` but are not equal. 


## Resolving and formatting

### Creating the Resolver object

When the `resolva.Resolver` is instantiated, it is stored in **cache**.  
This is done to keep the compiled regex from the configuration patterns in memory, for faster response.

We create the instance using a **unique key**, and pass the configuration.
The key enables to create multiple Resolver instances per application, if needed.

The key can be of any type that is usable as dictionary key (must be hashable).

Example:
```python
import resolva

patterns = {"maya_file": r"/mnt/prods/{prod}/shots/{seq}/{shot}_{version:(v\d\d\d)}.{ext:(ma|mb)}", 
            "any_file":  r"/mnt/prods/{prod}/shots/{seq}/{shot}_{version:(v\d\d\d)}.{ext}", 
            "sequence":  "/mnt/prods/{prod}/shots/{seq}", 
            "project":   "/mnt/prods/{prod}" }

resolva.Resolver("any_id", patterns)  # The instance is not used in the current code.
```

### Getting the Resolver object

Once the Resolver was instantiated, it is in cache.  
We retrieve it using the `get(id: Any)` factory.

Example:
```python
import resolva
r = resolva.Resolver.get("any_id")
```
Now `r` holds the Resolver object.


## Resolving

The Resolver has 3 resolve methods:
- resolve_first
- resolve_one
- resolve_all

### resolve_first

**resolve_first** resolves using the first available match.

It receives a string to resolve.
It runs over the list of patterns (internally over the list of re.Pattern) until the first match.

This match generates a data dictionary.
The method returns a tuple with the matching pattern label and the resolved data dictionary.

#### Example: resolving Maya file path, finds "maya_file" pattern

```python
import resolva

input = "/mnt/prods/hamlet/shots/sq010/sh010_v012.ma"
r = resolva.Resolver.get("any_id")
label, data = r.resolve_first(input)
```

Result:
- label: `maya_file`
- data: `{'prod': 'hamlet', 'seq': 'sq010', 'shot': 'sh010', 'version': 'v012', 'ext': 'ma'}`

#### Example: resolving Nuke file path, finds "any_file" pattern

```python
import resolva

input = "/mnt/prods/hamlet/shots/sq010/sh010_v012.nk"
r = resolva.Resolver.get("any_id")
label, data = r.resolve_first(input)
```

Result:
- label: `any_file`
- data: `{'prod': 'hamlet', 'seq': 'sq010', 'shot': 'sh010', 'version': 'v012', 'ext': 'nk'}`

### resolve_one

**resolve_one** resolves using the given pattern.

It receives a string to resolve and a pattern label to match against.
The Resolver then tries to match the string with the designated pattern.

If the match happens, a data dictionary is generated and returned.
If not, an empty dictionary is returned

#### Example: resolving Maya file path with given "maya_file" pattern

```python
import resolva
input = "/mnt/prods/hamlet/shots/sq010/sh010_v012.ma"
r = resolva.Resolver.get("any_id")
data = r.resolve_one(input, "maya_file")
```

Result:
- data: `{'prod': 'hamlet', 'seq': 'sq010', 'shot': 'sh010', 'version': 'v012', 'ext': 'ma'}`

#### Example: resolving Maya file path with given "any_file" pattern

```python
import resolva
input = "/mnt/prods/hamlet/shots/sq010/sh010_v012.ma"
r = resolva.Resolver.get("any_id")
data = r.resolve_one(input, "any_file")
```
Result:
- data: `{'prod': 'hamlet', 'seq': 'sq010', 'shot': 'sh010', 'version': 'v012', 'ext': 'ma'}`

#### Example: resolving Maya file path with given "sequence" pattern: not matching

```python
import resolva
input = "/mnt/prods/hamlet/shots/sq010/sh010_v012.ma"
r = resolva.Resolver.get("any_id")
data = r.resolve_one(input, "sequence")
```

Result: not matching
- data: `{}`

### resolve_all

**resolve_all** resolves all possible matches.

It receives a string to resolve.
It runs over the list of patterns (internally over the list of re.Pattern).

Every match generates a data dictionary.
The method returns a dictionary with
- each key: the matching pattern label
- each value: the resolved data dictionary.

If there is no match, an empty dictionary is returned.

#### Example: resolving Maya file path with all patterns

```python
import resolva
input = "/mnt/prods/hamlet/shots/sq010/sh010_v012.ma"
r = resolva.Resolver.get("any_id")
found = r.resolve_all(input)
```

Result:
- found: `{'any_file': {'ext': 'ma', 'prod': 'hamlet','seq': 'sq010', 'shot': 'sh010','version': 'v012'}, 'maya_file': {'ext': 'ma', 'prod': 'hamlet', 'seq': 'sq010','shot': 'sh010','version': 'v012'}}`

#### Example: resolving Nuke file path with all patterns

```python
import resolva
input = "/mnt/prods/hamlet/shots/sq010/sh010_v012.nk"
r = resolva.Resolver.get("any_id")
found = r.resolve_all(input)
```

Result:
- found: `{'any_file': {'ext': 'nk', 'prod': 'hamlet', 'seq': 'sq010', 'shot': 'sh010', 'version': 'v012'}}`

#### Example: resolving non-matching string with all patterns

```python
import resolva
r = resolva.Resolver.get("any_id")
found = r.resolve_all("blablabla")
```

Result:
- found: `{}`


## Formatting

Formatting is the reverse of resolving.
For a given string data dictionary, a formatted string is returned, according to the same configured patterns.

The Resolver has 3 format methods:
- format_first
- format_one
- format_all

### format_first

**format_first** formats using the first matching pattern.

It receives a string data dictionary to format.
It runs over the list of patterns (internally over the internal "formats" dict) until the first match.

A match means:
- the keys of the data dictionary match the keys of the patterns "format" string,
- the formatted string resolves back to an identical data dictionary.

Once a match is found, a formatted string is generated and returned.
The method returns a tuple with the label and the formatted string.
Or a (None, None) tuple if there is no match.


#### Example: formatting Maya file dict with first matching pattern 

```python
import resolva
r = resolva.Resolver.get("any_id")
data = { 'prod': 'hamlet', 'seq': 'sq010', 'shot': 'sh010', 'version': 'v012', 'ext': 'ma'}
formatted = r.format_first(data)
```

Result:
- formatted: `('maya_file', '/mnt/prods/hamlet/shots/sq010/sh010_v012.ma')`


#### Example: formatting Sequence dict with first matching pattern 

```python
import resolva
r = resolva.Resolver.get("any_id")
data = {'prod': 'hamlet', 'seq': 'sq010'}
formatted = r.format_first(data)
```

Result:
- formatted: `('sequence', '/mnt/prods/hamlet/shots/sq010')`


### format_one

**format_one** formats using the given pattern.

It receives a string data dictionary to format, and a pattern label to match against.

The Resolver then tries to match with the designated pattern.
A match means:
- the keys of the data dictionary match the keys of the patterns "format" string,
- the formatted string resolves back to an identical data dictionary.

If the pattern matches, the generated formatted string is returned.
Else, None is returned.

#### Example: formatting Sequence dict with given "sequence" pattern 

```python
import resolva
r = resolva.Resolver.get("any_id")
data = {'prod': 'hamlet', 'seq': 'sq010'}
formatted = r.format_one(data, "sequence")
```

Result:
- formatted: `'/mnt/prods/hamlet/shots/sq010'`

#### Example: formatting Sequence dict with given "project" pattern: not matching

```python
import resolva
r = resolva.Resolver.get("any_id")
data = {'prod': 'hamlet', 'seq': 'sq010'}
formatted = r.format_one(data, "project")
```

Result:
- formatted: `None`


### format_all

**format_all** formats using all possible matches.

It receives a string data dictionary to format.
It runs over the list of patterns (internally over the internal "formats" dict).

Every match generates a formatted string.

A match means:
- the keys of the data dictionary match the keys of the patterns "format" string,
- the formatted string resolves back to an identical data dictionary.

The method returns a dictionary with all matching pattern labels as keys, and the formatted strings as values.
If there is no match, an empty dictionary is returned.

#### Example: formatting Sequence dict with all patterns 

```python
import resolva
r = resolva.Resolver.get("any_id")
data = {'prod': 'hamlet', 'seq': 'sq010'}
formatted = r.format_all(data)
```

Result:
- formatted: `{'sequence': '/mnt/prods/hamlet/shots/sq010'}`


#### Example: formatting Maya file dict with all patterns
    
```python
import resolva
r = resolva.Resolver.get("any_id")
data = { 'prod': 'hamlet', 'seq': 'sq010', 'shot': 'sh010', 'version': 'v012', 'ext': 'ma'}
formatted = r.format_all(data)
```

Result:
- formatted: `{'maya_file': '/mnt/prods/hamlet/shots/sq010/sh010_v012.ma', 'any_file': '/mnt/prods/hamlet/shots/sq010/sh010_v012.ma'}`

    
## Control and introspection

The `resolva.Resolver` class has some extra methods to control and introspect its content.

These methods should not be useful for normal configuring, resolving and formatting.  

For more details, please check out the API section.

Methods list:
- get_id
- get_labels
- get_patterns
- get_pattern_for
- get_regexes
- get_regex_for
- get_formats
- get_format_for
- get_keys
- get_keys_for