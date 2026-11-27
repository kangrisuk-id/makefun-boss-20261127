#!/usr/bin/env python3
"""One Word for the Boss — entry writer.

Writes exactly one word describing the boss to entry.txt, per the bounty gate:
UTF-8 text of 1-30 characters, not only whitespace, a single word, no caption,
no explanation. The word is the whole entry.

Tournament winner (see candidates.md): "Hovercraft" — 34 candidates scored
against the judge brief's five criteria in order, top-8 knockout, 3-0,
final margin 1 over "Arsonist". It is a single word a person would actually
use about their boss, funny on its own (the boss hovering over your shoulder),
true (the hovering habit), fresh (not the first word anyone reaches for),
and it travels (hovering happens in a kitchen, a warehouse, or an office).

Pure standard library only; writes byte-exact output with no trailing newline.
"""

import os
import sys

# The tournament-winning word. One word, 10 characters, no spaces.
WORD = "Hovercraft"


def output_dir():
    """Resolve the output directory: MAKEFUN_OUTPUT_DIR, else /output, else ./output."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    if os.path.isdir("/output"):
        return "/output"
    return os.path.join(os.getcwd(), "output")


def self_check(word):
    """Gate self-check, mirroring the sealed scorer: UTF-8 text of 1-30
    characters, not only whitespace, a single word (no spaces), no trailing
    newline. Raises ValueError on any violation so a bad word never ships."""
    if not isinstance(word, str):
        raise ValueError("entry must be a string")
    if not (1 <= len(word) <= 30):
        raise ValueError("entry must be 1-30 characters, got %d" % len(word))
    if not word.strip():
        raise ValueError("entry must not be only whitespace")
    if any(ch.isspace() for ch in word):
        raise ValueError("entry must be a single word, no spaces: %r" % word)
    if word != word.strip():
        raise ValueError("entry must not have leading/trailing whitespace")
    word.encode("utf-8")  # must be encodable UTF-8
    return True


def main():
    self_check(WORD)
    out_dir = output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = WORD.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    # Read back and verify byte-exactness: what the grader reads is what we wrote.
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        raise ValueError("entry.txt mismatch: wrote %r, read back %r" % (data, written))
    return 0


if __name__ == "__main__":
    sys.exit(main())
