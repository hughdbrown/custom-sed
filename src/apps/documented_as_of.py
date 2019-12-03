#!/usr/bin/env python
from __future__ import absolute_import

import re

from lib import SedFile, main as umain

RE_NEXT = re.compile(
    r"""
    ^
    (?P<left>\s*.*?)
    public_as_of='
    (?P<public>[a-zA-Z0-9_\.]+)
    '
    (?P<middle>.*?)
    documented_as_of='
    (?P<documented>[a-zA-Z0-9_\.]+)
    '
    (?P<right>.*)
    $
""",
    re.VERBOSE,
)


class PublicDocumented(SedFile):
    """
    Derivative of SedFile dedicated to removing redundant 'documented_as_of'
    """

    def modify(self):
        match_iter = ((i, RE_NEXT.match(line)) for i, line in enumerate(self.data))
        matches = [(i, m) for i, m in match_iter if m]
        for i, m in matches:
            g = m.groupdict()
            left, middle, right = g["left"], g["middle"], g["right"]
            public, documented = g["public"], g["documented"]
            if public == documented:
                if middle == ', ' and right == ')':
                    self.data[i] = "{}public_as_of='{}')".format(left, public)
                else:
                    self.data[i] = "{}public_as_of='{}'{}{}".format(
                        left, public, middle, right
                    )
                self.modified = True


def main():
    umain(PublicDocumented)


if __name__ == "__main__":
    main()
