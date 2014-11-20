from __future__ import unicode_literals, print_function

from orthotokenizer.util import normalized_lines


class TreeNode(object):
    """
    Private class that creates the trie data structure from the orthography profile for parsing.
    """

    def __init__(self, char):
        self.char = char
        self.children = {}
        self.sentinel = False

    def isSentinel(self):
        return self.sentinel

    def getChar(self):
        return self.char

    def makeSentinel(self):
        self.sentinel = True

    def addChild(self, char):
        child = self.getChild(char)
        if not child:
            child = TreeNode(char)
            self.children[char] = child
        return child

    def getChild(self, char):
        if char in self.children:
            return self.children[char]
        else:
            return None

    def getChildren(self):
        return self.children


class Tree(object):
    def __init__(self, filename):
        # Internal function to add a multigraph starting at node.
        def addMultigraph(node, line):
            for char in line:
                node = node.addChild(char)
            node.makeSentinel()

        # Add all multigraphs in each line of file_name.
        # Skip "#" comments and blank lines.
        self.root = TreeNode('')
        self.root.makeSentinel()

        header = []

        for i, line in normalized_lines(filename):
            if i == 0 and line.lower().startswith("graphemes"):
                # deal with the columns header -- should always start with "graphemes" as
                # per the orthography profiles specification
                header = line.split("\t")
                continue

            # skip any comments
            if line.startswith("#") or line == "":
                continue

            tokens = line.split("\t")  # split the orthography profile into columns
            grapheme = tokens[0]
            addMultigraph(self.root, grapheme)

    def parse(self, line):
        parse = self._parse(self.root, line)
        return "# " + parse if parse else ""

    def _parse(self, root, line):
        # Base (or degenerate..) case.
        if len(line) == 0:
            return "#"

        parse = ""
        curr = 0
        node = root
        while curr < len(line):
            node = node.getChild(line[curr])
            curr += 1
            if not node:
                break
            if node.isSentinel():
                subparse = self._parse(root, line[curr:])
                if len(subparse) > 0:
                    # Always keep the latest valid parse, which will be
                    # the longest-matched (greedy match) graphemes.
                    parse = line[:curr] + " " + subparse

        # Note that if we've reached EOL, but not end of valid grapheme,
        # this will be an empty string.
        return parse

    def printTree(self, root, path=''):
        for char, child in root.getChildren().items():
            if child.isSentinel():
                char += "*"
            branch = (" -- " if len(path) > 0 else "")
            self.printTree(child, path + branch + char)
        if len(root.getChildren()) == 0:
            print(path)


def printMultigraphs(root, line, result):
    # Base (or degenerate..) case.
    if len(line) == 0:
        result += "#"
        return result

    # Walk until we run out of either nodes or characters.
    curr = 0   # Current index in line.
    last = 0   # Index of last character of last-seen multigraph.
    node = root
    while curr < len(line):
        node = node.getChild(line[curr])
        if not node:
            break
        if node.isSentinel():
            last = curr
        curr += 1

    # Print everything up to the last-seen sentinel, and process
    # the rest of the line, while there is any remaining.
    last = last + 1  # End of span (noninclusive).
    result += line[:last]+" "
    return printMultigraphs(root, line[last:], result)
