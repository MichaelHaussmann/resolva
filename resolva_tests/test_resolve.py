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

    log.info(f"\tFirst:")
    k, v = r.resolve_first(s)
    if k:
        log.info(f"\t\t{k}: {v}")

    log.info(f"\tAll:")
    for k, v in r.resolve_all(s).items():
        log.info(f"\t\t{k}: {v}")

    log.info(f"\tBy name:")
    for name in r.get_names():
        found = r.resolve_one(s, name)
        if found:
            log.info(f'\t\tKeys: {r.get_keys(name)}')
            log.info(f'\t\t{name} -> {found}')
            assert found.keys() == r.get_keys(name)

    log.info(' ' * 50)

end = datetime.now()
log.warning(f"\nDuration: {end-start} for {i} items. \n"
      f"Average: {(end-start)/i} per item (for 3 resolve operations). \n"
      f"Pattern lines: {len(r.get_keys())}. \n"
      f"(set log level to log.WARNING to measure time without print impact)")
