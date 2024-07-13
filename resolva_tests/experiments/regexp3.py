import re

template = "{project>}/{type:s}/{sequence}-{shot}/{ext:vdb|abc}"

# optional
template = "{project>}/{type:s}/{sequence}[-{shot}]/{ext:vdb|abc}"


pattern = r"(?P<project>.*)/(?P<type>s)/(?P<sequence>[a-zA-Z0-9]*)(?:-(?P<shot>[^/]*)?)?/(?P<ext>vdb|abc)"
# pattern = r"(?P<project>.*)/(?P<type>s)/(?P<sequence>[^/]*)-(?P<shot>[^/]*)/(?P<ext>vdb|abc)"

# [ => (?:
# ] => ?)?

# pattern = "(?P<project>.*)/(?P<type>s)/(?P<sequence>[^/]*)[.(?P<shot>[^/]*)/(?P<ext>vdb|abc)"

r = re.compile(pattern)

PASS = ['hamlet/s/100-50/abc', 'hamlet/s/100/abc', 'hamlet/s/-/abc', 'hamlet/s/100-/abc']
FAIL = [] # ['hamlet/s///abc', 'hamlet/s*/100/abc', 'hamlet/s/100/200/abc', 'hamlet/100/abc']


for p in PASS:
    found = r.search(p).groups()
    print(f"Expected PASS: {p} => {found}")

print("*"*50)
for p in FAIL:
    try:
        found = r.search(p).groups()
        print(f"This should FAIL: {p}, but we found: {found}")
    except Exception as e:
        print(f"Expected FAIL: {p}")
