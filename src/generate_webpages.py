#!/usr/bin/python3.12

"""Functionality to generate static webpage(s) from resource files."""


from collections import defaultdict
import os
import pathlib
import re
import shutil
import sys
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


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path) -> None:
    content_list: list[str] = list_directory(dir_path_content)
    to_replicate: dict[str, list[tuple[str, str]]] = paths_to_create(
        dir_path_content, dest_dir_path, content_list
    )

    dirs_to_create: list[tuple[str, str]] | None = to_replicate.get("dirs")
    if dirs_to_create:
        for d in dirs_to_create:
            new_dir: str = d[1]
            make_dir(new_dir)  # TODO log the newly created directories

    files_to_copy: list[tuple[str, str]] | None = to_replicate.get("files")
    if files_to_copy:
        for file in files_to_copy:
            file_source: str = file[0]

            if not file_source.endswith(".md"):
                continue

            file_dest: str = file[1][:-2] + "html"

            # TODO log the newly created directories
            generate_page(file_source, template_path, file_dest)


def list_directory(directory: str, filepaths: list[str] = []) -> list[str]:
    # TODO needs to go in tertiary file

    target_dir: str = str(pathlib.Path(directory).resolve())
    for node in os.listdir(target_dir):
        node: str
        nodepath: str = os.path.join(target_dir, node)
        if is_file(node):
            filepaths.append(nodepath)
        else:
            filepaths.append(nodepath + "/")
            list_directory(nodepath, filepaths)

    return filepaths


def paths_to_create(
    source: str, destination: str, source_tree: list[str]
) -> dict[str, list[tuple[str, str]]]:
    # TODO needs to go in tertiary file

    dest: str = str(pathlib.Path(destination).resolve())
    src: str = str(pathlib.Path(source).resolve())

    if not (os.path.isdir(dest) and os.path.isdir(src)):
        msg = "Both source and destination must be directories"
        sys.exit(msg)

    paths: dict = defaultdict(list)
    for p in source_tree:
        pathdiff: str = os.path.relpath(p, src)
        new_path: str = os.path.join(dest, pathdiff)
        old_path: str = str(pathlib.Path(p).resolve())

        if is_file(new_path):
            paths["files"].append((old_path, new_path))
        else:
            paths["dirs"].append((old_path, new_path))

    return paths


def is_file(filepath: str) -> bool:
    # TODO needs to go in tertiary file
    filename: str = pathlib.Path(filepath).name
    if re.match(r".+\..+", filename):
        return True
    return False


def make_dir(directory: str) -> None:
    # TODO needs to go in tertiary file
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)


def copy_file(source: str, destination: str) -> None:
    # TODO needs to go in tertiary file
    shutil.copyfile(source, destination)
