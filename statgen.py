#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from colorama import Fore, Style

# --------------------------------------------------------------------------- #
MIN_POINTS      = 7
TIME_FRACTION   = 0.5
MONEY_FRACTION  = 0.35
VALUE_ABIBALL   = 1   # Punktewert für ID "9"
DATA_FILE       = "data.json"
# --------------------------------------------------------------------------- #


def load_data(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def calculate_totals(data: dict) -> tuple[float, float]:
    points_now = 0.0
    points_planned = 0.0

    for info in data.values():
        full = info.get("punkte", "").split()
        half = info.get("punktehalb", "").split()
        # aktuelle Punkte berechnen
        pts = sum(VALUE_ABIBALL if pid == "9" else 1 for pid in full) \
              + 0.5 * len(half)
        points_now += pts
        # Planung: mind. MIN_POINTS, wer mehr hat, behält seinen Stand
        points_planned += max(pts, MIN_POINTS)

    return points_now, points_planned


def main() -> None:
    path = Path(DATA_FILE)
    if not path.exists():
        print(f"Datei »{DATA_FILE}« nicht gefunden.")
        return

    data = load_data(path)
    if not data:
        print("Keine Einträge in JSON.")
        return

    points_now, points_planned = calculate_totals(data)
    n = len(data)

    # Geld-Projektion per Dreisatz
    money_now_pct = MONEY_FRACTION * 100
    try:
        money_proj_pct = MONEY_FRACTION * points_planned / points_now * 100
    except ZeroDivisionError:
        money_proj_pct = 0.0
    money_gap_pct = max(0.0, 100 - money_proj_pct)

    money_proj_time_only_pct = MONEY_FRACTION / TIME_FRACTION * 100
    


    # Tabelle aufbauen
    rows = [
    ("Key","Val"),
     (f"{Fore.WHITE}Personen gesamt{Style.RESET_ALL}",                            str(n)),
    (f"{Fore.WHITE}Aktuelle Dienste{Style.RESET_ALL}",                            f"{points_now:.1f}"),
    (f"{Fore.WHITE}Aktueller Geldstand{Style.RESET_ALL}",                         f"{money_now_pct:.1f}%"),
    (f"{Fore.YELLOW}Geschätzter Geldstand (nur Zeitanteil){Style.RESET_ALL}",     f"{money_proj_time_only_pct:.1f}%"),
    (f"{Fore.RED}Fehlender Geldanteil (nur Zeitanteil){Style.RESET_ALL}",         f"{100 - money_proj_time_only_pct:.1f}%"),
    (f"{Fore.YELLOW}Geplanter Geldstand (bei min {MIN_POINTS}){Style.RESET_ALL}", f"{money_proj_pct:.1f}%"),
    (f"{Fore.RED}Fehlender Geldanteil (bei min {MIN_POINTS}){Style.RESET_ALL}",   f"{money_gap_pct:.1f}%"),
    ]   

    # Spaltenbreiten berechnen
    col1 = max(len(r[0]) for r in rows) + 2
    col2 = max(len(r[1]) for r in rows) + 2

    # Ausgabe
    print()
    print(f"{Style.BRIGHT}{MIN_POINTS} Mindestdienste;\n{VALUE_ABIBALL} für Abiball{Style.RESET_ALL}")
    print()
    print(rows[0][0].ljust(col1) + rows[0][1].ljust(col2))
    print("-" * (col1 + col2))
    for label, val in rows[1:]:
        print(label.ljust(col1) + val.ljust(col2))
    print()


if __name__ == "__main__":
    main()
