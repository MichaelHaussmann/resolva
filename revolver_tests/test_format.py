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

    name_resolved, resolved = r.resolve_first(s) or (None, None)
    # formatted = r.format_one(resolved, name)
    name_formatted, formatted = r.format_first(resolved) or (None, None)

    print(f"Back and forth: ({name_resolved}) {s} -> {formatted} ({name_formatted})")
    if name_resolved:
        assert name_resolved == name_formatted
        assert str(s) == str(formatted)

    print(f"All: ({resolved})")
    for k, v in r.format_all(resolved).items():
        print(f"\t{k}: {v}")

    print(' ' * 50)

end = datetime.now()
print(f"Duration: {end-start} for {i} items. \n"
      f"Average: {(end-start)/i} per item (for 1 resolve and 2 formatting operations). \n"
      f"Pattern lines: {len(r.get_keys())}. \n"
      f"(Including ~50% print time.)")
