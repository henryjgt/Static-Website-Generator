#!/usr/bin/python3.12

"""Functionality to parse raw markdown into a sequence of TextNode objects."""


from textnode import TextNode, TextType


type NodeList = list[TextNode]


def split_nodes_delimiter(
    old_nodes: NodeList, delimiter: str, text_type: TextType
) -> NodeList:

    inlined_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            inlined_nodes.append(node)
            continue

        split_nodes: list[TextNode] = []
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


if __name__ == "__main__":

    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes: NodeList = split_nodes_delimiter([node], "`", TextType.CODE)
    print(new_nodes)
