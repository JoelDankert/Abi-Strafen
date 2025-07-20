#!/usr/bin/env python3
"""
check_spaces.py ― prüft ein data.json-File auf
fehlerhafte / fehlende Leerzeichen zwischen den Tokens.

Erwartetes Format (space-getrennt):
  punkte      : "3 3 2 1"
  punktehalb  : "4 7"
  strafen     : "3 3 2 -1 -3"   #  -N  == gestrichene Strafe N
"""

import json
import re
import sys
from pathlib import Path
from typing import List, Tuple

# ------- zulässige Tokens ---------------------------------
PUNKT_TOKENS   = {str(i) for i in range(9)}          # 0-8
STRAFEN_TOKENS = {str(i) for i in range(4)}          # 0-3
STRAFEN_TOKENS |= {f"-{t}" for t in STRAFEN_TOKENS}  # -0 … -3

FIELDS = (
    ("punkte",      PUNKT_TOKENS,   False),
    ("punktehalb",  PUNKT_TOKENS,   False),
    ("strafen",     STRAFEN_TOKENS, True),
)

# -----------------------------------------------------------
def scan_field(s: str, allowed: set, allow_minus: bool) -> Tuple[bool, List[str], List[str]]:
    """
    Läuft zeichenweise durch den String und liefert:
        missing_space  : True/False
        invalid_tokens : Liste unzulässiger Tokens
        tokens         : Liste erkannter Tokens
    """
    i, n = 0, len(s)
    miss_space = False
    tokens, invalid = [], []

    while i < n:
        if s[i].isspace():
            i += 1
            continue

        # möglicher Tokenbeginn --------------------------------
        if s[i] == "-":
            if not allow_minus or i + 1 >= n or not s[i + 1].isdigit():
                invalid.append("-")
                i += 1
                continue
            token = s[i : i + 2]       # z. B. "-3"
            i += 2
        elif s[i].isdigit():
            token = s[i]
            i += 1
        else:                          # unerwartetes Zeichen
            invalid.append(s[i])
            i += 1
            continue

        # Token valid?
        if token not in allowed:
            invalid.append(token)

        tokens.append(token)

        # Nach dem Token MUSS entweder Ende oder Whitespace kommen
        if i < n and not s[i].isspace():
            miss_space = True

    return miss_space, invalid, tokens


def main(path: Path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        sys.exit(f"Fehler beim Laden von {path}: {e}")

    total_errors = 0

    for uid, person in data.items():
        name = person.get("name", f"(kein Name) [{uid}]")

        for field, allowed, allow_minus in FIELDS:
            raw = str(person.get(field, ""))

            miss_space, invalid, _ = scan_field(raw, allowed, allow_minus)
            if not miss_space and not invalid:
                continue

            total_errors += 1
            print(f"\n✗  Fehler bei {name}  →  Feld '{field}'")
            if miss_space:
                print("   • fehlende Leerzeichen gefunden")
            if invalid:
                print("   • ungültige Tokens:", ", ".join(invalid))
            print("   → Original:", raw)

    if total_errors == 0:
        print("✓  Keine Fehler gefunden – alle Tokens sauber getrennt.")
    else:
        print(f"\nInsgesamt {total_errors} fehlerhafte Einträge gefunden.")


if __name__ == "__main__":
    json_file = Path(sys.argv[1] if len(sys.argv) > 1 else "data.json")
    main(json_file)
