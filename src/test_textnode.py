#!/usr/bin/python3.12

"""Unit tests for the TextNode class."""

import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        node2 = TextNode("This might be a text node", "bold", "https://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_url_none(self):
        node = TextNode("Text node", "bold", None)
        self.assertEqual(node.url, None)

    def test_test_type(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertEqual(node.text_type, "bold")
        self.assertEqual(node2.text_type, "italic")


if __name__ == "__main__":
    unittest.main()
