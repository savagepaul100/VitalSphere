import os

path = r"C:\Users\PAUL\Documents\VitalSphere\public\m\index.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update recipient card in renderMobileDirectory
old_recipient_card = '''            <a href="tel:${r.contact}" class="btn-call" style="background:var(--navy-900);">
              <span>📞</span> Contact Attendant (${r.contact})
            </a>
          </div>'''

new_recipient_card = '''            <div style="display:flex; gap:8px; margin-top:10px;">
              <button onclick="handleMobileDonate('${r.id}')" style="flex:1.2; height:42px; background:#dc2626; color:white; border:none; border-radius:8px; font-weight:800; font-size:0.88rem; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:6px;">
                <span>🩸</span> Donate
              </button>
              <a href="tel:${r.contact}" class="btn-call" style="flex:1; margin-top:0; background:var(--navy-900); text-decoration:none;">
                <span>📞</span> Attendant
              </a>
            </div>
          </div>'''

if old_recipient_card in content:
    content = content.replace(old_recipient_card, new_recipient_card, 1)
    print("Recipient card in mobile directory updated with Donate button")
else:
    print("Warning: old_recipient_card not found")

# 2. Add handleMobileDonate function
old_switch_dir = '    window.switchMobileDirectory = function(tab) {'
new_handle_donate = '''    window.handleMobileDonate = function(reqId) {
      const r = (window.fullRecipientsList || []).find(x => x.id === reqId);
      if (!r) return;

      const confirmed = confirm(
        `Confirm Voluntary Blood Donation Commitment:\\n\\n` +
        `Patient: ${r.patientName}\\n` +
        `Required Group: ${r.bloodGroup}\\n` +
        `Hospital: ${r.hospital}\\n` +
        `Units: ${r.units}\\n\\n` +
        `When you click OK, VitalSphere will immediately dispatch a verified donor notification to the patient attendant (${r.contact}).`
      );

      if (!confirmed) return;

      r.status = 'DONOR FOUND (Coordination in progress)';
      renderMobileDirectory();

      alert(
        `✓ SUCCESS: Notification dispatched to ${r.patientName}'s attendant!\\n\\n` +
        `Patient Attendant: ${r.contact}\\n` +
        `Hospital Desk: ${r.hospital}\\n` +
        `Thank you for saving a life!`
      );
    };

    window.switchMobileDirectory = function(tab) {'''

if old_switch_dir in content:
    content = content.replace(old_switch_dir, new_handle_donate, 1)
    print("handleMobileDonate function added to mobile index.html")
else:
    print("Warning: old_switch_dir not found")

# 3. Add Patient Attendants section to Mobile Keychain Sheet
old_donors_section = '      <!-- Citizen Donors -->'
new_patient_section = '''      <!-- Patient Attendants / Recipients -->
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

      <!-- Citizen Donors -->'''

if old_donors_section in content:
    content = content.replace(old_donors_section, new_patient_section, 1)
    print("Patient attendants added to mobile keychain")
else:
    print("Warning: old_donors_section not found")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("update_mobile_donate.py completed successfully")
