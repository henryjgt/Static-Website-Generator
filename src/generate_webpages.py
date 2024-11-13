#!/usr/bin/python3.12

"""Functionality to generate static webpage(s) from resource files."""


import re
from typing import Any, TypeVar


ErrType = TypeVar("ErrType", bound=Exception)


def extract_title(markdown: str) -> str | Exception:
    lines: list[str] = markdown.split("\n")
    for line in lines:
        h1_heading: re.Match[str] | None = re.match(r"# (?P<heading>.+)", line)
        if h1_heading:
            extracted_title: str = h1_heading["heading"].strip()
            return extracted_title

    raise Exception("Invalid markdown: no h1 header found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")


if __name__ == "__main__":
    from pprint import pprint

    md = """
# this is the h1 heading

everything else is plain text!

"""

    title = extract_title(md)
    print(title)
