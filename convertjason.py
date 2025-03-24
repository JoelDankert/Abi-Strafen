import json
import hashlib

def hash_key(key, salt="BLA"):
    return hashlib.sha256((salt + key).encode('utf-8')).hexdigest()

def transform_json_keys(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    hashed_data = {hash_key(k): v for k, v in data.items()}

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(hashed_data, f, indent=2, ensure_ascii=False)

# Beispiel: input.json einlesen, output.json schreiben
transform_json_keys("databack.json", "data.json")
