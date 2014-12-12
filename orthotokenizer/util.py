from __future__ import print_function
import codecs
import unicodedata


def normalized_lines(path, skip_comments=True):
    for i, line in enumerate(codecs.open(path, 'r', 'utf8')):
        line = unicodedata.normalize('NFD', line.strip())
        if line and (not skip_comments or not line.startswith('#')):
            yield i, line


def normalized_string(string, add_boundaries=True):
    if add_boundaries:
        string = string.replace(" ", "#")
    return unicodedata.normalize("NFD", string)
