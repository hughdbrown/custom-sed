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
