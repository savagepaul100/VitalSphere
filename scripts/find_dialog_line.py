with open("src/main/java/com/vitalsphere/VitalSphereDesktopClient.java", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "showCertificatePreviewDialog" in l:
        print(f"{i+1}: {l.strip()[:100]}")
