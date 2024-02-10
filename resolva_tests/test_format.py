from datetime import datetime
from resolva import Resolver
from resolva_tests.data import test_strings
from resolva_tests.pattern import sid_templates

from resolva.utils import log
log.setLevel(log.INFO)  # type: ignore

r = Resolver.get("sids") or Resolver(id="sids", patterns=sid_templates)

start = datetime.now()

for i, s in enumerate(test_strings):
    log.info('*'*100)
    log.info(f'Input {i}: {s}')

    label_resolved, resolved = r.resolve_first(s)
    label_formatted, formatted = r.format_first(resolved)  # type: ignore

    # This tests that resolve_first and format first return the same type.
    log.info(f"\tBack and forth: ")
    log.info(f"\t\t({label_resolved}) {s} ---> {formatted} ({label_formatted})")
    if label_resolved:
        assert label_resolved == label_formatted
        assert str(s) == str(formatted)

    log.info(f"\tAll: ({resolved})")
    for k, v in r.format_all(resolved).items():
        log.info(f"\t\t{k}: {v}")

    log.info(' ' * 50)

end = datetime.now()
log.warning(f"\nDuration: {end-start} for {i} items. \n"
      f"Average: {(end-start)/i} per item (for 3 resolve operations). \n"
      f"Pattern lines: {len(r.get_keys())}. \n"
      f"(set log level to log.WARNING to measure time without print impact)")
