#!/usr/bin/python3.12

"""Implements the TextNode class."""

from enum import StrEnum, unique
from typing import Callable, Iterator, NoReturn, Optional

from htmlnode import LeafNode


@unique
class TextType(StrEnum):
    TEXT = "TEXT"
    BOLD = "BOLD"
    ITALIC = "ITALIC"
    CODE = "CODE"
    LINK = "LINK"
    IMAGE = "IMAGE"


def tt_validation(f) -> Callable:
    def wrapper(*args) -> Callable | NoReturn:
        TextType(args[2])
        return f(*args)

    return wrapper


class TextNode:

    @tt_validation
    def __init__(self, text: str, text_type: str, url: Optional[str] = None) -> None:
        self.text: str = text
        self.text_type: str = text_type
        self.url: Optional[str] = url

    def __eq__(self, other) -> bool:
        return vars(self) == vars(other)

    def __repr__(self) -> str:
        _name: str = type(self).__name__
        _args: Iterator[str] = (f"{v!r}" for v in vars(self).values())
        return f"{_name}({', '.join((_args))})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode | NoReturn:
    """Transforms TextNode obj to LeafNode obj."""

    match text_node.text_type:
        case "TEXT":
            return LeafNode(value=text_node.text)
        case "BOLD":
            return LeafNode(tag="b", value=text_node.text)
        case "ITALIC":
            return LeafNode(tag="i", value=text_node.text)
        case "CODE":
            return LeafNode(tag="code", value=text_node.text)
        case "LINK":
            a_props: dict[str, Optional[str]] = {"href": text_node.url}
            return LeafNode(tag="a", value=text_node.text, props=a_props)
        case "IMAGE":
            img_props: dict[str, Optional[str]] = {
                "src": text_node.url,
                "alt": text_node.text,
            }
            return LeafNode(tag="img", value=None, props=img_props)
        case _:
            raise ValueError("Text is not a valid text type")
