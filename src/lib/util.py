"""Utility methods for stream editor library"""
from __future__ import absolute_import, print_function

from datetime import datetime
import os
import os.path
import sys


def path_iter(folder=".", exts=(".py",)):
    """
    Generator for files in tree that match any exts
    """
    for root, _, files in os.walk(folder):
        for filename in files:
            fullpath = os.path.join(os.path.normpath(root), filename)
            if os.path.splitext(fullpath)[1] in exts:
                yield fullpath


def main(cls):
    """
    Traverse down tree, looking for files to modify. Save modified files
    """
    modified = 0
    start = datetime.now()
    files = sys.argv[1:] or path_iter()
    for count, fullpath in enumerate(files):
        with cls(fullpath) as obj:
            obj.modify()
            modified += int(bool(obj.modified))
    end = datetime.now()
    elapsed = end - start
    print("{}/{} processed in {}".format(modified, count, elapsed))
