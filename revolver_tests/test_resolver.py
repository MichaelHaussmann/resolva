from revolver import Resolver
from revolver_tests.data import test_strings
from revolver_tests.pattern import sid_templates

Resolver(id="sids", patterns=sid_templates)
r = Resolver.get("sids")

for s in test_strings[0:10]:
    print('*'*100)
    print(f'Input: {s}')

    name, resolved = r.resolve_first(s).popitem()
    # formatted = r.format_one(resolved, name)
    formatted = r.format_first(resolved)

    print(f"Back and forth: {s} -> {formatted}")
    continue


    print(' ' * 50)
