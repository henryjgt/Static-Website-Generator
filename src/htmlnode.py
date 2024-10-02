#!/usr/bin/python3.12

"""Implements the HTMLNode class."""

from typing import Optional


class HTMLNode:

    type Self = HTMLNode

    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[list[Self]] = None,
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


if __name__ == "__main__":

    vals = {
        "tag": "<h1>",
        "props": {"href": "https://www.google.com", "target": "_blank"},
    }
    hn = HTMLNode(**vals)
    print(hn)
    print(hn.props_to_html())

    vals = {
        "tag": "<h1>",
        "value": "This is fun.",
        "children": [hn],
        "props": {"href": "https://www.google.com", "target": "_blank"},
    }
    hn2 = HTMLNode(**vals)
    print(hn2)
    print(hn2.props_to_html())
