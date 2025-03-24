import re
import json
import hashlib

def extract_key_blocks(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        raw = f.read()

    # Extrahiere alle Objekte mit dem Key "KEY"
    matches = re.findall(r'"KEY"\s*:\s*({.*?})(?=,\s*"KEY"|}$)', raw, re.DOTALL)

    entries = []
    for match in matches:
        try:
            obj = json.loads(match)
            entries.append(obj)
        except json.JSONDecodeError as e:
            print("Fehler beim Parsen eines Objekts:", e)
            continue

    return entries

def hash_name(name, salt="BLA", length=7):
    return hashlib.sha256((salt + name).encode('utf-8')).hexdigest()[:length]

def convert_and_hash(input_file, output_file):
    entries = extract_key_blocks(input_file)

    hashed_data = {
        hash_name(entry.get("name", "")): entry
        for entry in entries
        if "name" in entry
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(hashed_data, f, indent=2, ensure_ascii=False)

    print(f"{len(hashed_data)} Einträge erfolgreich verarbeitet und gespeichert in: {output_file}")

# Anwendung
convert_and_hash("databack.json", "data.json")
