with open("public/m/index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "stat-chip-lbl" in l:
        print(f"{i+1}: {l.strip()}")
