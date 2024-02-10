from datetime import datetime
from resolva import Resolver  # type: ignore
from resolva_tests.data import test_strings  # type: ignore
from resolva_tests.pattern import sid_templates  # type: ignore

from resolva.utils import log  # type: ignore
log.setLevel(log.INFO)  # type: ignore

r = Resolver.get("sids") or Resolver(id="sids", patterns=sid_templates)

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

    log.info(f"\tBy label:")
    for label in r.get_labels():
        found = r.resolve_one(s, label)
        if found:
            log.info(f'\t\tKeys: {r.get_keys_for(label)}')
            log.info(f'\t\t{label} -> {found}')
            assert found.keys() == r.get_keys_for(label)

    log.info(' ' * 50)

end = datetime.now()
log.warning(f"\nDuration: {end-start} for {i} items. \n"
      f"Average: {(end-start)/i} per item (for 3 resolve operations). \n"
      f"Pattern lines: {len(r.get_keys())}. \n"
      f"(set log level to log.WARNING to measure time without print impact)")
