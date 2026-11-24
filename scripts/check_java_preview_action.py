with open("src/main/java/com/vitalsphere/VitalSphereDesktopClient.java", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("previewBtn.addActionListener")
print(text[idx:idx+1500])
