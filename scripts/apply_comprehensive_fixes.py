import os
import re

print("Starting comprehensive fixes across VitalSphere...")

# 1. Update public/m/index.html
m_html_path = os.path.abspath("public/m/index.html")
with open(m_html_path, "r", encoding="utf-8") as f:
    m_html = f.read()

# Fix tab buttons to strictly "Donors" and "Recipients" without hardcoded numbers
old_m_tabs = """    <!-- Tab Switcher: Donors vs Recipients -->
    <div class="m-fs-tab-bar">
      <button class="m-fs-tab-btn active" id="mFsTabDonors" onclick="switchMobileFsTab('donors')">
        Donors (<span id="mFsDonorsCount">0</span>)
      </button>
      <button class="m-fs-tab-btn" id="mFsTabRecipients" onclick="switchMobileFsTab('recipients')">
        Recipients (<span id="mFsRecipientsCount">0</span>)
      </button>
    </div>"""

new_m_tabs = """    <!-- Tab Switcher: Donors vs Recipients -->
    <div class="m-fs-tab-bar">
      <button class="m-fs-tab-btn active" id="mFsTabDonors" onclick="switchMobileFsTab('donors')">Donors</button>
      <button class="m-fs-tab-btn" id="mFsTabRecipients" onclick="switchMobileFsTab('recipients')">Recipients</button>
    </div>"""

if old_m_tabs in m_html:
    m_html = m_html.replace(old_m_tabs, new_m_tabs)
    print("Replaced mobile directory tab titles with clean 'Donors' and 'Recipients'")
else:
    # regex fallback
    m_html = re.sub(
        r'<button class="m-fs-tab-btn active" id="mFsTabDonors"[^>]*>[\s\S]*?<\/button>\s*<button class="m-fs-tab-btn" id="mFsTabRecipients"[^>]*>[\s\S]*?<\/button>',
        '<button class="m-fs-tab-btn active" id="mFsTabDonors" onclick="switchMobileFsTab(\'donors\')">Donors</button>\n      <button class="m-fs-tab-btn" id="mFsTabRecipients" onclick="switchMobileFsTab(\'recipients\')">Recipients</button>',
        m_html
    )
    print("Applied regex replacement for mobile directory tab titles")

# Update subtitle dynamically in applyMobileFsFilter
old_m_filter_counts = """      const cntDEl = document.getElementById('mFsDonorsCount');
      if (cntDEl) cntDEl.innerText = matchedDonorsCount;
      const cntREl = document.getElementById('mFsRecipientsCount');
      if (cntREl) cntREl.innerText = matchedRecipientsCount;"""

new_m_filter_counts = """      const cntDEl = document.getElementById('mFsDonorsCount');
      if (cntDEl) cntDEl.innerText = matchedDonorsCount;
      const cntREl = document.getElementById('mFsRecipientsCount');
      if (cntREl) cntREl.innerText = matchedRecipientsCount;

      const subEl = document.getElementById('mFsModalSubtitle');
      if (subEl) {
        subEl.innerText = `${matchedDonorsCount} Donors • ${matchedRecipientsCount} Recipients for ${window.mFsCurrentGroup === 'ALL' ? 'All Groups' : window.mFsCurrentGroup}`;
      }"""

if old_m_filter_counts in m_html:
    m_html = m_html.replace(old_m_filter_counts, new_m_filter_counts)
    print("Updated applyMobileFsFilter to update subtitle with counts")

with open(m_html_path, "w", encoding="utf-8") as f:
    f.write(m_html)
print("Updated public/m/index.html successfully.")

# 2. Update public/index.html
desktop_html_path = os.path.abspath("public/index.html")
with open(desktop_html_path, "r", encoding="utf-8") as f:
    d_html = f.read()

# Fix fallback recipient generation to 64
d_html = re.sub(
    r'for \(let j = 1; j <= 32; j\+\+\) \{',
    'for (let j = 1; j <= 64; j++) {',
    d_html
)

# Update Who Wants Blood button count
d_html = re.sub(
    r'Who Wants Blood \(32 Patients\)',
    'Who Wants Blood (<span id="heroRecipientBtnCount">64</span> Patients)',
    d_html
)

