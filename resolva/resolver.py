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

    def __init__(self, id: str, patterns: dict[str, str],
                 check_duplicate_placeholders: bool = True,
                 anchor_start: bool = True,
                 anchor_end: bool = True
                 ):

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
        instance = instance_cache.get(id)
        if not instance:
            log.info(f'No Resolver instance found with id "{id}"')
        return instance

    def get_id(self) -> Any:
        return self._id

    def get_labels(self) -> list[str]:
        """
        Returns the list of pattern labels.
        """
        return list(self._patterns.keys())

    def get_patterns(self) -> dict[str, str]:
        return self._patterns

    def get_pattern_for(self, label: str) -> str | None:
        return self._patterns.get(label)

    def get_regexes(self) -> dict[str, re.Pattern]:
        return self._regexes

    def get_regex_for(self, label: str) -> re.Pattern | None:
        return self._regexes.get(label)

    def get_formats(self) -> dict[str, str]:
        return self._formats

    def get_format_for(self, label: str) -> str | None:
        return self._formats.get(label)

    def get_keys(self) -> dict[str, set]:
        return self._keys

    def get_keys_for(self, label: str) -> set | None:
        return self._keys.get(label)

    @functools.lru_cache()
    def resolve_first(self, string: str) -> tuple[str, dict[str, str]] | tuple[None, None]:

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
