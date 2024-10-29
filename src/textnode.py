#!/usr/bin/python3.12

"""Implements the TextNode class."""

from typing import Iterator, Optional


class TextNode:
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
