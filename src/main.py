#!/usr/bin/python3.12

"""Generates a static html website from markdown."""


from collections import defaultdict
import os
import pathlib
import re
import shutil
import sys


type Path = os.PathLike | pathlib.Path


class Source:
    # should be moved such that
    # from config import Source

    _public: str = "./dummy"
    _static: str = "./static"

    @property
    def public(self) -> Path:
        return pathlib.Path(self._public)

    @public.setter
    def set_public(self, public_dir: str | Path) -> None:
        if not os.path.exists(public_dir):
            msg = "Trying to set public resources to nonexistent directory"
            sys.exit(msg)

        p: Path = pathlib.Path(public_dir).resolve()
        self._public = str(p)

    @property
    def static(self) -> Path:
        return pathlib.Path(self._static)

    @static.setter
    def set_static(self, static_dir: str | Path) -> None:
        if not os.path.exists(static_dir):
            msg = "Trying to set static resources to nonexistent directory"
            sys.exit(msg)

        p: Path = pathlib.Path(static_dir).resolve()
        self._static = str(p)


def main() -> None:
    sources = Source()
    public_source = sources.public
    static_source = sources.static
    make_public(static_source, public_source)


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
            make_dir(new_dir)

    files_to_copy: list[tuple[str, str]] | None = to_replicate.get("files")
    if files_to_copy:
        for file in files_to_copy:
            file_source: str = file[0]
            file_dest: str = file[1]
            copy_file(file_source, file_dest)


def clean_start(public_dest: Path) -> bool:
    try:
        assert directory_depth(public_dest) == 1
        shutil.rmtree(public_dest)
        os.mkdir(public_dest)
        return True
    except AssertionError:
        msg = "Public directory cleanup assertion checks failed"
        sys.exit(msg)
        return False
    except:
        # TODO naked exception should be handled
        return False


def directory_depth(directory: Path) -> int:
    return len(list(os.walk(directory)))


def list_directory(directory: str, filepaths: list[str] = []) -> list[str]:

    target_dir: str = str(pathlib.Path(directory).resolve())
    for node in os.listdir(target_dir):
        nodepath: str = os.path.join(target_dir, node)
        if re.match(r".+\..+", node):
            filepaths.append(nodepath)
        else:
            filepaths.append(nodepath + "/")
            list_directory(nodepath, filepaths)

    return filepaths


def paths_to_create(
    source: str, destination: str, source_tree: list[str]
) -> dict[str, list[tuple[str, str]]]:

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

        if new_path.endswith("/"):
            paths["dirs"].append((old_path, new_path))
        else:
            paths["files"].append((old_path, new_path))

    return paths


def make_dir(directory: str) -> None:
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)


def copy_file(source: str, destination: str) -> None:
    shutil.copyfile(source, destination)


if __name__ == "__main__":
    main()
