from string import Formatter

pattern = '{project}/{type:s}/{sequence}/{shot}/{task}/{version}/{state}[/{node}]/{ext:vdb|abc}'
pattern = '{project}/{type:s}/{sequence}/{shot}/{task}/{version}/{state}/{ext:vdb|abc}'

version_regex = "mnt/prod/(?P<prod>.*)/sequence/(?P<sequence>.*)/(?P<shot>.*)/(?P<department>.*)/render/.*-.*-v(?P<version>.*)"


keys = [fname for _, fname, _, _ in Formatter().parse(pattern) if fname]

# building pattern for filesearch
# keys = get_pattern_keys(conf.pattern)
searcher = {k: "*" for k in keys}
# searcher.update(kwargs)
search_pattern = conf.version_folder_pattern.format(**searcher)
log.debug(f"Search pattern: {search_pattern}")

# pattern for entity / version extraction
r = re.compile(conf.version_regex)

# parsing paths to extract entity / versions
collected = defaultdict(list)
for path in conf.root.glob(search_pattern):
    log.debug(f"looking up {path}")
    found = [m.groupdict() for m in r.finditer(str(path))]
    if found:
        fields = found[0]
        version = fields.pop("version")
        fields = dict(sorted(fields.items()))  # noqa # sorting the dict alphabetically
        uri = to_string(fields)
        collected[uri].append(version)


(?P<project001>[^/]*)/(?P<type001>s)/(?P<sequence001>[^/]*)/(?P<shot001>[^/]*)/(?P<task001>[^/]*)/(?P<version001>[^/]*)/(?P<state001>[^/]*)[/(?P<node001>[^/]*)]/(?P<ext001>vdb|abc)
