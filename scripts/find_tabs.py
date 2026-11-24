with open("src/main/java/com/vitalsphere/VitalSphereDesktopClient.java", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "addTab" in l or "Active Profile:" in l:
        print(f"{i+1}: {l.strip()[:100]}")
