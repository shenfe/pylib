# coding: utf8

from __future__ import print_function
from __future__ import division

import sys


is_python3 = sys.version_info[0] == 3


def to_unicode(s):

    if is_python3:
        if isinstance(s, bytes):
            return s.decode('utf8')
        return s

    if isinstance(s, str):
        return s.decode('utf8')
    return s


def to_utf8str(s):

    if is_python3:
        if isinstance(s, str):
            return s.encode('utf8')
        return s

    if isinstance(s, unicode):
        return s.encode('utf8')
    return s
