#!/usr/bin/env python3
"""Two Robots in an Elevator — make.fun entry.

One robot, one elevator ride, one line of small talk that tries
very hard to sound casual and fails in a very machine way.
"""

import hashlib
import os
import sys

# The entry: a single line of awkward robot small talk.
LINE = (
    "So... do you come up here often? I ran the numbers: same floor, "
    "same time, 214 days in a row — and I still rehearsed this sentence."
)

MAX_CHARS = 200
OUTPUT_NAME = "entry.txt"


def validate(line):
    """Enforce the competition rules for the line."""
    if not isinstance(line, str):
        raise TypeError("line must be a string")
    if not line:
        raise ValueError("line must not be empty")
    if line != line.strip():
        raise ValueError("line must not have leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if "  " in line:
        raise ValueError("line must not contain double spaces")
    if any(ord(ch) < 32 for ch in line):
        raise ValueError("line must not contain control characters")
    if not line.endswith((".", "!", "?")):
        raise ValueError("line must end with terminal punctuation")
    if len(line) >= MAX_CHARS:
        raise ValueError(
            "line is %d chars, must be under %d" % (len(line), MAX_CHARS)
        )
    return line


def write_entry(line, out_dir):
    """Write the line as UTF-8 bytes and verify the round trip."""
    data = validate(line).encode("utf-8")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUTPUT_NAME)
    with open(path, "wb") as handle:
        handle.write(data)
    with open(path, "rb") as handle:
        if handle.read() != data:
            raise RuntimeError("round-trip check failed: bytes differ")
    return path, data


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    path, data = write_entry(LINE, out_dir)
    print("wrote: %s" % path)
    print("chars: %d" % len(LINE))
    print("bytes: %d" % len(data))
    print("sha256: %s" % hashlib.sha256(data).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main())
