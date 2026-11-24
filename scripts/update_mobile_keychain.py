path = r"public/m/index.html"
with open(path, "r", encoding="utf-8") as f:
    c = f.read()

target = "      <!-- Citizens & Donors -->"
replacement = """      <!-- Patient Attendants / Recipients -->
      <div style="font-size:0.68rem; font-weight:800; color:var(--slate-400); text-transform:uppercase; margin:14px 0 6px;">Patient Attendants / Recipients (3)</div>

      <div class="keychain-item-mobile" onclick="selectMobileAccount('attendant.vijay@apollohospitals.org', 'Vijay Kumar (Attendant)', 'RECIPIENT_ATTENDANT')">
        <div class="k-avatar" style="background:#e11d48;">V</div>
        <div class="k-info">
          <div class="k-name">Vijay Kumar (Patient Attendant)</div>
          <div class="k-mail">attendant.vijay@apollohospitals.org</div>
        </div>
        <div class="k-role-badge" style="background:rgba(225,29,72,0.15); color:#fda4af;">ATTENDANT</div>
      </div>

      <div class="keychain-item-mobile" onclick="selectMobileAccount('attendant.sunita@carehospitals.com', 'Sunita Reddy (Attendant)', 'RECIPIENT_ATTENDANT')">
        <div class="k-avatar" style="background:#e11d48;">S</div>
        <div class="k-info">
          <div class="k-name">Sunita Reddy (Patient Attendant)</div>
          <div class="k-mail">attendant.sunita@carehospitals.com</div>
        </div>
        <div class="k-role-badge" style="background:rgba(225,29,72,0.15); color:#fda4af;">ATTENDANT</div>
      </div>

      <!-- Citizens & Donors -->"""

if target in c:
    c = c.replace(target, replacement, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
    print("Patient attendants added to mobile keychain successfully!")
else:
    print("Target not found")
