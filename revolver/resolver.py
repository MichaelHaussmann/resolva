from __future__ import annotations
from functools import lru_cache
import string as _string

from revolver import template
import revolver.utils

instance_cache = {}


class Resolver:

    def __init__(self, id: str, patterns: dict[str, str]):

        self._patterns = patterns
        self._regexes = {k: template.construct_regular_expression(v) for k, v in patterns.items()}
        self._formats = {k: template.construct_format_specification(v) for k, v in patterns.items()}
        self._keys = {k: set([t[1] for t in _string.Formatter().parse(v) if t[1] is not None]) for k, v in self._formats.items()}

        print(f'Resolver init of "{id}"')

        # TODO: warn if exists already in instance cache - overrides instance cache
        instance_cache[id] = self

    @staticmethod
    def get(id: str) -> Resolver:
        instance = instance_cache.get(id)
        if not instance:
            raise revolver.utils.RevolverException(f'No Resolver instance found with id "{id}"')
        return instance

    def get_names(self) -> list[str]:
        """
        Returns the list of pattern names.
        """
        return list(self._regexes.keys())

    def get_patterns(self, name=None):
        if name:
            return self._patterns.get(name)
        return self._patterns

    def get_regexes(self, name=None):
        if name:
            return self._regexes.get(name)
        return self._regexes

    def get_formats(self, name=None):
        if name:
            return self._formats.get(name)
        return self._formats

    def get_keys(self, name=None):
        if name:
            return self._keys.get(name)
        return self._keys

    @lru_cache()
    def resolve_first(self, string: str) -> dict[str, dict[str, str]] | None:

        for name, regex in self._regexes.items():

            match = regex.search(string)
            if match:
                data = template.match_to_dict(match)
                if data:
                    return {name: data}

    @lru_cache()
    def resolve_one(self, string: str, name: str) -> dict[str, str] | None:

        regex = self._regexes.get(name)

        if regex:
            match = regex.search(string)
            if match:
                data = template.match_to_dict(match)
                if data:
                    return data

    @lru_cache()
    def resolve_all(self, string: str) -> dict[str, dict[str, str]] | None:

        found = {}
        for name, regex in self._regexes.items():
            match = regex.search(string)
            if match:
                data = template.match_to_dict(match)
                if data:
                    found[name] = data

        if found:
            return found

    def format_first(self, data: dict[str, str]) -> dict[str, str] | None:

        for name, _format in self._formats.items():

            if data.keys() != self._keys.get(name):
                continue

            formatted = _format.format(**data)

            # reverse check
            reverse_check = self.resolve_one(formatted, name)
            if reverse_check:
                return {name: formatted}

    def format_one(self, data: dict[str, str], name: str) -> str | None:

        _format = self._formats.get(name)

        if data.keys() != self._keys.get(name):
            return None

        formatted = _format.format(**data)

        # reverse check
        reverse_check = self.resolve_one(formatted, name)
        if reverse_check:
            return formatted

    def format_all(self, data: dict[str, str]) -> dict[str, dict[str, str]] | None:

        found = {}

        for name, _format in self._formats.items():

            if data.keys() != self._keys.get(name):
                continue

            formatted = _format.format(**data)

            # reverse check
            reverse_check = self.resolve_one(formatted, name)
            if reverse_check:
                found[name] = formatted

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
    print(path)

    # if we want formatting without checks, we do it directly
    data = {'project': 'hamlet',
            'type': 's',
            'sequence': 'sq010',
            'foo': 'bar',
            'ext': 'not matching'}

    no_checks = r.get_formats("file").format(**data)
    print(no_checks)


