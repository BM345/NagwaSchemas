import unittest
from parameterized import parameterized
from schemata import *


class TestParsing(unittest.TestCase):

    @parameterized.expand([
        ["/* This is a comment. */", 0,  "This is a comment."],
        [" This is a comment. */", 0, None],
        ["abc /* This is a comment. */", 0, None],
        ["abc /* This is a comment. */", 4, "This is a comment."],
    ])
    def test_parse_comment(self, inputText, p, n):
        parser = Parser()
        marker = Marker()
        marker.position = p

        self.assertEqual(parser._parseComment(inputText, marker), n)

    @parameterized.expand([
        ["/* This is a comment.", 0, "This is a comment."],
    ])
    def test_parse_comment_fail(self, inputText, p, n):
        parser = Parser()
        marker = Marker()
        marker.position = p

        with self.assertRaises(SchemataParsingError) as context:
            parser._parseComment(inputText, marker)

    @parameterized.expand([
        ["123", 0, 123],
        ["12345", 0, 12345],
        ["000123", 0, 123],
        ["000000123", 0, 123],
        ["123 a b c", 0, 123],
        ["+123", 0, None],
        ["-123", 0, None],
        [" 123", 0, None],
        [".123", 0, None],
        ["+123", 1, 123],
        ["-123", 1, 123],
        [" 123", 1, 123],
        [".123", 1, 123],
    ])
    def test_parse_integer(self, inputText, p, n):
        parser = Parser()
        marker = Marker()
        marker.position = p

        self.assertEqual(parser._parseInteger(inputText, marker), n)

    @parameterized.expand([
        ["ref1", 0, "ref1"],
        ["Ref1_a_b_c-d-e-f", 0, "Ref1_a_b_c-d-e-f"],
        ["ref1   ", 0, "ref1"],
        ["ref1 a b c", 0, "ref1"],
        ["ref1 123", 0, "ref1"],
        ["   ref1", 0, None],
        ["+ref1", 0, None],
        ["   ref1", 3, "ref1"],
        ["+ref1", 1, "ref1"],
    ])
    def test_parse_reference(self, inputText, p, n):
        parser = Parser()
        marker = Marker()
        marker.position = p

        self.assertEqual(parser._parseReference(inputText, marker), n)

    @parameterized.expand([
        ["button_text", 0, "button_text", 1, 1],
        ["button_text (optional)", 0, "button_text", 0, 1],
        ["button_text (n >= 0)", 0, "button_text", 0, -1],
        ["button_text (n >= 1)", 0, "button_text", 1, -1],
        ["button_text (n > 0)", 0, "button_text", 1, -1],
        ["button_text (n > 1)", 0, "button_text", 2, -1],
        ["button_text (n <= 3)", 0, "button_text", 0, 3],
        ["button_text (n <= 10)", 0, "button_text", 0, 10],
        ["button_text (n < 10)", 0, "button_text", 0, 9],
        ["button_text (0 <= n <= 5)", 0, "button_text", 0, 5],
        ["button_text (0 < n <= 5)", 0, "button_text", 1, 5],
        ["button_text (0 <= n < 5)", 0, "button_text", 0, 4],
        ["button_text (0 < n < 5)", 0, "button_text", 1, 4],
        ["button_text (1 <= n <= 5)", 0, "button_text", 1, 5],
        ["button_text (1 < n <= 5)", 0, "button_text", 2, 5],
        ["button_text (1 <= n < 5)", 0, "button_text", 1, 4],
        ["button_text (1 < n < 5)", 0, "button_text", 2, 4],
    ])
    def test_parse_element_usage_reference(self, inputText, p, elementReference, minimumNumberOfOccurrences, maximumNumberOfOccurrences):
        parser = Parser()
        marker = Marker()
        marker.position = p

        elementUsageReference = parser._parseElementUsageReference(inputText, marker)

        self.assertEqual(elementUsageReference.elementReference, elementReference)
        self.assertEqual(elementUsageReference.minimumNumberOfOccurrences, minimumNumberOfOccurrences)
        self.assertEqual(elementUsageReference.maximumNumberOfOccurrences, maximumNumberOfOccurrences)

    @parameterized.expand([
        ["button_text (optional abc)", 0],
        ["button_text (optional, abc)", 0],
        ["button_text (optional, n <= 1)", 0],
        ["button_text (n >= 0, optional)", 0],
        ["button_text (n >= 0 >= 2)", 0],
        ["button_text (n >= 0, n <= 5)", 0],
        ["button_text (n >= 0 abc)", 0],
        ["button_text (n == 3)", 0],
        ["button_text (0 < n < 5 < n)", 0],
        ["button_text (0 << n)", 0],
    ])
    def test_parse_element_usage_reference_fail(self, inputText, p):
        parser = Parser()
        marker = Marker()
        marker.position = p

        with self.assertRaises(SchemataParsingError) as context:
            parser._parseElementUsageReference(inputText, marker)

