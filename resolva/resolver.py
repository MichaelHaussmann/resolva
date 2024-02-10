from __future__ import annotations
from typing import Any
import functools
from functools import lru_cache
import string as _string
import re

from resolva import template
from resolva.utils import log, ResolvaException

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
            raise ResolvaException(f'Keys not identical in check: "{self._keys}" vs "{self._keysB}"')

        self._keys = _keys
        self.check_duplicate_placeholders = check_duplicate_placeholders

        log.info(f'Resolver class init - id: "{id}"')

        # instance cache
        if instance_cache.get(id):
            log.info(f'Resolver instance already exists at "{id}". Will be overriden with: {self}')
        instance_cache[id] = self

    def __str__(self):
        return f"[resolva.Resolver] ID: [{self.get_id()}] - Pattern names: {self.get_names()}"

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

    def get_names(self) -> list[str]:
        """
        Returns the list of pattern names.
        """
        return list(self._regexes.keys())

    def get_patterns(self, name=None) -> dict[str, str] | str:
        if name:
            return self._patterns.get(name)
        return self._patterns

    def get_regexes(self, name=None) -> dict[str, re.Pattern] | re.Pattern:
        if name:
            return self._regexes.get(name)
        return self._regexes

    def get_formats(self, name=None) -> dict[str, str] | str:
        if name:
            return self._formats.get(name)
        return self._formats

    def get_keys(self, name=None) -> dict[str, set] | set:
        if name:
            return self._keys.get(name)
        return self._keys

    @lru_cache()
    def resolve_first(self, string: str) -> tuple[str, dict[str, str]] | tuple[None, None]:

        result = (None, None)

        if not string:
            return result

        for name, regex in self._regexes.items():

            match = regex.search(string)
            if match:
                data = template.match_to_dict(match, self.check_duplicate_placeholders)
                if data:
                    return name, data

        return result

    @lru_cache()
    def resolve_one(self, string: str, name: str) -> dict[str, str] | None:

        if not string:
            return None

        regex = self._regexes.get(name)

        if regex:
            match = regex.search(string)
            if match:
                data = template.match_to_dict(match, self.check_duplicate_placeholders)
                if data:
                    return data

        return None

    @lru_cache()
    def resolve_all(self, string: str) -> dict[str, dict[str, str]] | {}:

        found = {}

        if not string:
            return found

        for name, regex in self._regexes.items():
            match = regex.search(string)
            if match:
                data = template.match_to_dict(match, self.check_duplicate_placeholders)
                if data:
                    found[name] = data
        return found

    def format_first(self, data: dict[str, str]) -> tuple[str, str] | tuple[None, None]:

        result = (None, None)

        if not data:
            return result

        for name, _format in self._formats.items():

            if data.keys() != self._keys.get(name):
                continue

            formatted = _format.format(**data)

            # reverse check
            reverse_check = self.resolve_one(formatted, name)
            if reverse_check:
                return name, formatted
            else:
                log.debug(f'reverse check failed on "{formatted}" ({name})')

        return result

    def format_one(self, data: dict[str, str], name: str) -> str | None:

        if not data:
            return None

        _format = self._formats.get(name)

        if data.keys() != self._keys.get(name):
            return None

        formatted = _format.format(**data)

        # reverse check
        reverse_check = self.resolve_one(formatted, name)
        if reverse_check:
            return formatted
        else:
            log.debug(f'reverse check failed on "{formatted}" ({name})')

    def format_all(self, data: dict[str, str]) -> dict[str, dict[str, str]] | {}:

        found = {}

        if not data:
            return found

        for name, _format in self._formats.items():

            if data.keys() != self._keys.get(name):
                continue

            formatted = _format.format(**data)

            # reverse check
            reverse_check = self.resolve_one(formatted, name)
            if reverse_check:
                found[name] = formatted
            else:
                log.debug(f'reverse check failed on "{formatted}" ({name})')

        return found


if __name__ == "__main__":

    patterns = {'file': '{project}/{type:s}/{sequence}/bla/{ext:ma|mb}'}

    Resolver("any_id", patterns)
    r = Resolver.get("any_id")  # getting from instance cache.

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

    no_checks = r.get_formats("file").format(**data)
    log.info(no_checks)

    patterns = {'file': '{project}/{type:s}/{sequence}/{ext}/bla.{ext:ma|mb}'}
    r = Resolver("any_id", patterns)

    input = 'toto/s/1150/ma/bla.ma'
    found = r.resolve_one(input, 'file')
    log.info(found)
    keys = r.get_keys('file')
    log.info(keys)
    log.info(found.keys())

    p = Resolver.get("something else") or Resolver("something else", patterns=patterns)
    # override instance
    Resolver("something else", patterns=patterns)