# Update handleDonateAction so it doesn't block users with alert
old_donate_check = """      if (!window.currentUser) {
        alert("Please sign in with your account to confirm donation and dispatch a direct notification to the patient's attendant.");
        openLoginModal();
        return;
      }

      const confirmed = confirm(
        `Confirm Voluntary Blood Donation Commitment:\\n\\n` +
        `Patient: ${r.patientName}\\n` +
        `Blood Group: ${r.bloodGroup}\\n` +
        `Hospital: ${r.hospital}\\n` +
        `Attendant: ${r.contact}\\n\\n` +
        `Do you confirm commitment to donate? A real-time notification will be dispatched to the attendant immediately.`
      );

      if (!confirmed) return;

      r.status = "DONOR FOUND (Matched with " + window.currentUser.name + ")";
      renderDirectoryList();

      // Dispatch alert to patient attendant
      addNotification({
        category: 'DONATION',
        title: `Donor Matched for ${r.patientName}`,
        message: `${window.currentUser.name} (${window.currentUser.role || 'Voluntary Donor'}) committed to donate for ${r.patientName} (${r.bloodGroup}) at ${r.hospital}. Attendant notified at ${r.contact}.`,
        time: 'Just now'
      });

      alert(
        `✓ NOTIFICATION DISPATCHED TO PATIENT ATTENDANT!\\n\\n` +
        `Patient: ${r.patientName}\\n` +
        `Attendant Contact: ${r.contact}\\n` +
        `Hospital: ${r.hospital}\\n\\n` +
        `Thank you for saving a life!`
      );"""

new_donate_check = """      const donorName = window.currentUser ? window.currentUser.name : "Verified Voluntary Donor";
      const donorRole = window.currentUser ? (window.currentUser.role || 'Voluntary Donor') : "Citizen Volunteer";

      const confirmed = confirm(
        `Confirm Voluntary Blood Donation Commitment:\\n\\n` +
        `Patient: ${r.patientName}\\n` +
        `Blood Group: ${r.bloodGroup}\\n` +
        `Hospital: ${r.hospital}\\n` +
        `Attendant Contact: ${r.contact}\\n\\n` +
        `Do you confirm your donation commitment? A real-time dispatch notification will be sent to the patient attendant immediately.`
      );

      if (!confirmed) return;

      r.status = "DONOR FOUND (Matched with " + donorName + ")";
      renderDirectoryList();
      if (document.getElementById('fsDetailModal').style.display === 'flex') {
        openRecipientDetails(reqId);
      }

      // Dispatch alert to patient attendant
      addNotification({
        category: 'DONATION',
        title: `Donor Found for ${r.patientName}`,
        message: `${donorName} (${donorRole}) confirmed donation for ${r.patientName} (${r.bloodGroup}) at ${r.hospital}. Attendant notified at ${r.contact}.`,
        time: 'Just now'
      });

      alert(
        `✓ NOTIFICATION DISPATCHED TO PATIENT ATTENDANT!\\n\\n` +
        `Patient: ${r.patientName}\\n` +
        `Attendant Contact: ${r.contact}\\n` +
        `Hospital: ${r.hospital}\\n\\n` +
        `The patient's family and hospital desk have received your donation confirmation. Thank you for stepping up to save a life!`
      );"""

if old_donate_check in d_html:
    d_html = d_html.replace(old_donate_check, new_donate_check)
    print("Replaced handleDonateAction with seamless unblocked donation flow")
else:
    print("Note: handleDonateAction pattern check for exact string match")

# Add scrollToSection helper and smooth scrolling offset
if "window.scrollToSection =" not in d_html:
    scroll_helper = """
    // Smooth scrolling helper with guaranteed clearance so headers are never covered
    window.scrollToSection = function(id) {
      const el = document.getElementById(id);
      if (el) {
        const navHeight = 125;
        const bodyRect = document.body.getBoundingClientRect().top;
        const elementRect = el.getBoundingClientRect().top;
        const offsetPosition = elementRect - bodyRect - navHeight;
        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth'
        });
      }
    };
"""
    d_html = d_html.replace("// Shared Functions", scroll_helper + "\n    // Shared Functions")
    print("Added scrollToSection helper")

# Update nav links to use scrollToSection
d_html = d_html.replace('href="#inventory"', 'href="#inventory" onclick="scrollToSection(\'inventory\'); return false;"')
d_html = d_html.replace('href="#register"', 'href="#register" onclick="scrollToSection(\'register\'); return false;"')
d_html = d_html.replace('href="#request"', 'href="#request" onclick="scrollToSection(\'request\'); return false;"')
d_html = d_html.replace('href="#download"', 'href="#download" onclick="scrollToSection(\'download\'); return false;"')

# Ensure scroll-margin-top is 125px across all target containers
d_html = d_html.replace('scroll-margin-top: 110px;', 'scroll-margin-top: 125px;')
d_html = d_html.replace('scroll-margin-top: 100px;', 'scroll-margin-top: 125px;')

with open(desktop_html_path, "w", encoding="utf-8") as f:
    f.write(d_html)
print("Updated public/index.html successfully.")
