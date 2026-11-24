with open("src/main/java/com/vitalsphere/VitalSphereDesktopClient.java", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("void showCertificatePreviewDialog")
print(text[idx+1000:idx+2500])
