#!/usr/bin/python3.12

"""Generates a static html website from markdown."""


from collections import defaultdict
import os
import pathlib
import re
import shutil
import sys

from generate_webpages import Path, generate_pages_recursive


class Resources:
    # TODO should be moved such that
    # from config import Resources

    _public: str = "./public"
    _static: str = "./static"
    _content: str = "./content"

    _markdown_index: str = "./content/index.md"
    _page_template: str = "./template.html"
    _html_index: str = ""

    def __init__(self) -> None:
        self._html_index: str = f"{self._public}/index.html"

    @property
    def public(self) -> Path:
        return pathlib.Path(self._public)

    @public.setter
    def set_public(self, public_dir: str | Path) -> None:
        if not os.path.exists(public_dir):
            msg = "Trying to set public resources with nonexistent directory"
            sys.exit(msg)

        p: Path = pathlib.Path(public_dir).resolve()
        self._public = str(p)

    @property
    def static(self) -> Path:
        return pathlib.Path(self._static)

    @static.setter
    def set_static(self, static_dir: str | Path) -> None:
        if not os.path.exists(static_dir):
            msg = "Trying to set static resources with nonexistent directory"
            sys.exit(msg)

        p: Path = pathlib.Path(static_dir).resolve()
        self._static = str(p)

    @property
    def content(self) -> Path:
        return pathlib.Path(self._content)

    @content.setter
    def set_content(self, content_dir: str | Path) -> None:
        if not os.path.exists(content_dir):
            msg = "Trying to set content resources with nonexistent directory"
            sys.exit(msg)

        p: Path = pathlib.Path(content_dir).resolve()
        self._content = str(p)

    @property
    def markdown_index(self) -> Path:
        return pathlib.Path(self._markdown_index)

    @markdown_index.setter
    def set_markdown_index(self, index_file: str | Path) -> None:
        if not os.path.exists(index_file):
            msg: str = f"File {index_file} could not be found"
            raise FileExistsError(msg)

        p: Path = pathlib.Path(index_file).resolve()
        self._markdown_index = str(p)

    @property
    def page_template(self) -> Path:
        return pathlib.Path(self._page_template)

    @page_template.setter
    def set_page_template(self, template_file: str | Path) -> None:
        if not os.path.exists(template_file):
            msg: str = f"File {template_file} could not be found"
            raise FileExistsError(msg)

        p: Path = pathlib.Path(template_file).resolve()
        self._page_template = str(p)

    @property
    def html_index(self) -> Path:
        return pathlib.Path(self._html_index)

    @html_index.setter
    def set_html_index(self, index_file: str | Path) -> None:
        if not os.path.exists(index_file):
            msg: str = f"File {index_file} could not be found"
            raise FileExistsError(msg)

        p: Path = pathlib.Path(index_file).resolve()
        self._html_index = str(p)


def main() -> None:
    res = Resources()
    make_public(res.static, res.public)
    # generate_page(res.markdown_index, res.page_template, res.html_index)
    generate_pages_recursive(res.content, res.page_template, res.public)


def make_public(static_source: Path, public_source: Path) -> None:
    if not clean_start(public_source):
        msg = "Website's public resources could not be generated"
        sys.exit(msg)

    static_dir: str = str(pathlib.Path(static_source).resolve())
    public_dir: str = str(pathlib.Path(public_source).resolve())

    static_list: list[str] = list_directory(static_dir)
    to_replicate: dict[str, list[tuple[str, str]]] = paths_to_create(
        static_dir, public_dir, static_list
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
            file_dest: str = file[1]
            copy_file(file_source, file_dest)  # TODO log the newly created files


def clean_start(public_dest: Path) -> bool:
    try:
        # assert directory_depth(public_dest) == 1
        shutil.rmtree(public_dest)
        os.mkdir(public_dest)
        return True
    except AssertionError:
        msg = "Public directory cleanup assertion checks failed"
        sys.exit(msg)
        return False
    except:  # TODO naked exception should be better handled
        return False


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


def directory_depth(directory: Path) -> int:
    # TODO needs to go in tertiary file
    return len(list(os.walk(directory)))


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


if __name__ == "__main__":
    main()
