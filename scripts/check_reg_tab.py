with open("src/main/java/com/vitalsphere/VitalSphereDesktopClient.java", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("createDonorRegistrationTab")
if idx == -1:
    idx = text.find("Registration")
print("Found at:", idx)
print(text[idx:idx+1500])
