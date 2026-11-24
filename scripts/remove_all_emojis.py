import re

# 1. Update public/m/index.html
m_path = r"C:\Users\PAUL\Documents\VitalSphere\public\m\index.html"
with open(m_path, "r", encoding="utf-8") as f:
    m_code = f.read()

m_code = m_code.replace("🖥️ Desktop", "Desktop [PC]")
m_code = m_code.replace("🔑 Sign In", "Sign In")
m_code = m_code.replace("🩺 Review Desk", "Review Desk")
m_code = m_code.replace('<span style="font-size:1.1rem;">🔑</span>', '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 2l-2 2m-1.5 1.5L14 9l-1.5-1.5L11 9l-1.5-1.5L8 9 2 15v5h5l6-6 1.5 1.5L16 14l1.5-1.5 3.5 3.5 2-2z"/></svg>')
m_code = m_code.replace("📍 ", "Location: ")
m_code = m_code.replace("<span>📞</span> Call Donor", "Call Donor")
m_code = m_code.replace("🏥 ", "Hospital: ")
m_code = m_code.replace("🩸 ", "Units: ")
m_code = m_code.replace("<span>🩸</span> Donate", "Donate")
m_code = m_code.replace("<span>📞</span> Attendant", "Call Attendant")
m_code = m_code.replace("📄 Uploaded Document", "Uploaded Document")
m_code = m_code.replace("📄 ", "Document: ")
m_code = m_code.replace("👁️", "")
m_code = m_code.replace("👁", "")
m_code = m_code.replace("📞 ", "Call: ")
m_code = m_code.replace("🚨 ", "Emergency: ")

# Check for any remaining emojis in m/index.html
remaining_m = []
for ch in m_code:
    cp = ord(ch)
    if (0x1F000 <= cp <= 0x1FFFF) or (0x2600 <= cp <= 0x27BF and ch not in ['✓', '✕', '•', '→', '←', '↔', '▲', '▼', '◆', '■', '★', '☆']):
        remaining_m.append(ch)

print(f"Remaining emojis in m/index.html: {set(remaining_m)}")

with open(m_path, "w", encoding="utf-8") as f:
    f.write(m_code)


# 2. Update public/index.html
d_path = r"C:\Users\PAUL\Documents\VitalSphere\public\index.html"
with open(d_path, "r", encoding="utf-8") as f:
    d_code = f.read()

bell_svg = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>'
key_svg = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 2l-2 2m-1.5 1.5L14 9l-1.5-1.5L11 9l-1.5-1.5L8 9 2 15v5h5l6-6 1.5 1.5L16 14l1.5-1.5 3.5 3.5 2-2z"/></svg>'

d_code = d_code.replace('<span style="font-size:1.05rem;">🔔</span>', bell_svg)
d_code = d_code.replace("🔔", bell_svg)
d_code = d_code.replace("🩺 Medical Review Desk", "Medical Review Desk")
d_code = d_code.replace('<span class="key-icon" onclick="toggleKeychain()">🔑</span>', f'<span class="key-icon" onclick="toggleKeychain()">{key_svg}</span>')
d_code = d_code.replace("🔑", key_svg)
d_code = d_code.replace("📍 ", "Location: ")
d_code = d_code.replace("📞 ", "Call: ")
d_code = d_code.replace("🩸 ", "Units: ")
d_code = d_code.replace("🏥 ", "Hospital: ")
d_code = d_code.replace("🎉 ", "✓ ")
d_code = d_code.replace("📄 ", "Document: ")
d_code = d_code.replace("🚨 ", "Emergency: ")
d_code = d_code.replace("👁️", "")
d_code = d_code.replace("👁", "")

remaining_d = []
for ch in d_code:
    cp = ord(ch)
    if (0x1F000 <= cp <= 0x1FFFF) or (0x2600 <= cp <= 0x27BF and ch not in ['✓', '✕', '•', '→', '←', '↔', '▲', '▼', '◆', '■', '★', '☆']):
        remaining_d.append(ch)

print(f"Remaining emojis in index.html: {set(remaining_d)}")

with open(d_path, "w", encoding="utf-8") as f:
    f.write(d_code)


# 3. Update src/main/java/com/vitalsphere/VitalSphereDesktopClient.java
j_path = r"C:\Users\PAUL\Documents\VitalSphere\src\main\java\com\vitalsphere\VitalSphereDesktopClient.java"
with open(j_path, "r", encoding="utf-8") as f:
    j_code = f.read()

j_code = j_code.replace("📄 Preview Certificate", "Preview Certificate")
j_code = j_code.replace("📎 Browse PDF Certificate", "Browse PDF Certificate")
j_code = j_code.replace("📎 Browse Proof PDF", "Browse Proof PDF")

remaining_j = []
for ch in j_code:
    cp = ord(ch)
    if (0x1F000 <= cp <= 0x1FFFF) or (0x2600 <= cp <= 0x27BF and ch not in ['✓', '✕', '•', '→', '←', '↔', '▲', '▼', '◆', '■', '★', '☆']):
        remaining_j.append(ch)

print(f"Remaining emojis in VitalSphereDesktopClient.java: {set(remaining_j)}")

with open(j_path, "w", encoding="utf-8") as f:
    f.write(j_code)

print("Emoji removal completed across website and Java desktop client!")
