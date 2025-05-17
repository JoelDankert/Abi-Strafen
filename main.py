import json
import re # For regular expression parsing of input lines

def find_matching_user_ids(name_to_find_lower, data):
    """
    Finds user IDs in the data matching the given name.

    Args:
        name_to_find_lower (str): The name to search for (should be pre-processed: lowercased, stripped).
        data (dict): The JSON data (dictionary of users).

    Returns:
        list: A list of user_ids that match. Empty if no match.
              If multiple users match by partial name, all their IDs are returned.
    """
    if not name_to_find_lower:
        return []

    matched_ids = []

    # 1. Try exact full name match
    for user_id, details in data.items():
        if details.get("name", "").lower() == name_to_find_lower:
            return [user_id] # Exact match is considered unique and best

    # 2. If no exact full name match, try partial name (first or last name components)
    # This allows "Max" to match "Max Aicher" or "Aicher" to match "Max Aicher" / "Jule Aicher"
    for user_id, details in data.items():
        current_name_parts = details.get("name", "").lower().split()
        if name_to_find_lower in current_name_parts:
            matched_ids.append(user_id)
            
    return list(set(matched_ids)) # Return unique IDs found by partial match

def process_batch_update(file_path, batch_input_string):
    """
    Processes a batch of update instructions from a multi-line string.

    Args:
        file_path (str): Path to the JSON file.
        batch_input_string (str): The multi-line string with update instructions.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}. Please ensure the file exists.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_path}. Check for syntax errors.")
        return
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
        return

    lines = batch_input_string.strip().split('\n')
    data_changed_overall = False

    print("\n--- Processing Batch ---")

    for line_number, line_content in enumerate(lines):
        line_content = line_content.strip()
        if not line_content:
            continue

        print(f"Processing line {line_number + 1}: \"{line_content}\"")

        # Regex to parse: <CodeLetter><Value>:<Names>
        # e.g., P3: name1, name2  => Code: P, Value: 3, Names: name1, name2
        # e.g., SCheck: name3     => Code: S, Value: Check, Names: name3
        match = re.match(r"([PHS])([^:]+):\s*(.*)", line_content)

        if not match:
            print(f"  Error: Invalid format on line {line_number + 1}. Expected '<P/H/S><Value>:<Names>'. Skipping.")
            continue

        code = match.group(1)
        value_to_add = match.group(2).strip()
        names_string = match.group(3).strip()

        if not value_to_add:
            print(f"  Error: Value to add is empty on line {line_number + 1}. Skipping.")
            continue
        if not names_string:
            print(f"  Error: Names list is empty on line {line_number + 1}. Skipping.")
            continue

        field_to_update = ""
        if code == 'P':
            field_to_update = "punkte"
        elif code == 'H':
            field_to_update = "punktehalb"
        elif code == 'S':
            field_to_update = "strafen"
        # No else needed as regex ensures P, H, or S

        names_to_process = [name.strip() for name in names_string.split(',') if name.strip()]

        if not names_to_process:
            print(f"  Error: No valid names found after parsing on line {line_number + 1}. Skipping.")
            continue
            
        line_had_successful_update = False
        for name_raw in names_to_process:
            name_to_find_lower = name_raw.lower()
            
            matched_ids = find_matching_user_ids(name_to_find_lower, data)

            if len(matched_ids) == 1:
                user_id_to_update = matched_ids[0]
                person_data = data.get(user_id_to_update) # Should always exist if ID is from data.keys()

                if person_data: # Redundant check if find_matching_user_ids is correct
                    current_value = person_data.get(field_to_update)
                    if current_value is None: # Field might not exist or be null
                        person_data[field_to_update] = value_to_add
                    else:
                        person_data[field_to_update] = str(current_value) + value_to_add
                    
                    print(f"    SUCCESS: Updated '{person_data.get('name', 'N/A')}' (ID: {user_id_to_update}). Field '{field_to_update}' appended with '{value_to_add}'. New value: '{person_data[field_to_update]}'")
                    data_changed_overall = True
                    line_had_successful_update = True
                else:
                    # This case should ideally not be reached if find_matching_user_ids works correctly
                    print(f"    INTERNAL ERROR: Matched ID {user_id_to_update} for '{name_raw}' but data not found.")

            elif len(matched_ids) == 0:
                print(f"    INFO: Name '{name_raw}' - No match found. Skipping this name.")
            else: # len(matched_ids) > 1 (ambiguous)
                print(f"    WARNING: Name '{name_raw}' - Multiple potential matches found. No update made for this name due to ambiguity:")
                for uid in matched_ids:
                    print(f"      - ID: {uid}, Name: {data[uid].get('name', 'N/A')}")
        
        if not line_had_successful_update :
             print(f"  No updates made for line {line_number + 1}.")


    print("--- Batch Processing Complete ---")

    if data_changed_overall:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"\nSuccessfully updated and saved the JSON file: {file_path}")
        except IOError:
            print(f"\nError: Could not write updates to file {file_path}")
        except Exception as e:
            print(f"\nAn unexpected error occurred while writing the file: {e}")
    else:
        print("\nNo changes were made to the data that required saving.")

# --- How to use the tool ---
if __name__ == "__main__":
    json_file_path = "data.json"  # Replace with the actual path to your JSON file

    print(f"JSON Update Tool - Using file: {json_file_path}")
    print("----------------------------------------------------")
    print("Enter your update instructions line by line or paste a block.")
    print("Format: <P/H/S><Value>:<Comma-separated names>")
    print("Example: P3: joel, jule, riana, silas")
    print("         H2: joel, melis")
    print("         S1: max")
    print("Type 'ENDUPDATE' on a new line when you are finished with a batch.")
    print("Type 'exit' on a new line to quit the tool.")
    print("----------------------------------------------------")

    while True:
        print("\nEnter batch update lines (type 'ENDUPDATE' on a new line to process, or 'exit' to quit):")
        batch_lines = []
        while True:
            try:
                line = input()
            except EOFError: # Handle Ctrl+D or unexpected end of input
                print("EOF detected. Assuming 'exit'.")
                line = "exit"

            if line.strip().upper() == 'ENDUPDATE':
                break
            if line.strip().lower() == 'exit':
                print("Exiting tool.")
                exit() # Exit the entire script
            batch_lines.append(line)
        
        if not batch_lines:
            print("No input received for this batch.")
            continue # Go to next iteration of outer while loop

        batch_input_string = "\n".join(batch_lines)
        if batch_input_string.strip(): # Ensure there's some actual content
            process_batch_update(json_file_path, batch_input_string)
        else:
            print("Empty batch input received after processing. Nothing to do.")
        print("-" * 50)
