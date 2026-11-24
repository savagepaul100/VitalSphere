with open("src/main/java/com/vitalsphere/VitalSphereDesktopClient.java", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(618, 638):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}", end="")
