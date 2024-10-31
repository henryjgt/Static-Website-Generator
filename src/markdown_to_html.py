#!/usr/bin/python3.12

"""Functionality to convert markdown to HTML."""


from enum import StrEnum, unique

from htmlnode import Node, LeafNode, ParentNode
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


def markdown_to_html_node(markdown: str) -> None:
    blocks: list[str] = markdown_to_blocks(markdown)
    for block in blocks:
        block_type: str = block_to_block_type(block)
        block_to_html_node(block, block_type)


def block_to_html_node(block: str, block_type: str) -> ParentNode:
    # if block has text, block node will be a parent node
    # can block not have text? Img?

    if block_type == BlockType.QUOTE.value:
        return quote_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST.value:
        return unordered_list_to_html_node(block)

    return paragraph_to_html_node(block)


def text_to_html_nodes(text) -> list[LeafNode]:
    tns: list[TextNode] = text_to_textnodes(text)
    hns: list[LeafNode] = [text_node_to_html_node(tn) for tn in tns]

    return hns


def paragraph_to_html_node(block: str) -> ParentNode:
    tag: str = BlockTag.PARAGRAPH.value
    children: list[LeafNode] = text_to_html_nodes(block)

    return ParentNode(tag=tag, children=children)


def quote_to_html_node(block: str) -> ParentNode:
    tag: str = BlockTag.QUOTE.value

    formatted_block: str = ""
    for line in block.split("\n"):
        if len(line) > 0:
            formatted_block += line.lstrip("* ").strip() + " "
    children: list[LeafNode] = text_to_html_nodes(formatted_block)

    return ParentNode(tag=tag, children=children)


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
            msg = "Invalid markdown: ulist entries must start with '* ' or '- '"
            raise ValueError(msg)

        line_children: list[LeafNode] = text_to_html_nodes(fmt_line)
        list_subnodes.append(ParentNode(tag=subtag, children=line_children))

    return ParentNode(tag=tag, children=list_subnodes)


def ordered_list_to_html_node(block: str):
    tag: str = BlockTag.ORDERED_LIST.value
    subtag: str = BlockTag.LIST.value

    list_subnodes: list[ParentNode] = []
