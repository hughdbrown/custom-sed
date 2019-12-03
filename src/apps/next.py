#!/usr/bin/env python
"""Script to replace use of next"""
from __future__ import absolute_import, print_function

import re

from src.lib import SedFile, main as umain

HAS_OPT_ARG = re.compile(
    r"""
    ^
    .*
    ,\s\w+
    $
""",
    re.VERBOSE,
)

RE_INDEX0 = re.compile(
    r"""
    ^
    (?P<whitespace>\s*)
    (?P<var>\w+\s=\s)
    \[
        (?P<comp>(.*for\s.*\sin\s.*?)|(\w+))
    \]
    \[0\]
    $
""",
    re.VERBOSE,
)

RE_NEXT_VAR = re.compile(
    r"""
    ^
    (?P<whitespace>\s*)
    (?P<var>\w+\s=\s)
    next\(
        (?P<next>(.*for\s.*\sin\s.*?)|[A-Za-z0-9_\[\]\(\)\.\'\"]+?)
    \)
    $
""",
    re.VERBOSE,
)

RE_NEXT_NOVAR = re.compile(
    r"""
    ^
    (?P<whitespace>\s*)
    (?P<keyword>(return|assert|yield)\s)?
    next\(
        (?P<next>(.*for\s.*\sin\s.*?)|[A-Za-z0-9_\[\]\(\)\.\'\"]+?)
    \)
    $
""",
    re.VERBOSE,
)

RE_NEXT_VAR2 = re.compile(
    r"""
    ^
    (?P<whitespace>\s*)
    (?P<var>
        ([\w\.\[\]\'\"\(\),\s]+?\s=\s) |
        (return\s) |
        (assert\s) |
        (yield\s)
    )
    next\(
    $
""",
    re.VERBOSE,
)


class NextInjector(SedFile):
    """
    Derivative of SedFile dedicated to replacing takign first element of list comprehension into
    calls to next().
    """

    first_func = "first_nodefault"

    def modify(self):
        # self._modify_index0()
        # self._modify_next_var()
        self._modify_next_var2()
        # self._modify_next_novar()

    def _modify_index0(self):
        start = self.modified
        match_iter = ((i, RE_INDEX0.match(line)) for i, line in enumerate(self.data))
        matches = [(i, m) for i, m in match_iter if m]
        for i, m in matches:
            g = m.groupdict()
            left = "{}{}".format(g["whitespace"], g["var"])
            right = "{}({})".format(NextInjector.first_func, g["comp"])
            self.data[i] = "{}{}".format(left, right)
            self.modified += 1

    def _modify_next_var(self):
        start = self.modified
        match_iter = ((i, RE_NEXT_VAR.match(line)) for i, line in enumerate(self.data))
        matches = [(i, m) for i, m in match_iter if m]
        for i, m in matches:
            g = m.groupdict()
            m = HAS_OPT_ARG.match(g["next"])
            if not m:
                left = "{}{}".format(g["whitespace"], g["var"])
                right = "{}({})".format(NextInjector.first_func, g["next"] or "")
                self.data[i] = "{}{}".format(left, right)
                self.modified += 1

    def _modify_next_var2(self):
        start = self.modified
        match_iter = ((i, RE_NEXT_VAR2.match(line)) for i, line in enumerate(self.data))
        matches = [(i, m) for i, m in match_iter if m]
        for i, m in matches:
            g = m.groupdict()
            self.data[i] = "{}{}{}(".format(
                g["whitespace"], g["var"], NextInjector.first_func
            )
            self.modified += 1

    def _modify_next_novar(self):
        start = self.modified
        match_iter = (
            (i, RE_NEXT_NOVAR.match(line)) for i, line in enumerate(self.data)
        )
        matches = [(i, m) for i, m in match_iter if m]
        for i, m in matches:
            g = m.groupdict()
            m = HAS_OPT_ARG.match(g["next"])
            if not m:
                self.data[i] = "{}{}{}({})".format(
                    g["whitespace"],
                    g["keyword"] or "",
                    NextInjector.first_func,
                    g["next"] or "",
                )
                self.modified += 1
            else:
                print("{}|{}".format(g["next"], m))


def main():
    umain(NextInjector)


if __name__ == "__main__":
    main(NextInjector)
