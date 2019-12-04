#!/usr/bin/env python
from __future__ import absolute_import

from src import SedFile, main as umain


class ImportInjector(SedFile):
    """
    Derivative of SedFile dedicated to injecting
        from common.utilities.fn_util import first
    into python files.
    """

    injection = "from common.iterutils import first_nodefault"

    def modify(self):
        """
        Inject import into file if not already present.
        Most of the logic is dedicated to finding the correct injection point
        """
        if (
            any(self.data)
            and any("first_nodefault(" in line for line in self.data)
            and not any(self.injection in line for line in self.data)
        ):
            # print(self.filename)
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
                    if len(self.data[i]) == 3 or not self.data[i].endswith(
                        comment_header
                    ):
                        # If the comment does not start and end on this line ...
                        i += 1
                        try:
                            while not self.data[i].endswith(comment_header):
                                # print(i, self.data[i])
                                i += 1
                        except IndexError:
                            return
                    assert self.data[i].endswith(comment_header)
                    i += 1

                last_import = None
                for j in reversed(range(i, len(self.data))):
                    if "import " in self.data[j]:
                        last_import = j
                        break
                else:
                    last_import = j

                for import_line in [
                    "common",
                    "ModelingMachine",
                    "config",
                    "from tests.",
                ]:
                    for inject_point in range(i, j + 1):
                        if import_line in self.data[inject_point]:
                            # This is the first line that a common import might be placed
                            self.data = (
                                self.data[:inject_point]
                                + [self.injection]
                                + self.data[inject_point:]
                            )
                            self.modified = True
                            return

            except IndexError:
                print("Could not find insertion point for {}".format(self.filename))


def main():
    umain(ImportInjector)


if __name__ == "__main__":
    main()
