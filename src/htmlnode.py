#!/usr/bin/python3.12

"""Implements the HTMLNode class."""

from typing import Optional


type Node = HTMLNode


class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[list[Node]] = None,
        props: Optional[dict[str, str]] = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        _name = type(self).__name__
        _args = (f"{v!r}" for v in vars(self).values())
        return f"{_name}({', '.join((_args))})"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return None

        attrs = (f"{k}={v!r}" for k, v in self.props.items())
        return " ".join(("", *attrs))


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        props: Optional[dict[str, str]] = None,
    ):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("`value` argument must have a value")

        if not self.tag:
            return str(self.value)

        props = self.props_to_html() or ""
        rendered_html = f"<{self.tag}{props}>{self.value}</{self.tag}>"
        return rendered_html


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: Optional[str] = None,
        children: Optional[list[Node]] = None,
        props: Optional[dict[str, str]] = None,
    ):
        if self.tag is None:
            raise ValueError("`tag` argument must have a value")

        if self.children is None:
            raise ValueError("`children` argument must have a value")

        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        assert self.children

        parent_props = self.props_to_html() or ""
        for child in self.children:
            if isinstance(child, LeafNode):
                self.to_html()


if __name__ == "__main__":

    vals = {
        "tag": "<h1>",
        "props": {"href": "https://www.google.com", "target": "_blank"},
    }
    hn = HTMLNode(**vals)
    print(hn)
    print(hn.props_to_html())

    # vals = {
    #     "tag": "<h1>",
    #     "value": "This is fun.",
    #     "children": [hn],
    #     "props": {"href": "https://www.google.com", "target": "_blank"},
    # }
    # hn = HTMLNode(**vals)
    # print(hn)
    # print(hn.props_to_html())

    # hn = HTMLNode(None, None, None, None)
    # print(hn)
    # print(hn.props_to_html())

    # ln = LeafNode(None, None, None)
    # print(ln)

    ln = LeafNode("p", "This is a paragraph of text.")
    print(ln.to_html())
