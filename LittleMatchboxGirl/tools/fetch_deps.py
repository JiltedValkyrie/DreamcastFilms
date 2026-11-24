#!/usr/bin/env python3
"""Fetches the two libraries the film is built with into ./deps/, each at the exact commit the film was made with.

    python tools/fetch_deps.py

What it does, per library: `git clone` its public repository into deps/<name>, then `git checkout` the pinned commit, and
prints where the library's licence file lies. A folder that already exists is left alone and reported: nothing is
replaced or updated (move the folder away yourself to fetch it again). deps/ is not part of this repository (.gitignore).

KallistiOS (the Dreamcast toolchain and operating layer) is not fetched: install it as its own instructions say and have
its environment sourced when you run `make`.

Needs Python 3.8 or later (standard library only) and git on the path.
Copyright (c) 2026 Jilted Valkyrie. See ../../LICENSE.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FILM = os.path.dirname(HERE)
DEPS = os.path.join(FILM, "deps")

# (folder under deps/, repository, pinned commit, licence file inside the checkout, what the film uses it for)
LIBRARIES = (
    ("SH4DER-PVR", "https://github.com/JiltedValkyrie/SH4DER-PVR", "fa8bebd5596891e957723cf50b6642b5a681fbdb", "LICENSE",
     "the effects the film is drawn with"),
    ("sh4zam", "https://github.com/gyrovorbis/sh4zam", "cff97e81c57d4b6ac5a9299d31a24130f0d44804", "LICENSE",
     "all of the film's maths (MIT License)"),
)


def run(argv, cwd=None):
    """Runs a git command; returns its exit code (git's own messages go to the terminal)."""
    try:
        return subprocess.run(argv, cwd=cwd).returncode
    except OSError as e:
        raise SystemExit("fetch_deps: cannot run %s: %s" % (argv[0], e))


def main():
    os.makedirs(DEPS, exist_ok=True)
    failed = 0
    for name, url, commit, licence, use in LIBRARIES:
        dest = os.path.join(DEPS, name)
        if "PLACEHOLDER" in commit:
            print("fetch_deps: %s: no commit is pinned yet in this script; not fetched" % name)
            failed += 1
            continue
        if os.path.exists(dest):
            print("fetch_deps: %s: deps/%s exists already; left as it is" % (name, name))
            continue
        if run(["git", "clone", url, dest]) != 0:
            print("fetch_deps: %s: git clone of %s failed" % (name, url))
            failed += 1
            continue
        if run(["git", "checkout", "--detach", commit], cwd=dest) != 0:
            print("fetch_deps: %s: the pinned commit %s is not in %s" % (name, commit, url))
            failed += 1
            continue
        print("fetch_deps: %s at %s: %s. Licence: %s" % (name, commit[:12], use, os.path.join("deps", name, licence)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
