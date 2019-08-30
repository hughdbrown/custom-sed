#!/usr/bin/env python
from __future__ import absolute_import

import re

from lib import SedFile, main

RE_ROLE_HELPER1 = re.compile(
    r"""
    ^
    (?P<left>\s*)
    role_helper\.set_initial_owner_permissions
    \(
        (?P<first>[\d\w\._]+)
        ,\s+
        (?P<second>[\d\w\._]+)
    \)
    $
""",
    re.VERBOSE,
)

RE_ROLE_HELPER2 = re.compile(
    r"""
    ^
    (?P<left>\s*)
    role_helper.set_initial_can_read_info_only_permission
    \(
        (?P<first>[\d\w\._]+)
        ,\s+
        (?P<second>[\d\w\._]+)
    \)
    $
""",
    re.VERBOSE,
)


class RoleHelperInjector(SedFile):
    """
    Derivative of SedFile dedicated to replacing takign first element of list comprehension into
    calls to next().
    """

    def modify(self):
        self._modify1()
        self._modify2()

    def _modify1(self):
        match_iter = (
            (i, RE_ROLE_HELPER1.match(line)) for i, line in enumerate(self.data)
        )
        matches = [(i, m) for i, m in match_iter if m]
        for i, m in matches:
            g = m.groupdict()
            left, first, second = g["left"], g["first"], g["second"]
            self.data[
                i
            ] = "{}CatalogItemPermissionManager({}, {}, unittest_persistent_db).set_initial_owner_permissions()".format(
                left, first, second
            )
            self.modified = True

    def _modify2(self):
        match_iter = (
            (i, RE_ROLE_HELPER2.match(line)) for i, line in enumerate(self.data)
        )
        matches = [(i, m) for i, m in match_iter if m]
        for i, m in matches:
            g = m.groupdict()
            left, first, second = g["left"], g["first"], g["second"]
            self.data[
                i
            ] = "{}CatalogItemPermissionManager({}, {}, unittest_persistent_db).set_initial_can_read_info_only_permission()".format(
                left, first, second
            )
            self.modified = True


if __name__ == "__main__":
    main(RoleHelperInjector)
