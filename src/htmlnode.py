#!/usr/bin/python3.12

"""Implements the HTMLNode class."""

from typing import Iterator, NoReturn, Optional


type Node = HTMLNode


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

    def to_html(self) -> str | NoReturn:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if not self.props:
            return ""
        attrs: Iterator[str] = (f"{k}={v!r}" for k, v in self.props.items())
        return "" or " ".join(("", *attrs))


class LeafNode(HTMLNode):

    err_missing_value: str = "LeafNode object cannot have missing `value`"

    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        props: Optional[dict[str, str]] = None,
    ) -> None:
        if value is None:
            value = ""
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self) -> str | NoReturn:
        if self.value is None:
            raise ValueError(self.err_missing_value)
        if self.tag is None:
            return str(self.value)

        _props: str = self.props_to_html()
        return f"<{self.tag}{_props}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):

    err_missing_tag: str = "ParentNode object cannot have missing `tag`"
    err_missing_children: str = "ParentNode object must have child node(s)"

    def __init__(
        self,
        tag: Optional[str] = None,
        children: Optional[list[Node]] = None,
        props: Optional[dict[str, str]] = None,
    ) -> None:
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self) -> str | NoReturn:
        if self.tag is None:
            raise ValueError(self.err_missing_tag)
        if self.children is None:
            raise ValueError(self.err_missing_children)

        _html: str = ""
        for child in self.children:
            _html += child.to_html()

        _props: str = self.props_to_html()
        return f"<{self.tag}{_props}>{_html}</{self.tag}>"
