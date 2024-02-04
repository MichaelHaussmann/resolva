from __future__ import annotations
from functools import lru_cache

from revolver import template, formatter
import revolver.utils

instance_cache = {}


class Resolver:

    def __init__(self, id: str, patterns: dict[str, str]):

        self._patterns = patterns
        self._regexes = {k: template.construct_regular_expression(v) for k, v in patterns.items()}

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

    def regexes(self):
        return self._regexes

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

        for name, pattern in self._patterns.items():

            formatted = formatter.format(data, pattern)

            if formatted:

                return {name: formatted}

    def format_one(self, data: dict[str, str], name: str) -> str | None:

        pattern = self._patterns.get(name)

        return formatter.format(data, pattern)

    def format_all(self, data: dict[str, str]) -> dict[str, str] | None:

        found = {}

        for name, pattern in self._patterns.items():

            formatted = formatter.format(data, pattern)

            if formatted:

                found[name] = formatted

        return found


if __name__ == "__main__":
    pass
