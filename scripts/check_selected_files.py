with open("src/main/java/com/vitalsphere/VitalSphereDesktopClient.java", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("selectedCertFile")
print("Found selectedCertFile at:", idx)
print(text[idx-100:idx+1200])
