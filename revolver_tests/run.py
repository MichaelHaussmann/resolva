from revolver import Resolver
from revolver_tests.data import test_strings
from revolver_tests.pattern import sid_templates

Resolver(name="sids", patterns=sid_templates)

r = Resolver.get("sids")

for s in test_strings:
    print(f'Input: {s}')

    print(f"First: {r.resolve_first(s)}")
    print(f"All:   {r.resolve_all(s)}")
