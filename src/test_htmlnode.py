#!/usr/bin/python3.12

"""Unit tests for the HTMLNode class."""

import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    example_in = {
        "tag": "<h1>",
        "props": {"href": "https://www.google.com", "target": "_blank"},
    }
    example_out = " href='https://www.google.com' target='_blank'"

    def test_sample_behaviour(self):
        hn = HTMLNode(**self.example_in)
        self.assertEqual(hn.props_to_html(), self.example_out)

    def test_eq(self):
        hn1 = HTMLNode(**self.example_in)
        hn2 = HTMLNode(**self.example_in)
        self.assertEqual(repr(hn1), repr(hn2))

    def test_null(self):
        hn = HTMLNode(None, None, None, None)
        self.assertEqual(hn.props_to_html(), None)


if __name__ == "__main__":
    unittest.main()
