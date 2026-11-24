with open("src/main/java/com/vitalsphere/VitalSphereDesktopClient.java", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("JPanel createDonorRegistrationPanel")
print("Found method at:", idx)
print(text[idx:idx+2500])
