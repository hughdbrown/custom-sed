#!/usr/bin/env python
from __future__ import absolute_import

import re

from src.lib import SedFile, main as umain

RE_NEXT = re.compile(
    r"""
    ^
    (?P<left>\s*)
    (?P<key1>\w+)\s
    for\s
    (?P<key2>\w+)
    \sin\s
    (?P<coll1>\w+)
    \sif\s
    (?P<coll2>\w+)
    \[
        (?P<key3>\w+)
    \]
    (?P<right>.*?)
    $
""",
    re.VERBOSE,
)


class KeyValueInjector(SedFile):
    """
    Derivative of SedFile dedicated to replacing takign first element of list comprehension into
    calls to next().
    """

    def modify(self):
        match_iter = ((i, RE_NEXT.match(line)) for i, line in enumerate(self.data))
        matches = [(i, m) for i, m in match_iter if m]
        for i, m in matches:
            g = m.groupdict()
            left = g["left"]
            key1, key2, key3 = g["key1"], g["key2"], g["key3"]
            coll1, coll2 = g["coll1"], g["coll2"]
            right = g["right"]
            if key1 == key2 == key3 and coll1 == coll2:
                self.data[i] = "{}{} for {}, value in {}.items() if value{}".format(
                    left, key1, key1, coll1, right
                )
                self.modified = True


def main():
    umain(KeyValueInjector)


if __name__ == "__main__":
    main()
