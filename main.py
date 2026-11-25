#!/usr/bin/env python3
"""One Line, Big Laugh entry.

This program does exactly one small thing: it prints a single original
one-line joke to standard output, and mirrors that same line into
/output/entry.txt so the stored entry file always matches the program's
own output byte for byte. Before printing, it checks the line against
the bounty's gate (one line, 1 to 200 characters) and refuses to emit
anything that would fail it.

Standard library only. No arguments, no network, no randomness, no
side effects beyond the one output file.
"""

import os
import sys

SETUP = "My grandad left me his sense of humour in his will"
PUNCHLINE = "the lawyer read it out, nobody laughed, and honestly, that proved his point."

# The joke is held as setup + punchline and joined with an em dash, so the
# line is assembled from its two beats rather than stored as one blob.
JOKE = SETUP + " — " + PUNCHLINE

OUTPUT_PATH = "/output/entry.txt"

# The gate the bounty seals: the entry must be UTF-8 text of 1 to 200
# characters, not only white space, and a single line. Enforce it here so
# the program can never hand in an entry the gate would reject.
MAX_CHARS = 200


def validate(text: str) -> None:
    """Refuse to emit a line that would fail the bounty's entry gate."""
    line = text.rstrip("\n")
    if not line.strip():
        raise ValueError("joke line is empty")
    if "\n" in line or "\r" in line:
        raise ValueError("joke must be exactly one line")
    if len(line) > MAX_CHARS:
        raise ValueError("joke exceeds 200 characters: %d" % len(line))


def render() -> str:
    """Return the full joke line, terminated by a single newline."""
    return JOKE + "\n"


def mirror(text: str) -> None:
    """Write the line to the entry file and verify the write landed intact."""
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    with open(OUTPUT_PATH, "r", encoding="utf-8", newline="") as handle:
        if handle.read() != text:
            raise IOError("entry file does not match printed output")


def main() -> int:
    """Print the joke line and mirror it to the entry file."""
    text = render()
    validate(text)
    sys.stdout.write(text)
    sys.stdout.flush()
    mirror(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
