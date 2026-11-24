with open("public/m/index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "class=\"stat-chip\"" in l or "class='stat-chip'" in l:
        print(f"Line {i+1} to {i+5}:")
        for j in range(i, min(i+15, len(lines))):
            print(f"  {lines[j]}", end="")
        break
