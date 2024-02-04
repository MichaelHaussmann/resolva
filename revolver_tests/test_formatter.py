from revolver import Resolver
from revolver_tests.data import test_strings
from revolver_tests.pattern import sid_templates


Resolver(id="sids", patterns=sid_templates)

r = Resolver.get("sids")

for s in test_strings:
    print('*'*100)
    print(f'Input: {s}')

    print(f"First:")
    for k, v in r.resolve_first(s).items():
        print(f"\t{k}: {v}")
    print(f"All:")
    for k, v in r.resolve_all(s).items():
        print(f"\t{k}: {v}")

    print(f"By name:")
    for name in r.get_names():
        found = r.resolve_one(s, name)
        if found:
            print(f'\t{name} -> {found}')

    print(' ' * 50)
