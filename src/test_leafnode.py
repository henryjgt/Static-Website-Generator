#!/usr/bin/python3.12

"""Unit tests for the HTMLNode class."""

import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):

    def test_example_1(self):
        ln = LeafNode("p", "This is a paragraph of text.")
        example_1_out = "<p>This is a paragraph of text.</p>"
        self.assertEqual(ln.to_html(), example_1_out)

    def test_example_2(self):
        ln = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        example_2_out = "<a href='https://www.google.com'>Click me!</a>"
        self.assertEqual(ln.to_html(), example_2_out)

    def test_eq(self):
        ln1 = LeafNode("p")
        ln2 = LeafNode("p")
        self.assertEqual(repr(ln1), repr(ln2))

    def test_null(self):
        ln = LeafNode(None, None, None)
        self.assertEqual(ln.props_to_html(), None)


if __name__ == "__main__":
    unittest.main()
