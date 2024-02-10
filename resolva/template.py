"""
This code is taken and derived from Lucidity.

https://gitlab.com/4degrees/lucidity/
https://lucidity.readthedocs.io

copyright: Copyright (c) 2013 Martin Pengelly-Phillips
licence: Apache License, Version 2.0, January 2004, http://www.apache.org/licenses

"""
import functools
from collections import defaultdict
import re
import sys

from resolva.utils import ResolvaException

_default_placeholder_expression = "[^/]*"  # spil
_STRIP_EXPRESSION_REGEX = re.compile(r'{(.+?)(:(\\}|.)+?)}')
_PLAIN_PLACEHOLDER_REGEX = re.compile(r'{(.+?)}')


def construct_regular_expression(pattern, anchor_start=True, anchor_end=True):
    '''Return a regular expression to represent *pattern*.'''
    # Escape non-placeholder components.
    # expression = re.sub(
    #     r'(?P<placeholder>{(.+?)(:(\\}|.)+?)?})|(?P<other>.+?)',
    #     self._escape,
    #     pattern
    # )
    expression = pattern

    # Replace placeholders with regex pattern.
    expression = re.sub(
        r'{(?P<placeholder>.+?)(:(?P<expression>(\\}|.)+?))?}',
        functools.partial(
            _convert, placeholder_count=defaultdict(int)
        ),
        expression
    )

    # anchoring
    if anchor_start:
        expression = '^{0}'.format(expression)
    if anchor_end:
        expression = '{0}$'.format(expression)

    # Compile expression.
    try:
        compiled = re.compile(expression)
    except re.error as error:
        if any([
            'bad group name' in str(error),
            'bad character in group name' in str(error)
        ]):
            raise ValueError('Placeholder name contains invalid '
                             'characters.')
        else:
            _, value, traceback = sys.exc_info()
            message = 'Invalid pattern: {0}| {1}'.format(value, traceback)
            raise ValueError(message)

    return compiled


def _convert(match, placeholder_count):
    '''Return a regular expression to represent *match*.

    *placeholder_count* should be a `defaultdict(int)` that will be used to
    store counts of unique placeholder names.

    '''
    placeholder_name = match.group('placeholder')

    # The re module does not support duplicate group names. To support
    # duplicate placeholder names in templates add a unique count to the
    # regular expression group name and strip it later during parse.
    placeholder_count[placeholder_name] += 1
    placeholder_name += '{0:03d}'.format(
        placeholder_count[placeholder_name]
    )

    expression = match.group('expression')
    if expression is None:
        expression = _default_placeholder_expression

    # Un-escape potentially escaped characters in expression.
    expression = expression.replace('\\{', '{').replace('\\}', '}')

    return r'(?P<{0}>{1})'.format(placeholder_name, expression)


def match_to_dict(match, check_duplicate_placeholders=True):
    """
    Derived from lucidity.Template.parse function.

    Args:
        match: regex match
        check_duplicate_placeholders: if we should check that duplicate placeholders have identical values.

    Returns:
        the dictionary of key values extracted from the regex match.
    """

    data = {}
    for key, value in match.groupdict().items():
        # Strip number that was added to make group name unique.
        key = key[:-3]

        # If check_duplicate_placeholders is True, ensure that
        # all duplicate placeholders extract the same value.
        if check_duplicate_placeholders:
            if key in data:
                if data[key] != value:
                    raise ResolvaException(
                        'Different extracted values for placeholder '
                        '{0!r} detected. Values were {1!r} and {2!r}.'
                        .format(key, data[key], value)
                    )

        data[key] = value

    return data


def construct_format_specification(pattern):
    '''Return format specification from *pattern*.'''
    return _STRIP_EXPRESSION_REGEX.sub('{\g<1>}', pattern)


def get_keys(pattern):
    return _PLAIN_PLACEHOLDER_REGEX.findall(construct_format_specification(pattern))


if __name__ == "__main__":

    pat = '{project}/{type:s}/{sequence}/{shot}/{task}/{version}/{state}/{ext:ma|mb}'
    print(f'Pattern: \n{pat}\n')

    reg = construct_regular_expression(pat)
    print(f'Regex: \n{reg}\n')

    fmt = construct_format_specification(pat)
    print(f'Formattable: \n{fmt}\n')
