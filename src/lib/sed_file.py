"""Main utility class for stream editor library"""
from __future__ import absolute_import


class SedFile(object):
    """Class that implements reading and saving files if there are changes"""

    def __init__(self, filename):
        self.filename = filename
        self.modified = 0
        with open(self.filename, "r") as handle:
            self.data = [line.rstrip() for line in handle]

    def __enter__(self):
        """with-stmt interface method"""
        return self

    def __exit__(self, _type, _value, _tb):
        """with-stmt interface method"""
        if self.modified:
            with open(self.filename, "w") as handle:
                handle.write("\n".join(self.data) + "\n")

    def modify(self):
        """Abstract method for derived class to apply changes to file"""
        raise NotImplementedError

    def next_match(self, match, start=None):
        start = start if start is not None else 0
        line_iter = ((i, self.data[i])) for line_no in range(start, -1))
        return next((i for i, line in line_iter if match in line), None)

    def prev_match(self, match, end=None):
        end = end if end is not None else len(self.data)
        line_iter = ((i, self.data[i])) for line_no in reversed(range(0, end))
        return next((i for i, line in line_iter if match in line), None)

    def sort(self, start=None, end=None, key=str):
        start = start if start is not None else 0
        end = end if end is not None else len(self.data)
        self.data[start:end] = sorted(self.data[start:end], key=key)
        self.modified += len(self.data)
