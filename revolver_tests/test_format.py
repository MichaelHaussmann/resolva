from revolver import Resolver
from revolver_tests.data import test_strings
from revolver_tests.pattern import sid_templates

Resolver(id="sids", patterns=sid_templates)
r = Resolver.get("sids")

for s in test_strings:
    print('*'*100)
    print(f'Input: {s}')

    name_resolved, resolved = r.resolve_first(s).popitem()
    # formatted = r.format_one(resolved, name)
    name_formatted, formatted = r.format_first(resolved).popitem()

    print(f"Back and forth: ({name_resolved}) {s} -> {formatted} ({name_formatted})")
    assert name_resolved == name_formatted
    assert str(s) == str(formatted)

    print(f"All:")
    for k, v in r.format_all(resolved).items():
        print(f"\t{k}: {v}")


    print(' ' * 50)
