from resolva import Resolver

from resolva.utils import log  # type: ignore
log.setLevel(log.INFO)  # type: ignore

templates = {"project": "{project}/{type:s}/{sequence}[/{shot}]/{ext:vdb|abc}"}

r = Resolver.get("-") or Resolver(id="-", patterns=templates)

PASS = ['hamlet/s/100/50/abc', 'hamlet/s/100/abc', 'hamlet/s//abc', 'hamlet/s///abc']
FAIL = ['hamlet/s*/100/abc', 'hamlet/100/abc']

test_strings = PASS + FAIL

for i, s in enumerate(test_strings):

    log.info('*'*100)
    log.info(f'Input {i}: {s}')

    log.info(f"\tFirst:")
    k, v = r.resolve_first(s)
    if k:
        log.info(f"\t\t{k}: {v}")
    else:
        log.warning(f"Did not resolve {s}")
        continue

