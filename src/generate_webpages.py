#!/usr/bin/python3.12

"""Functionality to generate static webpage(s) from resource files."""


import os
import pathlib
import re
from typing import TypeVar

from htmlnode import ParentNode
from markdown_to_html import markdown_to_html_node


type Path = os.PathLike | pathlib.Path
ErrType = TypeVar("ErrType", bound=Exception)


def extract_title(markdown: str) -> str:
    lines: list[str] = markdown.split("\n")
    for line in lines:
        h1_heading: re.Match[str] | None = re.match(r"# (?P<heading>.+)", line)
        if h1_heading:
            extracted_title: str = h1_heading["heading"].strip()
            return extracted_title

    raise Exception("Invalid markdown: no h1 header found")


def generate_page(from_path, template_path, dest_path) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f, open(template_path) as t:
        markdown_content: str = f.read()
        template_html: str = t.read()

    page_title: str = extract_title(markdown_content)
    html_nodes: ParentNode = markdown_to_html_node(markdown_content)
    html_content: str = html_nodes.to_html()

    template_html: str = template_html.replace("{{ Title }}", page_title)
    template_html: str = template_html.replace("{{ Content }}", html_content)

    p: Path = pathlib.Path(dest_path).resolve()
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(str(p), "w") as f:
        f.write(template_html)

    return


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path): ...
