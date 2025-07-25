import json

def count_items(punkte_str):
    return len(punkte_str.strip().split()) if punkte_str.strip() else 0

# Load from JSON file
with open("data.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# Process users
users = []
for key, info in raw_data.items():
    name = info.get("name", "")
    punkte = count_items(info.get("punkte", ""))
    punktehalb = count_items(info.get("punktehalb", ""))
    total = punkte + 0.5 * punktehalb
    users.append({
        "Name": name,
        "Total": total
    })

# Sort by total descending, then name ascending
sorted_users = sorted(users, key=lambda x: (-x["Total"], x["Name"]))

# Print results
for user in sorted_users:
    print(f'{user["Name"]}: {user["Total"]}')
