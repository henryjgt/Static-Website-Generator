#!/usr/bin/python3.12

"""Implements the HTMLNode class."""

from typing import Any, Iterator, Optional


type Node = HTMLNode
type Error = Any


class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[list[Node]] = None,
        props: Optional[dict[str, str]] = None,
    ) -> None:
        self.tag: Optional[str] = tag
        self.value: Optional[str] = value
        self.children: Optional[list[Node]] = children
        self.props: Optional[dict[str, str]] = props

    def __repr__(self) -> str:
        _name: str = type(self).__name__
        _args: Iterator[str] = (f"{v!r}" for v in vars(self).values())
        return f"{_name}({', '.join((_args))})"

    def to_html(self) -> Error:
        raise NotImplementedError

    def props_to_html(self) -> Optional[str]:
        if not self.props:
            return None

        attrs: Iterator[str] = (f"{k}={v!r}" for k, v in self.props.items())
        return " ".join(("", *attrs))


class LeafNode(HTMLNode):

    err_missing_value: str = "LeafNode object must have `value` of type str"

    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        props: Optional[dict[str, str]] = None,
    ) -> None:
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self) -> str | Error:
        if self.value is None:
            raise ValueError(self.err_missing_value)

        if not self.tag:
            return str(self.value)

        props: str = self.props_to_html() or ""
        rendered_html: str = f"<{self.tag}{props}>{self.value}</{self.tag}>"
        return rendered_html


class ParentNode(HTMLNode):

    err_missing_tag: str = "ParentNode object must have `tag` of type str"
    err_missing_children: str = "ParentNode object must have child node(s)"

    def __init__(
        self,
        tag: Optional[str] = None,
        children: Optional[list[Node]] = None,
        props: Optional[dict[str, str]] = None,
    ) -> None:
        if self.tag is None:
            raise ValueError(self.err_missing_tag)

        if self.children is None:
            raise ValueError(self.err_missing_children)

        super().__init__(tag=tag, value=None, children=children, props=props)

    # validate arguments decorator
    def to_html(self) -> str | Error:
        assert self.children

        parent_props: str = self.props_to_html() or ""
        for child in self.children:
            if isinstance(child, LeafNode):
                self.to_html()

        return str()


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
