"""
This file is part of resolva.
(C) copyright 2024 Michael Haussmann, spil@xeo.info
resolva is free software and is distributed under the MIT License. See LICENSE file.
"""
from __future__ import annotations
from typing import Any
import functools
import string as _string
import re

from resolva import template  # type: ignore
from resolva.utils import log, ResolvaException  # type: ignore

instance_cache: dict = {}


class Resolver:
    """
    Main class and entry point to use Resolva.

    When a Resolver object is created, it is set in an instance cache (in memory), for faster usage later.
    The instance contains the compiled regex patterns, which do not need to be recompiled later.

    Examples:

        >>> # 1. Reading the patterns and creating the Resolver instance
        >>> patterns = {"maya_file": r"/mnt/prods/{prod}/shots/{seq}/{shot}_{version:(v\d\d\d)}.{ext:(ma|mb)}", \
                        "any_file":  r"/mnt/prods/{prod}/shots/{seq}/{shot}_{version:(v\d\d\d)}.{ext}", \
                        "sequence":  "/mnt/prods/{prod}/shots/{seq}", \
                        "project":   "/mnt/prods/{prod}" }
        >>> __ = Resolver("any_id", patterns)  # the instance is created and set in the cache

        >>> # 2. Getting and using the instance
        >>> r = Resolver.get("any_id")
        >>> print(r)
        [resolva.Resolver] ID: [any_id] - Pattern labels: ['maya_file', 'any_file', 'sequence', 'project']

        >>> # Can also be done in one call
        >>> r = Resolver.get("other_id") or Resolver("other_id", patterns)  # getting from instance cache, or creating object
        >>> print(r)
        [resolva.Resolver] ID: [other_id] - Pattern labels: ['maya_file', 'any_file', 'sequence', 'project']


    The Resolver object holds all methods to use the resolver, for resolving and formatting.

    """

    def __init__(self, id: str, patterns: dict[str, str],
                 check_duplicate_placeholders: bool = True,
                 anchor_start: bool = True,
                 anchor_end: bool = True
                 ):
        """
        Creates a Resolver instance.

        The expected "patterns" is a dictionary holding pattern templates.
        - Each key is a "label": any string to identify the pattern.
        - Each value is a "pattern": a pattern string

        On instantiation, each pattern in the "patterns" dictionary is translated into regex and compiled to re.Pattern objects.
        This results in an internal "regexes" dictionary.

        Also, each pattern in the "patterns" dictionary is translated into a "format" string.
        This string is used to apply the format function, for the Resolvers formatting feature.
        All "format" strings are stored in an internal "formats" dict, with labels as keys.

        Each pattern is a string containing keywords, in curly brackets, eg "{project}", that will be matched by the Resolver.
        These keywords are stored in an internal "keys" dictionary, with labels as dict keys, and a set of keywords as value.

        The last arguments are configuration options.

        >>> patterns = {"maya_file": r"/mnt/prods/{prod}/shots/{seq}/{shot}_{version:(v\d\d\d)}.{ext:(ma|mb)}", \
                        "any_file":  r"/mnt/prods/{prod}/shots/{seq}/{shot}_{version:(v\d\d\d)}.{ext}", \
                        "sequence":  "/mnt/prods/{prod}/shots/{seq}", \
                        "project":   "/mnt/prods/{prod}" }
        >>> r = Resolver("any_id", patterns)
        >>> print(r)
        [resolva.Resolver] ID: [any_id] - Pattern labels: ['maya_file', 'any_file', 'sequence', 'project']

        Args:
            id: Any value that can be used as a dictionary key, to store the Resolver instance
            patterns: The {label: pattern} dictionary
            check_duplicate_placeholders: if the pattern may contain duplicate placeholders, and if the Resolver should check if their resolved values are identical.
            anchor_start: if each patterns starts with regex "^"
            anchor_end: if each patterns ends with regex "$"
        """

        # this is just to have a more readable dict comprehension loop later (k: construct_regex(v) ...)
        construct_regex = functools.partial(template.construct_regular_expression,
                                            anchor_start=anchor_start,
                                            anchor_end=anchor_end)

        self._id = id
        self._patterns = patterns
        self._regexes = {k: construct_regex(v) for k, v in patterns.items()}
        self._formats = {k: template.construct_format_specification(v) for k, v in patterns.items()}
        _keys = {k: set(template.get_keys(v)) for k, v in patterns.items()}

        # key extraction should be strictly identical, this is a temporary check.
        _keysB = {k: set([t[1] for t in _string.Formatter().parse(v) if t[1] is not None]) for k, v in self._formats.items()}
        if _keys != _keysB:
            raise ResolvaException(f'Keys not identical in check: "{_keys}" vs "{_keysB}"')

        self._keys = _keys
        self.check_duplicate_placeholders = check_duplicate_placeholders

        log.info(f'Resolver class init - id: "{id}"')

        # instance cache
        if instance_cache.get(id):
            log.info(f'Resolver instance already exists at "{id}". Will be overriden with: {self}')
        instance_cache[id] = self

    def __str__(self):
        return f"[resolva.Resolver] ID: [{self.get_id()}] - Pattern labels: {self.get_labels()}"

    def __repr__(self):
        return f'resolva.Resolver(id={self.get_id()}, patterns={self.get_patterns()})'

    @staticmethod
    def get(id: Any) -> Resolver | None:
        """
        Static factory method to retrieve an existing Resolver object from the instance cache.
        The given id should be an id already used during Resolver creation.

        Example
            >>> # the instance was created in earlier example
            >>> r = Resolver.get("any_id")
            >>> print(r)
            [resolva.Resolver] ID: [any_id] - Pattern labels: ['maya_file', 'any_file', 'sequence', 'project']

        Args:
            id: the id that was previously used during instantiation of the Resolver

        Returns:
            A resolver instance

        """
        instance = instance_cache.get(id)
        if not instance:
            log.info(f'No Resolver instance found with id "{id}"')
        return instance

    def get_id(self) -> Any:
        """
        Gets the id for the current Resolver instance.

        Example
            >>> # the instance was created in earlier example
            >>> r = Resolver.get("any_id")
            >>> print(r.get_id())
            any_id

        Returns:
            the id that was used during instantiation of the Resolver

        """
        return self._id

    def get_labels(self) -> list[str]:
        """
        Returns the list of pattern labels, as set during instantiation of the Resolver

        Example
            >>> # the instance was created in earlier example
            >>> r = Resolver.get("any_id")
            >>> print(r.get_labels())
            ['maya_file', 'any_file', 'sequence', 'project']

        Returns:
            List of pattern labels

        """
        return list(self._patterns.keys())

    def get_patterns(self) -> dict[str, str]:
        """
        Returns the patterns dictionary, as set during instantiation of the Resolver

        Example
            >>> # the instance was created in earlier example
            >>> from pprint import pprint
            >>> r = Resolver.get("any_id")
            >>> pprint(r.get_patterns(), sort_dicts=True)
            {'any_file': '/mnt/prods/{prod}/shots/{seq}/{shot}_{version:(v\\\\d\\\\d\\\\d)}.{ext}',
             'maya_file': '/mnt/prods/{prod}/shots/{seq}/{shot}_{version:(v\\\\d\\\\d\\\\d)}.{ext:(ma|mb)}',
             'project': '/mnt/prods/{prod}',
             'sequence': '/mnt/prods/{prod}/shots/{seq}'}


        Returns:
            The patterns dictionary
        """
        return self._patterns

    def get_pattern_for(self, label: str) -> str | None:
        """
        Returns the pattern for the given label.
        As stored in the patterns dictionary set during instantiation of the Resolver

        Example
            >>> # the instance was created in earlier example
            >>> r = Resolver.get("any_id")
            >>> print(r.get_pattern_for("sequence"))
            /mnt/prods/{prod}/shots/{seq}

        Args:
            label: a pattern label, must exist as key in the patterns dictionary

        Returns:
            The pattern stored in the patterns dictionary for the given label key.

        """
        return self._patterns.get(label)

    def get_regexes(self) -> dict[str, re.Pattern]:
        """
        On instantiation of the resolver, each pattern in the "patterns" dictionary is translated into regex, and compiled to re.Pattern objects.

        This results in an internal "regexes" dictionary:
        - Each key is a "label": string used to identify the pattern.
        - Each value is a "regex": a compiled regex object, generated from the corresponding "pattern".

        This function is useful for controlling and debugging.
        Is it not necessary to manipulate the regexes to resolve or format.

        Example
            >>> # the instance was created in earlier example
            >>> from pprint import pprint
            >>> r = Resolver.get("any_id")
            >>> pprint(r.get_regexes(), sort_dicts=True)
            {'any_file': re.compile('^/mnt/prods/(?P<prod001>[^/]*)/shots/(?P<seq001>[^/]*)/(?P<shot001>[^/]*)_(?P<version001>(v\\\\d\\\\d\\\\d)).(?P<ext001>[^/]*)$'),
             'maya_file': re.compile('^/mnt/prods/(?P<prod001>[^/]*)/shots/(?P<seq001>[^/]*)/(?P<shot001>[^/]*)_(?P<version001>(v\\\\d\\\\d\\\\d)).(?P<ext001>(ma|mb))$'),
             'project': re.compile('^/mnt/prods/(?P<prod001>[^/]*)$'),
             'sequence': re.compile('^/mnt/prods/(?P<prod001>[^/]*)/shots/(?P<seq001>[^/]*)$')}

        Returns:
            The internal compiled regexes dictionary resulting from the patterns.
        """
        return self._regexes

    def get_regex_for(self, label: str) -> re.Pattern | None:
        """
        Returns the compiled regex expression for the given label.
        As stored in the internal regexes dictionary

        Example
            >>> # the instance was created in earlier example
            >>> r = Resolver.get("any_id")
            >>> print(r.get_regex_for("sequence"))
            re.compile('^/mnt/prods/(?P<prod001>[^/]*)/shots/(?P<seq001>[^/]*)$')

        Args:
            label: a pattern label, must exist as key in the patterns dictionary

        Returns:
            The regex stored in the regexes dictionary for the given label key.

        """
        return self._regexes.get(label)

    def get_formats(self) -> dict[str, str]:
        """
        Each pattern in the "patterns" dictionary is translated into a "format" string.
        This string is used to apply the format function, for the Resolvers formatting feature.
        All "format" strings are stored in an internal "formats" dict, with labels as keys.

        Example
            >>> # the instance was created in earlier example
            >>> r = Resolver.get("any_id")
            >>> print(r.get_formats())
            {'maya_file': '/mnt/prods/{prod}/shots/{seq}/{shot}_{version}.{ext}', 'any_file': '/mnt/prods/{prod}/shots/{seq}/{shot}_{version}.{ext}', 'sequence': '/mnt/prods/{prod}/shots/{seq}', 'project': '/mnt/prods/{prod}'}


        Returns:
            The internal formats dictionary, resulting from the patterns.

        """
        return self._formats

    def get_format_for(self, label: str) -> str | None:
        """
        Returns the format string for the given label.
        As stored in the internal "formats" dictionary.

        Example
            >>> # the instance was created in earlier example
            >>> r = Resolver.get("any_id")
            >>> print(r.get_format_for("sequence"))
            /mnt/prods/{prod}/shots/{seq}

        Args:
            label: a pattern label, must exist as key in the patterns dictionary

        Returns:
            The string stored in the "formats" dictionary for the given label key.

        """
        return self._formats.get(label)

    def get_keys(self) -> dict[str, set]:
        """
        Each pattern is a string containing keywords, in curly brackets, eg "{project}", that will be matched by the Resolver.
        These keywords are stored in an internal "keys" dictionary, with labels as dict keys, and a set of keywords as value.

        Example
            >>> # the instance was created in earlier example
            >>> r = Resolver.get("any_id")
            >>> for k, v in r.get_keys().items(): \
                    print(f"{k} => {sorted(v)}")
            maya_file => ['ext', 'prod', 'seq', 'shot', 'version']
            any_file => ['ext', 'prod', 'seq', 'shot', 'version']
            sequence => ['prod', 'seq']
            project => ['prod']

        Returns:
            The internal "keys" dictionary
        """
        return self._keys

    def get_keys_for(self, label: str) -> set | None:
        """
        Returns the set of keywords for the given label.
        As stored in the internal "keys" dictionary.

        Example
            >>> # the instance was created in earlier example
            >>> r = Resolver.get("any_id")
            >>> print(r.get_keys_for("project"))
            {'prod'}

        Args:
            label: a pattern label, must exist as key in the patterns dictionary

        Returns:
            The set of keywords stored in the "keys" dictionary for the given label.

        """
        return self._keys.get(label)

    @functools.lru_cache()
    def resolve_first(self, string: str) -> tuple[str, dict[str, str]] | tuple[None, None]:
        """
        The Resolver has 3 resolve methods:
        - resolve_first
        - resolve_one
        - resolve_all

        This **resolve_first** resolves using the first available match.

        It receives a string to resolve.
        It runs over the list of patterns (internally over the list of re.Pattern) until the first match.

        This match generates a data dictionary.
        The method returns a tuple with the matching pattern label and the resolved data dictionary.

        Example
            >>> input = "/mnt/prods/hamlet/shots/sq010/sh010_v012.ma"
            >>> r = Resolver.get("any_id")
            >>> label, data = r.resolve_first(input)
            >>> print(f'Label: "{label}" - Data: "{data}"')
            Label: "maya_file" - Data: "{'prod': 'hamlet', 'seq': 'sq010', 'shot': 'sh010', 'version': 'v012', 'ext': 'ma'}"

            >>> input = "/mnt/prods/hamlet/shots/sq010/sh010_v012.nk"
            >>> r = Resolver.get("any_id")
            >>> label, data = r.resolve_first(input)
            >>> print(f'Label: "{label}" - Data: "{data}"')
            Label: "any_file" - Data: "{'prod': 'hamlet', 'seq': 'sq010', 'shot': 'sh010', 'version': 'v012', 'ext': 'nk'}"

        Args:
            string: a string to resolve, typically a path

        Returns:
            Tuple with the first matching pattern label and the resolved data dictionary

        """

        result = (None, None)

        if not string:
            return result

        for label, regex in self._regexes.items():

            match = regex.search(string)
            if match:
                data = template.match_to_dict(match, self.check_duplicate_placeholders)
                if data:
                    return label, data

        return result

    @functools.lru_cache()
    def resolve_one(self, string: str, label: str) -> dict[str, str] | dict:
        """
        The Resolver has 3 resolve methods:
        - resolve_first
        - resolve_one
        - resolve_all

        This **resolve_one** resolves using the designated pattern.

        It receives a string to resolve and a pattern label to match against.
        The Resolver then tries to match the string with the designated pattern.

        If the match happens, a data dictionary is generated and returned.
        If not, an empty dictionary is returned

        Examples
            >>> input = "/mnt/prods/hamlet/shots/sq010/sh010_v012.ma"
            >>> r = Resolver.get("any_id")
            >>> data = r.resolve_one(input, "maya_file")
            >>> print(data)
            {'prod': 'hamlet', 'seq': 'sq010', 'shot': 'sh010', 'version': 'v012', 'ext': 'ma'}

            >>> input = "/mnt/prods/hamlet/shots/sq010/sh010_v012.ma"
            >>> r = Resolver.get("any_id")
            >>> data = r.resolve_one(input, "any_file")
            >>> print(data)
            {'prod': 'hamlet', 'seq': 'sq010', 'shot': 'sh010', 'version': 'v012', 'ext': 'ma'}

            >>> data = r.resolve_one(input, "sequence")
            >>> print(data)
            {}

        Args:
            string: a string to resolve, typically a path, and the label of a pattern to match against

        Returns:
            Resolved data dictionary or empty dictionary if there is no match.

        """
        result: dict = {}

        if not string:
            return result

        regex = self._regexes.get(label)

        if regex:
            match = regex.search(string)
            if match:
                data = template.match_to_dict(match, self.check_duplicate_placeholders)
                if data:
                    return data

        return result

    @functools.lru_cache()
    def resolve_all(self, string: str) -> dict[str, dict[str, str]] | dict:
        """
        The Resolver has 3 resolve methods:
        - resolve_first
        - resolve_one
        - resolve_all

        This **resolve_all** resolves all possible matches.

        It receives a string to resolve.
        It runs over the list of patterns (internally over the list of re.Pattern).

        Every match generates a data dictionary.
        The method returns a dictionary with
        - each key: the matching pattern label
        - each value: the resolved data dictionary.

        If there is no match, an empty dictionary is returned.

        Example
            >>> from pprint import pprint
            >>> input = "/mnt/prods/hamlet/shots/sq010/sh010_v012.ma"
            >>> r = Resolver.get("any_id")
            >>> found = r.resolve_all(input)
            >>> pprint(found)
            {'any_file': {'ext': 'ma',
                          'prod': 'hamlet',
                          'seq': 'sq010',
                          'shot': 'sh010',
                          'version': 'v012'},
             'maya_file': {'ext': 'ma',
                           'prod': 'hamlet',
                           'seq': 'sq010',
                           'shot': 'sh010',
                           'version': 'v012'}}

            >>> input = "/mnt/prods/hamlet/shots/sq010/sh010_v012.nk"
            >>> found = r.resolve_all(input)
            >>> pprint(found)
            {'any_file': {'ext': 'nk',
                          'prod': 'hamlet',
                          'seq': 'sq010',
                          'shot': 'sh010',
                          'version': 'v012'}}

            >>> found = r.resolve_all("blablabla")
            >>> print(found)
            {}

        Args:
            string: a string to resolve, typically a path

        Returns:
            Dictionary with all matching pattern labels as keys, and the resolved data dictionaries as values.
            An empty dictionary if there is no match.

        """

        found: dict = {}

        if not string:
            return found

        for label, regex in self._regexes.items():
            match = regex.search(string)
            if match:
                data = template.match_to_dict(match, self.check_duplicate_placeholders)
                if data:
                    found[label] = data
        return found

    def format_first(self, data: dict[str, str]) -> tuple[str, str] | tuple[None, None]:
        """
        The Resolver has 3 format methods:
        - format_first
        - format_one
        - format_all

        This **format_first** formats using the first matching pattern.

        It receives a string data dictionary to format.
        It runs over the list of patterns (internally over the internal "formats" dict) until the first match.

        A match means:
        - the keys of the data dictionary matches the keys of the patterns "format" string,
        - the formatted string resolves back to an identical data dictionary.

        Once a match is found, a formatted string is generated and returned.
        The method returns a tuple with the label and the formatted string.
        Or a (None, None) tuple if there is no match.

        Example
            >>> r = Resolver.get("any_id")
            >>> data = { 'prod': 'hamlet', 'seq': 'sq010', 'shot': 'sh010', 'version': 'v012', 'ext': 'ma'}
            >>> formatted = r.format_first(data)
            >>> print(formatted)
            ('maya_file', '/mnt/prods/hamlet/shots/sq010/sh010_v012.ma')

            >>> data = {'prod': 'hamlet', 'seq': 'sq010'}
            >>> formatted = r.format_first(data)
            >>> print(formatted)
            ('sequence', '/mnt/prods/hamlet/shots/sq010')

        Args:
            data: a string data dictionary to format

        Returns:
            a tuple with the label and the formatted string, or (None, None) if there is no match.

        """

        result = (None, None)

        if not data:
            return result

        for label, _format in self._formats.items():

            if data.keys() != self._keys.get(label):
                continue

            formatted = _format.format(**data)

            # reverse check
            reverse_check = self.resolve_one(formatted, label)
            if reverse_check:
                return label, formatted
            else:
                log.debug(f'reverse check failed on "{formatted}" ({label})')

        return result

    def format_one(self, data: dict[str, str], label: str) -> str | None:
        """
        The Resolver has 3 format methods:
        - format_first
        - format_one
        - format_all

        This **format_one** formats using the designated pattern.

        It receives a string data dictionary to format, and a pattern label to match against.

        The Resolver then tries to match with the designated pattern.
        A match means:
        - the keys of the data dictionary matches the keys of the patterns "format" string,
        - the formatted string resolves back to an identical data dictionary.

        If the pattern matches, the generated formatted string is returned.
        Else, None is returned.

        Example
            >>> data = {'prod': 'hamlet', 'seq': 'sq010'}
            >>> r = Resolver.get("any_id")
            >>> formatted = r.format_one(data, "sequence")
            >>> print(formatted)
            /mnt/prods/hamlet/shots/sq010

            >>> formatted = r.format_one(data, "project")
            >>> print(formatted)
            None

        Args:
            data: a string data dictionary to format

        Returns:
            the formatted string, or None if the pattern does not match.

        """

        if not data:
            return None

        _format = self.get_format_for(label)

        if not _format:
            log.info(f'Asked to format with "{label}", but not found in {self.get_formats()}')
            return None

        if data.keys() != self._keys.get(label):
            return None

        formatted = _format.format(**data)

        # reverse check
        reverse_check = self.resolve_one(formatted, label)
        if reverse_check:
            return formatted
        else:
            log.debug(f'reverse check failed on "{formatted}" ({label})')
            return None

    def format_all(self, data: dict[str, str]) -> dict[str, dict[str, str]] | dict:
        """
        The Resolver has 3 format methods:
        - format_first
        - format_one
        - format_all

        This **format_all** formats using all possible matches.

        It receives a string data dictionary to format.
        It runs over the list of patterns (internally over the internal "formats" dict).

        Every match generates a formatted string.

        A match means:
        - the keys of the data dictionary matches the keys of the patterns "format" string,
        - the formatted string resolves back to an identical data dictionary.

        The method returns a dictionary with all matching pattern labels as keys, and the formatted strings as values.
        If there is no match, an empty dictionary is returned.

         Example
            >>> data = {'prod': 'hamlet', 'seq': 'sq010'}
            >>> r = Resolver.get("any_id")
            >>> formatted = r.format_all(data)
            >>> print(formatted)
            {'sequence': '/mnt/prods/hamlet/shots/sq010'}

            >>> data = { 'prod': 'hamlet', 'seq': 'sq010', 'shot': 'sh010', 'version': 'v012', 'ext': 'ma'}
            >>> r = Resolver.get("any_id")
            >>> formatted = r.format_all(data)
            >>> print(formatted)
            {'maya_file': '/mnt/prods/hamlet/shots/sq010/sh010_v012.ma', 'any_file': '/mnt/prods/hamlet/shots/sq010/sh010_v012.ma'}

        Args:
            data: a string data dictionary to format

        Returns:
            Dictionary with all matching pattern labels as keys, and the formatted strings as values.
            An empty dictionary if there is no match.

        """

        found: dict = {}

        if not data:
            return found

        for label, _format in self._formats.items():

            if data.keys() != self._keys.get(label):
                continue

            formatted = _format.format(**data)

            # reverse check
            reverse_check = self.resolve_one(formatted, label)
            if reverse_check:
                found[label] = formatted
            else:
                log.debug(f'reverse check failed on "{formatted}" ({label})')

        return found


if __name__ == "__main__":

    patterns = {'file': '{project}/{type:s}/{sequence}/bla/{ext:ma|mb}'}

    r = Resolver.get("any_id") or Resolver("any_id", patterns)  # getting from instance cache, or creating object

    # formatting checks the data
    data = {'project': 'hamlet',
            'type': 's',
            'sequence': 'sq010',
            'ext': 'mb'}
    path = r.format_one(data, "file")
    log.info(path)

    # if we want formatting without checks, we do it directly
    data = {'project': 'hamlet',
            'type': 's',
            'sequence': 'sq010',
            'foo': 'bar',
            'ext': 'not matching'}

    no_checks = r.get_format_for("file").format(**data)  # type: ignore  # type shortcut for test.
    log.info(no_checks)

    patterns = {'file': '{project}/{type:s}/{sequence}/{ext}/bla.{ext:ma|mb}'}
    r = Resolver("any_id", patterns)

    input = 'toto/s/1150/ma/bla.ma'
    found = r.resolve_one(input, 'file')
    log.info(found)
    keys = r.get_keys_for('file')
    log.info(keys)
    log.info(found.keys())

    p = Resolver.get("something else") or Resolver("something else", patterns=patterns)
    # override instance
    Resolver("something else", patterns=patterns)
