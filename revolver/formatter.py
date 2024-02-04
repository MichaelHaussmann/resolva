"""
This code is taken and derived from Lucidity.

https://gitlab.com/4degrees/lucidity/
https://lucidity.readthedocs.io

copyright: Copyright (c) 2013 Martin Pengelly-Phillips
licence: Apache License, Version 2.0, January 2004, http://www.apache.org/licenses

"""
import re
import functools

from revolver.utils import RevolverException

_STRIP_EXPRESSION_REGEX = re.compile(r'{(.+?)(:(\\}|.)+?)}')
_PLAIN_PLACEHOLDER_REGEX = re.compile(r'{(.+?)}')


def format(data, pattern):
    '''Return a path formatted by applying *data* to this template.

    Raise :py:class:`~lucidity.error.FormatError` if *data* does not
    supply enough information to fill the template fields.

    '''
    format_specification = _construct_format_specification(
        pattern
    )

    return _PLAIN_PLACEHOLDER_REGEX.sub(
        functools.partial(_format, data=data),
        format_specification
    )


def _format(match, data):
    '''Return value from data for *match*.'''
    placeholder = match.group(1)
    parts = placeholder.split('.')

    try:
        value = data
        for part in parts:
            value = value[part]

    except (TypeError, KeyError):
        print(
            'Could not format data {0!r} due to missing key {1!r}. ({2})'
            .format(data, placeholder, match)
        )
        return None

    else:
        return value


def _construct_format_specification(pattern):
    '''Return format specification from *pattern*.'''
    return _STRIP_EXPRESSION_REGEX.sub('{\g<1>}', pattern)


if __name__ == "__main__":

    # pat = '{project}/{type:s}/{sequence}/{shot}/{task}/{version}/{state}/{ext:scenes}'
    pat = '{project}/{type:s}/{sequence}/bla'
    data = {'project': 'hamlet',
            'type': 's',
            'sequence': 'sq010',
            'bidule': 'john'}
    print(format(data, pat))
