import unittest
from parameterized import parameterized
from schemata import *


class TestParsing(unittest.TestCase):

    @parameterized.expand([
        ["123", 123],
        ["12345", 12345],
        ["000123", 123],
        ["000000123", 123],
        ["123 a b c", 123],
        ["+123", None],
        ["-123", None],
        [" 123", None],
        [".123", None],
    ])
    def test_parse_integer(self, inputText, n):
        parser = Parser()
        marker = Marker()

        self.assertEqual(parser._parseInteger(inputText, marker), n)

    @parameterized.expand([
        ["ref1", "ref1"],
        ["Ref1_a_b_c-d-e-f", "Ref1_a_b_c-d-e-f"],
        ["ref1   ", "ref1"],
        ["ref1 a b c", "ref1"],
        ["ref1 123", "ref1"],
        ["   ref1", None],
        ["+ref1", None],
    ])
    def test_parse_reference(self, inputText, n):
        parser = Parser()
        marker = Marker()

        self.assertEqual(parser._parseReference(inputText, marker), n)
