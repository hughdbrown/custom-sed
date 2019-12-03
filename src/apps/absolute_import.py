#!/usr/bin/env python
from __future__ import absolute_import, print_function

from util import main
from sed_file import SedFile


class AbsoluteImportInjector(SedFile):
    """
    Derivative of SedFile dedicated to injecting
        from __future__ import absolute_import
    into python files.
    """

    prefix = "from __future__ import "
    injection = "from __future__ import absolute_import\n"

    def modify(self):
        self._modify_absolute()
        # self._modify_multiple()
        self._modify_pylint()

    def _modify_absolute(self):
        """
        Inject absolute import into file if not already present.
        Most of the logic is dedicated to findint the correct injection point
        """
        if any(self.data) and not any("absolute_import" in line for line in self.data):
            print(self.filename)
            try:
                i = 0
                if self.data[i].startswith(("#!/")):
                    # Skip execution header
                    i += 1

                if self.data[i].startswith("#") and "coding" in self.data[i]:
                    # Skip file encoding comment
                    i += 1

                comment_header = ("'''", '"""')
                if self.data[i].lstrip().startswith(comment_header):
                    # Skip any docstring
                    if len(self.data[i]) == 3 or not self.data[i].endswith(comment_header):
                        # If the comment does not start and end on this line ...
                        i += 1
                        try:
                            while not self.data[i].endswith(comment_header):
                                # print(i, self.data[i])
                                i += 1
                        except IndexError:
                            return None
                    assert self.data[i].endswith(comment_header)
                    i += 1

                for j, line in enumerate(self.data, start=i):
                    # Skip other comments
                    if not line.lstrip().startswith("#"):
                        break
                    i = j

                # This is the first line that a future import might be placed
                if self.data[i].startswith(self.prefix):
                    self.data[i] += ", absolute_import"
                else:
                    self.data = self.data[:i] + [self.injection] + self.data[i:]
                self.modified = True
            except IndexError:
                pass

    def _modify_multiple(self):
        """Flatten multiple (possibly non-conecutive) matches into a single line"""
        x = [i for i, line in enumerate(self.data) if line.startswith(self.prefix)]
        if len(x) > 1:
            # Join lines onto the first import-line, preserving order
            len_prefix = len(self.prefix)
            absolute_extracts = (self.data[j][len_prefix:] for j in x)
            self.data[x[0]] = self.prefix + ", ".join(absolute_extracts)

            # Discard lines that have been joined
            self.data = [
                line for j, line in enumerate(self.data) if j not in set(x[1:])
            ]
            self.modified = True

    def _modify_pylint(self):
        j = {i for i, line in enumerate(self.data) if line.startswith('# pylint: disable=no-absolute-import')}
        self.delete_lines(j)


if __name__ == "__main__":
    main(AbsoluteImportInjector)
