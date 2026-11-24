with open("public/index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(1120, 1150):
    print(f"{i+1}: {lines[i]}", end="")
