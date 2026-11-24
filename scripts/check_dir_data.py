with open("public/directory-data.js", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(35, 65):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}", end="")
