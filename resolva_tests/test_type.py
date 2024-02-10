from datetime import datetime
from resolva import Resolver
from resolva_tests.data import test_strings
from resolva_tests.pattern import sid_templates

from resolva.utils import log
log.setLevel(log.INFO)

Resolver(id="sids", patterns=sid_templates)
r = Resolver.get("sids")

start = datetime.now()

for i, s in enumerate(test_strings):
    log.info('*'*100)
    log.info(f'Input {i}: {s}')

    found = {}
    for i, data in r.resolve_all(s).items():
        for j, sid in r.format_all(data).items():
            found[j] =


    name_resolved, resolved = r.resolve_first(s)
    # formatted = r.format_one(resolved, name)
    name_formatted, formatted = r.format_first(resolved)

    log.info(f"Back and forth: ({name_resolved}) {s} -> {formatted} ({name_formatted})")
    if name_resolved:
        assert name_resolved == name_formatted
        assert str(s) == str(formatted)

    log.info(f"All: ({resolved})")
    for k, v in r.format_all(resolved).items():
        log.info(f"\t{k}: {v}")

    log.info(' ' * 50)

end = datetime.now()
log.warning(f"\nDuration: {end-start} for {i} items. \n"
      f"Average: {(end-start)/i} per item (for 3 resolve operations). \n"
      f"Pattern lines: {len(r.get_keys())}. \n")
