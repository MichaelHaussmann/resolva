from datetime import datetime
from resolva import Resolver
from resolva_tests.data import test_strings
from resolva_tests.pattern import sid_templates

from resolva.utils import log
log.setLevel(log.INFO)

Resolver(id="sids", patterns=sid_templates)
r = Resolver.get("sids")

start = datetime.now()
count = 0

for i, s in enumerate(test_strings):
    log.info('*'*100)
    log.info(f'Input {i}: {s}')

    for name_resolved, resolved in r.resolve_all(s).items():

        log.info(f'\tResolved:')
        log.info(f'\t\t"{name_resolved}" ({resolved})')

        # resolve_all and format first do not necessarily return the same type
        # format first will not work here because
        formatted = r.format_one(resolved, name_resolved)

        log.info(f"\tBack and forth:")
        log.info(f'\t\t"{name_resolved}" {s} -> {formatted}')
        assert str(s) == str(formatted)

        log.info(f"\tAll: ({resolved})")
        for k, v in r.format_all(resolved).items():
            log.info(f"\t\t{k}: {v}")

        count = count + 1

    log.info(' ' * 50)

end = datetime.now()
log.warning(f"\nDuration: {end-start} for {i} items. \n"
      f"Average: {(end-start)/count} per item and resolve operations. \n"
      f"Pattern lines: {len(r.get_keys())}. \n"
      f"(set log level to log.WARNING to measure time without print impact)")
