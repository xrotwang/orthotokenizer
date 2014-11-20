# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import unittest
from orthotokenizer.tokenizer import Tokenizer


class TokenizerTestCase(unittest.TestCase):
    """ Tests for tokenizer.py """

    def setUp(self):
        self.t = Tokenizer(os.path.join(os.path.dirname(__file__), 'test.prf'))

    def test_printTree(self):
        self.t.tree.printTree(self.t.tree.root)

    def test_characters(self):
        t = Tokenizer()
        result = t.characters("Màttís List")
        self.assertEqual(result, "M a ̀ t t i ́ s # L i s t")

        result = self.t.characters("Màttís List")
        self.assertEqual(result, "M a ̀ t t i ́ s # L i s t")

    def test_graphemes(self):
        t = Tokenizer()
        result = t.graphemes("Màttís List")
        self.assertEqual(result, "M à t t í s # L i s t")

        result = self.t.graphemes("Màttís List")
        self.assertEqual(result, "M à tt í s # ? ? s ?")

    def test_grapheme_clusters(self):
        result = self.t.grapheme_clusters("Màttís List")
        self.assertEqual(result, "M à t t í s # L i s t")
        
    def test_transform1(self):
        result = self.t.transform("Màttís List")
        self.assertEqual(result, "M à tt í s # ? ? s ?")

    def test_transform2(self):
        result = self.t.transform("Màttís List", 'ipa')
        self.assertEqual(result, "m a tː i s # ? ? s ?")

    def test_transform3(self):
        result = self.t.transform("Màttís List", 'funny')
        self.assertEqual(result, "J e l n a # ? ? a ?")

    def test_rules(self):
        result = self.t.rules("Màttís List")
        self.assertEqual(result, "Jelena")

    def test_transform_rules(self):
        result = self.t.transform_rules("Màttís List")
        self.assertEqual(result, "M à e l ?")

    def test_find_missing_characters(self):
        result = self.t.find_missing_characters("L i s t")
        self.assertEqual(result, "? ? s ?")
