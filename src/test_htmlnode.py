#!/usr/bin/python3.12

"""Unit tests for the HTMLNode class."""

import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
        self.assertEqual(hn.props_to_html(), "")

    def test_leafnode_1(self):
        ln = LeafNode("p", "This is a paragraph of text.")
        example_1_out = "<p>This is a paragraph of text.</p>"
        self.assertEqual(ln.to_html(), example_1_out)

    def test_leafnode_2(self):
        ln = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        example_2_out = "<a href='https://www.google.com'>Click me!</a>"
        self.assertEqual(ln.to_html(), example_2_out)

    def test_leafnode_eq(self):
        ln1 = LeafNode("p")
        ln2 = LeafNode("p")
        self.assertEqual(repr(ln1), repr(ln2))

    def test_leafnode_null(self):
        ln = LeafNode(None, None, None)
        self.assertEqual(ln.props_to_html(), "")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


if __name__ == "__main__":
    unittest.main()
