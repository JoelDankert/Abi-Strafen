import json

BASE_URL = "https://joeldankert.github.io/Abi-Strafen/?key="

def generate_links(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    lines = []
    for key, entry in data.items():
        name = entry.get("name", "Unbekannt")
        link = f"{name} : {BASE_URL}{key}"
        lines.append(link)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))

    print(f"{len(lines)} Links gespeichert in {output_file}")

# Anwendung
generate_links("data.json", "links.txt")
