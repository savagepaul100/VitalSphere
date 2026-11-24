with open("public/m/index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(842, 856):
    print(f"{i+1}: {lines[i]}", end="")
