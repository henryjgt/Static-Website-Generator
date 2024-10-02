#!/usr/bin/python3.12

"""Generates a static html website from markdown."""

from textnode import TextNode


def main():
    args = ("This is a text node", "bold", "https://www.boot.dev")
    tn = TextNode(*args)
    print(tn)


if __name__ == "__main__":

    print("hello world")
    main()
