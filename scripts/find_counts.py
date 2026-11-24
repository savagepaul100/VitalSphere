with open("public/index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "PATIENT" in l.upper() or "DONOR" in l.upper() and ("32" in l or "256" in l):
        print(f"{i+1}: {l.strip()[:100]}")
