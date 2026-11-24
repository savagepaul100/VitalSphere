with open("src/main/java/com/vitalsphere/VitalSphereDesktopClient.java", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("Preview Certificate")
print("Found Preview Certificate at:", idx)
print(text[idx-200:idx+600])
