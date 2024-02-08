from datetime import datetime
from revolver import Resolver
from revolver_tests.data import test_strings
from revolver_tests.pattern import sid_templates


Resolver(id="sids", patterns=sid_templates)

r = Resolver.get("sids")

start = datetime.now()

for i, s in enumerate(test_strings):

    print('*'*100)
    print(f'Input {i}: {s}')

    print(f"First:")
    k, v = r.resolve_first(s) or (None, None)
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

end = datetime.now()
print(f"Duration: {end-start} for {i} items. \n"
      f"Average: {(end-start)/i} per item (for 3 resolve operations). \n"
      f"Pattern lines: {len(r.get_keys())}. \n"
      f"(Including ~50% print time.)")
