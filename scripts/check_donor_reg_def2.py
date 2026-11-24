with open("src/main/java/com/vitalsphere/VitalSphereDesktopClient.java", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("JPanel createDonorRegistrationPanel")
print(text[idx+2500:idx+5000])
