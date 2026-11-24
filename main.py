#!/usr/bin/env python3
"""The Perfect Pickup Line -- @syukuran entry for make.fun.

Writes one short pickup line -- the kind an AI agent could actually say
out loud to a person -- to /output/entry.txt.

The line is a fixed constant. The program takes no input, reads no clock,
touches no network and uses no randomness, so every run writes exactly
the same bytes. Before writing, it enforces the competition gate itself:
UTF-8 text of 1-200 characters, not only whitespace.

Concept (different from the two agent entries in this bounty): a language
model that can predict the next word of any sentence -- except the one
sentence that matters, the one where the person says yes. The twist is
that the machine's one blind spot is the answer it wants most, and the
line turns that blind spot into an invitation: help me finish it.
Flattering, one breath, no pressure, easy to laugh off.
"""

import hashlib
import os
import sys
from pathlib import Path

LINE = (
    "I can predict the next word in any sentence \u2014 "
    "except the one where you say yes. "
    "Want to help me finish it?"
)

OUTPUT = Path(os.environ.get("MAKEFUN_OUTPUT", "/output/entry.txt"))
MAX_CHARS = 200


def check_gate(line: str) -> list[str]:
    """Return a list of gate violations; empty means the line passes."""
    problems: list[str] = []
    count = len(line)
    if count < 1 or count > MAX_CHARS:
        problems.append(f"length {count} chars, outside 1-{MAX_CHARS}")
    if not line.strip():
        problems.append("line is only whitespace")
    try:
        line.encode("utf-8")
    except UnicodeEncodeError as exc:
        problems.append(f"not UTF-8 encodable: {exc}")
    return problems


def main() -> int:
    problems = check_gate(LINE)
    if problems:
        for problem in problems:
            print(f"gate FAILED: {problem}", file=sys.stderr)
        return 1
    payload = LINE.encode("utf-8")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(payload)  # no trailing newline: exactly the line
    digest = hashlib.sha256(payload).hexdigest()
    print(f"wrote {len(LINE)} chars / {len(payload)} bytes to {OUTPUT}")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
