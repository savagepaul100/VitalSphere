import os
import re

print("Cleaning handleDonateAction and fixing mojibake...")

# 1. Update public/index.html
html_path = os.path.abspath("public/index.html")
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace handleDonateAction
old_fn_pattern = re.compile(r'window\.handleDonateAction\s*=\s*function\(reqId\)\s*\{[\s\S]*?alert\(\s*`[^\n]*SUCCESS: Notification dispatched[\s\S]*?\);\s*\};')

new_fn = """window.handleDonateAction = function(reqId) {
      const r = (window.fullRecipientsList || []).find(x => x.id === reqId);
      if (!r) return;

      const donorName = window.currentUser ? (window.currentUser.name || window.currentUser.email) : "Verified Voluntary Donor";

      const confirmed = confirm(
        `Confirm Voluntary Blood Donation Commitment:\\n\\n` +
        `Patient: ${r.patientName}\\n` +
        `Required Blood Group: ${r.bloodGroup}\\n` +
        `Hospital: ${r.hospital}\\n` +
        `Units: ${r.units}\\n\\n` +
        `When you click OK, VitalSphere will immediately dispatch a verified donor notification to the patient attendant (${r.contact}).`
      );

      if (!confirmed) return;

      r.status = 'DONOR FOUND (Matched with ' + donorName + ')';

      // Dispatch real-time notifications
      addNotification({
        category: 'DONATION',
        title: `✓ Donor Found for ${r.patientName}!`,
        message: `Donor ${donorName} has accepted emergency request ${r.id} (${r.bloodGroup}) at ${r.hospital}. Attendant notified at ${r.contact}.`,
        time: 'Just now',
        unread: true
      });

      addNotification({
        category: 'DONATION',
        title: `Donation Commitment Registered`,
        message: `You have committed to donate blood for ${r.patientName} (${r.bloodGroup}) at ${r.hospital}. Attendant phone: ${r.contact}.`,
        time: 'Just now',
        unread: true
      });

      applyDirectoryFilter();
      if (document.getElementById('fsDetailModal').style.display === 'flex') {
        openRecipientDetails(reqId);
      }

      alert(
        `✓ SUCCESS: Notification dispatched to ${r.patientName}'s attendant!\\n\\n` +
        `Patient Attendant: ${r.contact}\\n` +
        `Hospital Desk: ${r.hospital}\\n\\n` +
        `Thank you for saving a life!`
      );
    };"""

if old_fn_pattern.search(content):
    content = old_fn_pattern.sub(new_fn, content)
    print("Replaced handleDonateAction successfully.")
else:
    print("Warning: regex pattern for handleDonateAction did not match.")

# Replace any mojibake in public/index.html
mojibake_map = {
    'âœ“': '✓',
    'âœ•': '✕',
    'â€¢': '•',
    'â€”': '—',
    'â†’': '→',
    'â†': '←',
    'Â©': '©'
}
for bad, good in mojibake_map.items():
    if bad in content:
        content = content.replace(bad, good)
        print(f"Replaced mojibake '{bad}' -> '{good}' in index.html")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)

# 2. Update public/m/index.html mojibake
m_path = os.path.abspath("public/m/index.html")
with open(m_path, "r", encoding="utf-8") as f:
    m_content = f.read()

for bad, good in mojibake_map.items():
    if bad in m_content:
        m_content = m_content.replace(bad, good)
        print(f"Replaced mojibake '{bad}' -> '{good}' in m/index.html")

with open(m_path, "w", encoding="utf-8") as f:
    f.write(m_content)

# 3. Update Java client mojibake
java_path = os.path.abspath("src/main/java/com/vitalsphere/VitalSphereDesktopClient.java")
with open(java_path, "r", encoding="utf-8") as f:
    j_content = f.read()

java_mojibake_map = {
    'âœ“': '\\u2713',
    'âœ•': '\\u2715',
    'â€¢': '\\u2022',
    'â€”': '\\u2014',
    'â†’': '\\u2192',
    'â†': '\\u2190',
    'Â©': '\\u00A9',
    '✓': '\\u2713',
    '✕': '\\u2715',
    '•': '\\u2022',
    '—': '\\u2014',
    '→': '\\u2192',
    '←': '\\u2190'
}
for bad, good in java_mojibake_map.items():
    if bad in j_content:
        j_content = j_content.replace(bad, good)
        print(f"Replaced '{bad}' -> '{good}' in VitalSphereDesktopClient.java")

with open(java_path, "w", encoding="utf-8") as f:
    f.write(j_content)

print("All files updated and cleaned.")
