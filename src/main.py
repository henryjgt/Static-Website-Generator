#!/usr/bin/python3.12

"""Generates a static html website from markdown."""


from textnode import TextNode


def main():
    args = ("This is a text node", "bold", "https://www.boot.dev")
    tn = TextNode(*args)
    print(tn)


def text_node_to_html_node(text_node): ...


if __name__ == "__main__":
    main()
