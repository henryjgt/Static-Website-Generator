#!/usr/bin/python3.12

"""Functionality to convert markdown to HTML."""


from enum import StrEnum, unique
import re

from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from markdown_blocks import BlockType, markdown_to_blocks, block_to_block_type
from textnode import TextNode, text_node_to_html_node


@unique
class BlockTag(StrEnum):
    PARAGRAPH = "p"
    HEADING = "h"
    PREFORMATTED = "pre"
    CODE = "code"
    QUOTE = "blockquote"
    LIST = "li"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"


def markdown_to_html_node(markdown: str) -> ParentNode:
    children: list[ParentNode] = []
    blocks: list[str] = markdown_to_blocks(markdown)
    for block in blocks:
        html_nodes: ParentNode = block_to_html_node(block)
        children.append(html_nodes)

    return ParentNode(tag="div", children=children)


def block_to_html_node(block: str) -> ParentNode:
    # if block has text, block node will be a parent node
    # can block not have text? Img?

    block_type: str = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH.value:
        return paragraph_to_html_node(block)
    if block_type == BlockType.QUOTE.value:
        return quote_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST.value:
        return unordered_list_to_html_node(block)
    if block_type == BlockType.HEADING.value:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE.value:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST.value:
        return ordered_list_to_html_node(block)
    raise ValueError("Invalid block type")


def text_to_html_nodes(text) -> list[LeafNode]:
    text_nodes: list[TextNode] = text_to_textnodes(text)
    html_nodes: list[LeafNode] = [text_node_to_html_node(tn) for tn in text_nodes]
    return html_nodes


def paragraph_to_html_node(block: str) -> ParentNode:
    tag: str = BlockTag.PARAGRAPH.value

    lines: list[str] = block.split("\n")
    paragraph: str = " ".join(lines)
    children: list[LeafNode] = text_to_html_nodes(paragraph)

    return ParentNode(tag=tag, children=children)


def quote_to_html_node(block: str) -> ParentNode:
    tag: str = BlockTag.QUOTE.value

    formatted_lines: list[str] = []
    for line in block.split("\n"):
        if not line.startswith(">"):
            raise ValueError("Invalid markdown: invalid quote block")
        if len(line) > 0:
            formatted_lines.append(line.lstrip("> ").strip())

    formatted_block: str = " ".join(formatted_lines)
    children: list[LeafNode] = text_to_html_nodes(formatted_block)

    return ParentNode(tag=tag, children=children)


def heading_to_html_node(block: str) -> ParentNode:
    basetag: str = BlockTag.HEADING.value
    m: re.Match[str] | None = re.match(r"^#{1,6}", block)
    if not m:
        raise ValueError("Invalid markdown: header cannot be coerced to HTML")
    tag: str = f"{basetag}{m.end()}"

    header_text: str = block.lstrip("#").strip()
    children: list[LeafNode] = text_to_html_nodes(header_text)

    return ParentNode(tag=tag, children=children)


def code_to_html_node(block: str) -> ParentNode:
    tag: str = BlockTag.PREFORMATTED.value
    subtag: str = BlockTag.CODE.value

    m: re.Match[str] | None = re.match(r"^```(?P<code>[\s\S]*?)```$", block)
    if not m:
        raise ValueError("Valid code could not be extracted from codeblock")

    extracted_code: str = m.group("code")
    children: list[LeafNode] = text_to_html_nodes(extracted_code)
    subnodes = ParentNode(tag=subtag, children=children)

    return ParentNode(tag=tag, children=[subnodes])


def unordered_list_to_html_node(block: str) -> ParentNode:
    tag: str = BlockTag.UNORDERED_LIST.value
    subtag: str = BlockTag.LIST.value

    list_subnodes: list[ParentNode] = []
    for line in block.split("\n"):
        if line.startswith("* "):
            fmt_line: str = line.lstrip("* ").strip()
        elif line.startswith("- "):
            fmt_line: str = line.lstrip("- ").strip()
        else:
            msg = "Invalid markdown: list elements could not be coerced"
            raise ValueError(msg)

        line_children: list[LeafNode] = text_to_html_nodes(fmt_line)
        list_subnodes.append(ParentNode(tag=subtag, children=line_children))

    return ParentNode(tag=tag, children=list_subnodes)


def ordered_list_to_html_node(block: str) -> ParentNode:
    tag: str = BlockTag.ORDERED_LIST.value
    subtag: str = BlockTag.LIST.value

    list_subnodes: list[ParentNode] = []
    for line in block.split("\n"):
        fmt_line: str = re.sub(r"^\d\. ", "", line).strip()
        line_children: list[LeafNode] = text_to_html_nodes(fmt_line)
        list_subnodes.append(ParentNode(tag=subtag, children=line_children))

    return ParentNode(tag=tag, children=list_subnodes)


if __name__ == "__main__":
    from pprint import pprint

    markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""

    html: ParentNode = markdown_to_html_node(markdown)
    pprint(html)
