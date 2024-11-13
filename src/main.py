#!/usr/bin/python3.12

"""Generates a static html website from markdown."""


import os
import pathlib
import shutil
import sys


type Path = os.PathLike | pathlib.Path


class Source:
    # should be moved such that
    # from config import Source

    _public: str = "./public"
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

    static_tree: list[str] = os.listdir(static_source)
    print("TREE:", static_tree)
    for node in static_tree:
        print(node)


def clean_start(public_dest: Path) -> bool:
    try:
        shutil.rmtree(public_dest)
        os.mkdir(public_dest)
        return True
    except:
        # TODO naked exception should be handled
        return False


if __name__ == "__main__":
    main()
