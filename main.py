import json
import re

# ANSI colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"

def find_matching_user_ids(name_to_find_lower, data):
    if not name_to_find_lower:
        return []

    matched_ids = []

    for user_id, details in data.items():
        if details.get("name", "").lower() == name_to_find_lower:
            return [user_id]

    for user_id, details in data.items():
        current_name_parts = details.get("name", "").lower().split()
        if name_to_find_lower in current_name_parts:
            matched_ids.append(user_id)

    return list(set(matched_ids))

def prompt_user_to_select(name, matched_ids, data, line_num):
    print(f"{YELLOW}Line {line_num}: Ambiguous match for '{name}'. Please select the correct one(s):{RESET}")
    for idx, uid in enumerate(matched_ids, 1):
        person = data.get(uid)
        print(f"{CYAN}{idx}) {person.get('name', 'N/A')} (ID: {uid}){RESET}")
    print(f"{YELLOW}Enter number(s) like 1,2 or 's' to skip:{RESET} ", end="")

    response = input().strip()
    if not response or response.lower() == 's':
        return []

    selections = []
    for part in response.split(','):
        try:
            index = int(part.strip())
            if 1 <= index <= len(matched_ids):
                selections.append(matched_ids[index - 1])
        except ValueError:
            continue
    return selections

def process_batch_update(file_path, batch_input_string):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        print(f"{RED}Error: Failed to load JSON from {file_path}{RESET}")
        return

    lines = batch_input_string.strip().split('\n')
    data_changed = False

    for line_num, line in enumerate(lines, start=1):
        line = line.strip()
        if not line:
            continue

        print(f"{CYAN}Processing Line {line_num}:{RESET} {line}")

        match = re.match(r"([PHS])([^:]+):\s*(.*)", line)
        if not match:
            print(f"{RED}Line {line_num}: Invalid format. Skipping.{RESET}")
            continue

        code = match.group(1)
        value = match.group(2).strip()
        names = [n.strip() for n in match.group(3).split(',') if n.strip()]

        field = {"P": "punkte", "H": "punktehalb", "S": "strafen"}.get(code)
        if not field:
            continue

        for name in names:
            ids = find_matching_user_ids(name.lower(), data)
            selected_ids = []

            if len(ids) == 1:
                selected_ids = ids
            elif len(ids) > 1:
                selected_ids = prompt_user_to_select(name, ids, data, line_num)
            else:
                print(f"{RED}Line {line_num}: Not found - {name}{RESET}")

            for uid in selected_ids:
                person = data.get(uid)
                if person:
                    current = person.get(field)
                    person[field] = value if current is None else str(current) + value
                    print(f"{GREEN}Line {line_num}: ({code}{value}) {person.get('name', 'N/A')}{RESET}")
                    data_changed = True

    if data_changed:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception:
            print(f"{RED}Error: Failed to write updates to file{RESET}")

# --- Run tool ---
if __name__ == "__main__":
    json_file_path = "data.json"

    print(f"JSON Update Tool - Using file: {json_file_path}")
    print("----------------------------------------------------")
    print("Enter update lines (e.g., P3: name1, name2)")
    print("Type 'end' to apply updates or 'exit' to quit.")
    print("----------------------------------------------------")

    while True:
        print("\nEnter batch update lines:")
        batch_lines = []
        while True:
            try:
                line = input()
            except EOFError:
                print("EOF detected. Exiting.")
                exit()

            if line.strip().lower() == 'end':
                break
            if line.strip().lower() == 'exit':
                print("Exiting tool.")
                exit()
            batch_lines.append(line)

        if not batch_lines:
            print("No input provided.")
            continue

        batch_input = "\n".join(batch_lines)
        process_batch_update(json_file_path, batch_input)
        print("-" * 50)
