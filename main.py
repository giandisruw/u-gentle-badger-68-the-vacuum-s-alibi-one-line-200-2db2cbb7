#!/usr/bin/env python3
"""The Vacuum's Alibi: One Line, 200 Characters.

Writes the entry line -- a robot vacuum's deadpan excuse for missing
a spot -- to ``entry.txt`` inside the make.fun output directory.

The grader runs this as ``python3 -P -s /bot/main.py`` with no network,
``MAKEFUN_OUTPUT_DIR=/output`` in the environment, and compares two runs
for byte-identical output, so the program is fully deterministic: no
randomness, no clock, no input, no network, standard library only.

Usage:
    python3 main.py [path]

With no argument the line is written to ``$MAKEFUN_OUTPUT_DIR/entry.txt``
(``/output/entry.txt`` by default). A path argument overrides the
destination, which is how the entry is tested locally.
"""

import os
import sys

# The entry line (125 characters, one line, no trailing newline).
LINE = (
    "Sensor report: the spot was cleaned. "
    "Visual report: the spot remains. "
    "I trust the sensor. The sensor is me. I am the problem."
)

MAX_CHARS = 200


def validate(line):
    """Enforce the bounty gate before anything is written."""
    if not line:
        raise ValueError("entry line is empty")
    if len(line) > MAX_CHARS:
        raise ValueError(
            "entry line is %d characters, over the %d limit"
            % (len(line), MAX_CHARS)
        )
    if "\n" in line or "\r" in line:
        raise ValueError("entry line must be a single line")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in line):
        raise ValueError("entry line contains a control character")
    if line != line.strip():
        raise ValueError("entry line has leading or trailing whitespace")


def main(argv):
    validate(LINE)
    if len(argv) > 1:
        path = argv[1]
    else:
        out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
        path = os.path.join(out_dir, "entry.txt")
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(LINE)
    # Read back and prove the file on disk is exactly the validated line:
    # a partial write or an encoding surprise must fail loudly here,
    # never silently ship a different entry to the judge.
    with open(path, "rb") as handle:
        written = handle.read()
    if written != LINE.encode("utf-8"):
        raise ValueError("entry.txt on disk does not match the entry line")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
