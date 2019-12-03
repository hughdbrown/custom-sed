#!/usr/bin/env python
from __future__ import absolute_import

import re

from src.lib import SedFile, main as umain

RE_CONSTANT = re.compile(
    r"""
    ^
    (?P<left>.*)
    \[
        (?P<number>\d+)
        \sfor\s_\sin\s
        range\(
            (?P<expr>.*?)
        \)
    \]
    (?P<right>.*)
    $
""",
    re.VERBOSE,
)

RE_CONSTANT2 = re.compile(
    r"""
    ^
    (?P<left>.*)
    \[
        (?P<number>\d+)
        \sfor\s_\sin\s
        (?P<expr>.*?)
    \]
    (?P<right>.*)
    $
""",
    re.VERBOSE,
)


class ConstatArrayInjector(SedFile):
    """
    Derivative of SedFile dedicated to injecting
    into python files.
    """

    def modify(self):
        self._modify1()
        self.modify2()

    def _modify1(self):
        match_iter = ((i, RE_CONSTANT.match(line)) for i, line in enumerate(self.data))
        matches = [(i, m) for i, m in match_iter if m]
        for i, m in matches:
            g = m.groupdict()
            self.data[i] = "{}[{}] * {}{}".format(
                g["left"], g["number"], g["expr"], g["right"]
            )
            self.modified = True

    def _modify2(self):
        match_iter = ((i, RE_CONSTANT2.match(line)) for i, line in enumerate(self.data))
        matches = [(i, m) for i, m in match_iter if m]
        for i, m in matches:
            g = m.groupdict()
            self.data[i] = "{}[{}] * len({}){}".format(
                g["left"], g["number"], g["expr"], g["right"]
            )
            self.modified = True


def main():
    umain(ConstatArrayInjector)


if __name__ == "__main__":
    main()
