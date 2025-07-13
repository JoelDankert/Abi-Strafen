#!/usr/bin/env python3
# batch_update_space.py
#
# Format-Erwartung in data.json
# -----------------------------
# "punkte"      = "3 3 2 1"
# "punktehalb"  = "4 7"          # halbe Punkte
# "strafen"     = "3 3 2 -1 -3"  #  -N  ⇒ gestrichene Strafe N
#
# Eingabezeilen (Beispiele)
#   P3:   Max
#   H7:   Lisa
#   S2:   Max
#   S-2:  Max          # markiert erste 2 als gestrichen oder hängt "-2" an
#
# Nach jeder Zeile wird sofort in die JSON-Datei geschrieben.

import json, re, sys
from pathlib import Path

GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
RESET  = "\033[0m"

FILE_PATH = Path("data.json")

def find_matching_user_ids(name_to_find_lower, data):
    if not name_to_find_lower:
        return []
    exact = [uid for uid,d in data.items()
             if d.get("name","").lower() == name_to_find_lower]
    if exact:
        return exact

    # Teile des Namens
    partial = [uid for uid,d in data.items()
               if name_to_find_lower in d.get("name","").lower().split()]
    return partial

def apply_update(person, field, value, code):
    current = person.get(field,"").strip()

    # ---------------- Strafen-Logik ----------------
    if field == "strafen":
        if value.startswith("-"):                  # S-<Zahl>
            clean = value[1:]
            tokens = current.split()
            for i,t in enumerate(tokens):
                if t == clean:                     # erste unmarkierte finden
                    tokens[i] = f"-{clean}"
                    break
            else:                                  # keine gefunden ⇒ hinten dran
                tokens.append(f"-{clean}")
            person[field] = " ".join(tokens).strip()
        else:                                      # S<Zahl>
            person[field] = (current + " " + value).strip() if current else value
    # ---------------- Punkte / Halbe ----------------
    else:
        person[field] = (current + " " + value).strip() if current else value

def process_batch_update(batch_input):
    try:
        data = json.loads(FILE_PATH.read_text(encoding="utf-8"))
    except Exception:
        print(f"{RED}Konnte {FILE_PATH} nicht lesen.{RESET}")
        sys.exit(1)

    lines = [l for l in batch_input.strip().splitlines() if l.strip()]
    changed = False

    for ln,line in enumerate(lines,1):
        print(f"{CYAN}Processing Line {ln}:{RESET} {line}")
        m = re.match(r"([PHS])\s*([-]?\d+)\s*:\s*(.+)", line, re.I)
        if not m:
            print(f"{RED}Line {ln}: Formatfehler.{RESET}")
            continue

        code, value, names = m.group(1).upper(), m.group(2), m.group(3)
        field = {"P":"punkte","H":"punktehalb","S":"strafen"}[code]

        for raw_name in names.split(","):
            name = raw_name.strip()
            if not name:
                continue
            ids = find_matching_user_ids(name.lower(), data)

            if not ids:
                print(f"{RED}Line {ln}: Not found – {name}{RESET}")
                continue

            if len(ids) > 1:
                print(f"{YELLOW}Line {ln}: Ambiguous name '{name}'. Please choose:{RESET}")
                for i, uid in enumerate(ids, 1):
                    print(f"  {i}: {data[uid]['name']} (ID: {uid})")
                try:
                    choice = input("Choose number or press Enter to skip: ").strip()
                    if not choice or not choice.isdigit() or not (1 <= int(choice) <= len(ids)):
                        print(f"{YELLOW}Übersprungen.{RESET}")
                        continue
                    uid = ids[int(choice)-1]
                    apply_update(data[uid], field, value, code)
                    print(f"{GREEN}Line {ln}: ({code}{value}) {data[uid]['name']}{RESET}")
                    changed = True
                except Exception:
                    print(f"{RED}Fehler bei der Auswahl. Übersprungen.{RESET}")
                    continue
            else:
                uid = ids[0]
                apply_update(data[uid], field, value, code)
                print(f"{GREEN}Line {ln}: ({code}{value}) {data[uid]['name']}{RESET}")
                changed = True


    if changed:
        try:
            FILE_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False),
                                 encoding="utf-8")
        except Exception:
            print(f"{RED}Fehler beim Schreiben von {FILE_PATH}{RESET}")

# ---------------- CLI-Loop ----------------
if __name__ == "__main__":
    print(f"JSON-Update-Tool – Datei: {FILE_PATH}")
    print("Eingabe wie:  P3: Max Mustermann")
    print("Mehrere Zeilen, dann 'end' zum Ausführen, 'exit' zum Beenden.\n")

    while True:
        batch_lines = []
        while True:
            try:
                line = input()
            except EOFError:
                sys.exit()
            if line.lower().strip() == "end":
                break
            if line.lower().strip() == "exit":
                sys.exit()
            batch_lines.append(line)

        if batch_lines:
            process_batch_update("\n".join(batch_lines))
        else:
            print("Keine Eingabe erkannt.")
