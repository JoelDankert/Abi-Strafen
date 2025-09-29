import json

def convert_input_json(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    converted = []

    for uid, user in data.items():
        if "name" not in user or not user["name"]:
            continue

        name_parts = user["name"].split(maxsplit=1)
        vorname = name_parts[0]
        nachname = name_parts[1] if len(name_parts) > 1 else ""

        converted.append({
            "vorname": vorname,
            "nachname": nachname,
            "klasse": "11",          # kann manuell ergänzt werden
            "nfc_uid": ""
        })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(converted, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(converted)} Nutzer konvertiert → {output_path}")

if __name__ == "__main__":
    input_file = input("Pfad zur Eingabe-JSON: ")
    output_file = input("Pfad zur Ausgabe-JSON: ")
    convert_input_json(input_file, output_file)
