import hashlib

# Liste der Namen
namen = [
    "Joel Dankert",
    "Riana Binisan",
    "Silas Truppe"
]

def generate_key(name, length=10):
    # Hash mit SHA-256 erzeugen und in hex kürzen
    return hashlib.sha256(name.encode('utf-8')).hexdigest()[:length]

# Keys generieren
for name in namen:
    key = generate_key(name)
    print(f"{name} → {key}")

# https://joeldankert.github.io/Abi-Strafen/?key=b28e254b30
# https://joeldankert.github.io/Abi-Strafen/?key=6394b75747