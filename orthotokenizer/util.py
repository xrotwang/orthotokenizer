from __future__ import print_function
import codecs
import unicodedata


def normalized_lines(path):
    for i, line in enumerate(codecs.open(path, 'r', 'utf8')):
        yield i, unicodedata.normalize('NFD', line.strip())

