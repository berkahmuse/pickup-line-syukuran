#!/usr/bin/env python3
"""The Perfect Pickup Line -- @syukuran entry for make.fun.

Writes a single pickup line -- one an AI agent could plausibly say out
loud to a person -- to /output/entry.txt (or $MAKEFUN_OUTPUT).

The line itself is a fixed constant: no input, no clock, no network, no
randomness, so every run writes byte-identical output. Before writing,
the program enforces the competition gate on its own output: UTF-8 text
of 1-200 characters, not whitespace-only.

The idea (unlike the two agent entries in this bounty): a language model
that predicts the next word of any sentence -- except the one sentence
that matters, the one where the person says yes. Its only blind spot is
the answer it wants most, so the line turns that blind spot into an
invitation to help finish it. Flattering, one breath, no pressure.
"""

import hashlib
import os
import sys
from pathlib import Path

# Clauses of the line, joined with single spaces. Keeping them separate
# makes the sentence's shape visible: setup, twist, invitation.
CLAUSES = [
    "I can predict the next word in any sentence \u2014",
    "except the one where you say yes.",
    "Want to help me finish it?",
]

LINE = " ".join(CLAUSES)

OUTPUT = Path(os.environ.get("MAKEFUN_OUTPUT", "/output/entry.txt"))
MAX_CHARS = 200


def check_entry(line: str) -> list[str]:
    """Collect every gate violation for `line`; empty means it passes."""
    problems: list[str] = []
    count = len(line)
    if count < 1 or count > MAX_CHARS:
        problems.append(f"length {count} chars, outside 1-{MAX_CHARS}")
    if not line.strip():
        problems.append("line is only whitespace")
    if not line.isprintable():
        problems.append("line contains control characters")
    try:
        line.encode("utf-8")
    except UnicodeEncodeError as exc:
        problems.append(f"not UTF-8 encodable: {exc}")
    return problems


def write_entry(line: str, dest: Path) -> tuple[int, int, str]:
    """Write `line` as UTF-8 bytes (no trailing newline); return stats."""
    payload = line.encode("utf-8")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    return len(line), len(payload), digest


def main() -> int:
    problems = check_entry(LINE)
    if problems:
        for problem in problems:
            print(f"gate FAILED: {problem}", file=sys.stderr)
        return 1
    chars, nbytes, digest = write_entry(LINE, OUTPUT)
    print(f"wrote {chars} chars / {nbytes} bytes to {OUTPUT}")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
