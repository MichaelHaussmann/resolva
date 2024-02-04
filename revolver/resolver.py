from __future__ import annotations

from functools import lru_cache

# from typing import List, Dict

import revolver.utils
from revolver import template

instance_cache = {}


class Resolver:

    def __init__(self, name: str, patterns: list[dict[str, str]]):

        self._patterns = patterns
        self._regexes = {k: template.construct_regular_expression(patterns.get(k)) for k in patterns}

        print(f'Resolver init of "{name}"')

        # TODO: warn if exists already in instance cache - overrides instance cache
        instance_cache[name] = self

    @staticmethod
    def get(name):
        instance = instance_cache.get(name)
        if not instance:
            raise revolver.utils.RevolverException(f'No Resolver instance found with name "{name}"')
        return instance

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

