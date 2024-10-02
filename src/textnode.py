#!/usr/bin/python3.12

"""Implements the TextNode class."""

from typing import Optional


class TextNode:
    def __init__(self, text: str, text_type: str, url: Optional[str] = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return vars(self) == vars(other)

    def __repr__(self):
        _name = type(self).__name__
        _args = (f"{v!r}" for v in vars(self).values())
        return f"{_name}({', '.join((_args))})"
