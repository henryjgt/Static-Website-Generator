#!/usr/bin/python3.12

"""Functionality to parse raw markdown into a sequence of TextNode objects."""

from enum import Enum
import re
from typing import Pattern

from textnode import TextNode, TextType


type NodeList = list[TextNode]


class Patterns(Enum):

    # IMAGES
    # This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)

    # LINKS
    # This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)

    IMAGE = r"!\[(?P<alt>.+?)\]\((?P<src>.+?)\)"
    LINK = r"\[(?P<anchor>.*?)\]\((?P<src>.+?)\)"


match_image: Pattern = re.compile(Patterns.IMAGE.value)
match_link: Pattern = re.compile(Patterns.LINK.value)


def extract_markdown_images(text) -> list[tuple[str, str]]:
    images: list[tuple[str, str]] = []
    for match in re.finditer(match_image, text):
        image_alt_url: tuple = (match.group("alt"), match.group("src"))
        images.append(image_alt_url)

    return images


def extract_markdown_links(text) -> list[tuple[str, str]]:
    links: list[tuple[str, str]] = []
    for match in re.finditer(match_link, text):
        link_anchor_url: tuple = (match.group("anchor"), match.group("src"))
        links.append(link_anchor_url)

    return links


def split_nodes_delimiter(
    old_nodes: NodeList, delimiter: str, text_type: TextType
) -> NodeList:

    inlined_nodes: NodeList = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            inlined_nodes.append(node)
            continue

        split_nodes: NodeList = []
        substrings: list[str] = node.text.split(delimiter)
        if len(substrings) % 2 == 0:
            raise ValueError("Invalid markdown: missing formatting element")
        for i, ss in enumerate(substrings):
            if substrings[i] == "":
                continue

            if i % 2 == 1:
                split_nodes.append(TextNode(ss, text_type))
            else:
                split_nodes.append(TextNode(ss, TextType.TEXT))

        inlined_nodes.extend(split_nodes)

    return inlined_nodes


def split_nodes_image(old_nodes: NodeList) -> NodeList:

    inlined_nodes: NodeList = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            inlined_nodes.append(node)
            continue

        node_text: str = node.text
        next_start: int = 0
        split_nodes: NodeList = []
        for m in re.finditer(match_image, node_text):
            if m.start() != next_start:
                text_node = TextNode(node_text[next_start : m.start()], TextType.TEXT)
                split_nodes.append(text_node)

            image_node = TextNode(m.group("alt"), TextType.IMAGE, m.group("src"))
            split_nodes.append(image_node)

            next_start: int = m.end()

        if next_start < len(node_text):
            split_nodes.append(TextNode(node_text[next_start:], TextType.TEXT))

        inlined_nodes.extend(split_nodes)

    return inlined_nodes


def split_nodes_link(old_nodes: NodeList) -> NodeList:

    inlined_nodes: NodeList = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            inlined_nodes.append(node)
            continue

        node_text: str = node.text
        next_start: int = 0
        split_nodes: NodeList = []
        for m in re.finditer(match_link, node_text):
            if m.start() != next_start:
                text_node = TextNode(node_text[next_start : m.start()], TextType.TEXT)
                split_nodes.append(text_node)

            image_node = TextNode(m.group("anchor"), TextType.LINK, m.group("src"))
            split_nodes.append(image_node)

            next_start: int = m.end()

        if next_start < len(node_text):
            split_nodes.append(TextNode(node_text[next_start:], TextType.TEXT))

        inlined_nodes.extend(split_nodes)

    return inlined_nodes


if __name__ == "__main__":

    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes: NodeList = split_nodes_delimiter([node], "`", TextType.CODE)
    # print(new_nodes)
    # print()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)! Isn't that cool?",
        TextType.TEXT,
    )
    new_nodes: NodeList = split_nodes_link([node])
    # print(new_nodes)
    # print()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # node = TextNode(
    #     "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)! Isn't that cool?",
    #     TextType.TEXT,
    # )
    node = TextNode(
        "![image](https://www.example.COM/IMAGE.PNG)",
        TextType.TEXT,
    )
    new_nodes: NodeList = split_nodes_image([node])
    # print(new_nodes)
    # print()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
