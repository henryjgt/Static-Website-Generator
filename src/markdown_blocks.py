#!/usr/bin/python3.12

"""Functionality to parse markdown blocks."""

from enum import StrEnum, unique
import re


@unique
class BlockType(StrEnum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks: list[str] = markdown.split("\n\n")
    blocks = [b.strip() for b in blocks if b]
    return blocks


def block_to_block_type(block: str) -> str:

    if re.match(r"^#{1,6} \S+", block):
        return BlockType.HEADING.value
    if re.match(r"^```[\s\S]*?```$", block):
        return BlockType.CODE.value
    if all(re.match(r"^>", line) for line in block.split("\n")):
        return BlockType.QUOTE.value
    if all(re.match(r"[*|-] ", line) for line in block.split("\n")):
        return BlockType.UNORDERED_LIST.value
    if all(line.startswith(f"{n}. ") for n, line in enumerate(block.split("\n"), 1)):
        return BlockType.ORDERED_LIST.value

    return BlockType.PARAGRAPH.value


if __name__ == "__main__":
    from pprint import pprint

    md = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
    # pprint(markdown_to_blocks(md))
    # print()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # print(block_to_block_type())
    # print(block_to_block_type("# heading"))
    # print(block_to_block_type("```\ncode\n```"))
    # print()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
