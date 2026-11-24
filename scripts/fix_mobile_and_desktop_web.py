import os

# ==========================================
# 1. FIX PUBLIC/INDEX.HTML (Desktop)
# ==========================================
d_path = r"C:\Users\PAUL\Documents\VitalSphere\public\index.html"
with open(d_path, "r", encoding="utf-8") as f:
    d_html = f.read()

# Replace hardcoded metric values with dynamic IDs
old_d_metrics = '''  <!-- Key Metrics -->
  <div class="metrics-bar">
    <div class="metric-item">
      <div class="metric-value">256</div>
      <div class="metric-label">Enrolled Donors</div>
    </div>
    <div class="metric-item">
      <div class="metric-value">32</div>
      <div class="metric-label">Active Patient Requests</div>
    </div>'''

new_d_metrics = '''  <!-- Key Metrics -->
  <div class="metrics-bar">
    <div class="metric-item">
      <div class="metric-value" id="heroDonorCount">256</div>
      <div class="metric-label">Enrolled Donors</div>
    </div>
    <div class="metric-item">
      <div class="metric-value" id="heroRecipientCount">64</div>
      <div class="metric-label">Active Patient Requests</div>
    </div>'''

if old_d_metrics in d_html:
    d_html = d_html.replace(old_d_metrics, new_d_metrics, 1)
    print("Desktop metrics bar updated with dynamic IDs")
else:
    print("Warning: old_d_metrics not found in index.html")

# Ensure clean tab button names: Donors and Recipients
d_html = d_html.replace(
    '<button class="tab-btn active" id="btnTabDonors" onclick="switchDirectoryTab(\'donors\')">Donors (<span id="tabDonorsCount">256</span>)</button>',
    '<button class="tab-btn active" id="btnTabDonors" onclick="switchDirectoryTab(\'donors\')">Donors</button>'
)
d_html = d_html.replace(
    '<button class="tab-btn" id="btnTabRecipients" onclick="switchDirectoryTab(\'recipients\')">Recipients Who Want Blood (<span id="tabRecipientsCount">64</span>)</button>',
    '<button class="tab-btn" id="btnTabRecipients" onclick="switchDirectoryTab(\'recipients\')">Recipients</button>'
)
d_html = d_html.replace(
    '<button class="tab-btn" id="btnTabRecipients" onclick="switchDirectoryTab(\'recipients\')">Recipients Who Want Blood (32 Patients)</button>',
    '<button class="tab-btn" id="btnTabRecipients" onclick="switchDirectoryTab(\'recipients\')">Recipients</button>'
)
d_html = d_html.replace(
    '<button class="tab-btn active" id="btnTabDonors" onclick="switchDirectoryTab(\'donors\')">Donors (256 Members)</button>',
    '<button class="tab-btn active" id="btnTabDonors" onclick="switchDirectoryTab(\'donors\')">Donors</button>'
)

# Update switchDirectoryTab in index.html to not rewrite tab text
old_switch_dir = """      if (tab === 'donors') {
        heading.innerText = currentFilterGroup 
          ? `Verified Blood Donors for Group ${currentFilterGroup} (${window.fullDonorsList.length} Members Total)` 
          : `Verified Blood Donors Directory (${window.fullDonorsList.length} Members)`;
      } else {
        heading.innerText = `Recipients Who Want Blood (${window.fullRecipientsList.length} Inpatients)`;
      }"""

new_switch_dir = """      if (heading) {
        if (tab === 'donors') {
          heading.innerText = currentFilterGroup 
            ? `Verified Blood Donors for Group ${currentFilterGroup} (${window.fullDonorsList.length} Members Total)` 
            : `Verified Blood Donors Directory (${window.fullDonorsList.length} Members)`;
        } else {
          heading.innerText = `Recipients Who Want Blood (${window.fullRecipientsList.length} Inpatients)`;
        }
      }
      updateHeroStatsCounters();"""

if old_switch_dir in d_html:
    d_html = d_html.replace(old_switch_dir, new_switch_dir, 1)

with open(d_path, "w", encoding="utf-8") as f:
    f.write(d_html)
print("index.html updated successfully")


# ==========================================
# 2. FIX PUBLIC/M/INDEX.HTML (Mobile)
# ==========================================
m_path = r"C:\Users\PAUL\Documents\VitalSphere\public\m\index.html"
with open(m_path, "r", encoding="utf-8") as f:
    m_html = f.read()

# 2.1 Update Hero Stats Chips in Mobile
old_m_stats = '''      <div class="stat-chip">
        <div class="stat-chip-num">256</div>
        <div class="stat-chip-lbl">Enrolled Donors</div>
      </div>
      <div class="stat-chip">
        <div class="stat-chip-num">32</div>
        <div class="stat-chip-lbl">Active Requests</div>
      </div>'''

new_m_stats = '''      <div class="stat-chip">
        <div class="stat-chip-num" id="mHeroDonorCount">256</div>
        <div class="stat-chip-lbl">Enrolled Donors</div>
      </div>
      <div class="stat-chip">
        <div class="stat-chip-num" id="mHeroRecipientCount">64</div>
        <div class="stat-chip-lbl">Active Requests</div>
      </div>'''

if old_m_stats in m_html:
    m_html = m_html.replace(old_m_stats, new_m_stats, 1)
    print("Mobile hero stats chips updated with dynamic IDs")
else:
    print("Warning: old_m_stats not found")

# 2.2 Add Notification Bell and Active User Badge in Mobile Header
old_m_header_right = '''    <div class="header-right">
      <a href="/?view=desktop" class="btn-header" title="Switch to Full Desktop Version">Desktop [PC]</a>
      <button class="btn-header primary" onclick="openMobileLogin()">Sign In</button>
    </div>'''

new_m_header_right = '''    <div class="header-right" style="display:flex; align-items:center; gap:8px;">
      <a href="/?view=desktop" class="btn-header" title="Switch to Full Desktop Version" style="padding:5px 8px; font-size:0.72rem;">Desktop [PC]</a>
      
      <!-- Mobile Notification Bell with Real-Time Counter -->
      <button id="mNotifBellBtn" onclick="toggleMobileNotifSheet()" class="btn-header" style="position:relative; padding:6px 9px; display:inline-flex; align-items:center; justify-content:center; background:rgba(255,255,255,0.08); border-color:rgba(255,255,255,0.18);" title="Notifications & Transfusion Alerts">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>
        <span id="mNotifBadge" style="position:absolute; top:-4px; right:-4px; background:#dc2626; color:white; font-size:0.6rem; font-weight:900; border-radius:10px; padding:1px 5px; min-width:14px; text-align:center; display:inline-block;">3</span>
      </button>

      <!-- Active User Badge / Sign In Toggle -->
      <div id="mNavUserBadge" style="display:none; align-items:center; gap:6px;">
        <span id="mNavUserName" style="font-size:0.72rem; font-weight:800; color:#38bdf8; max-width:75px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">User</span>
        <button onclick="executeMobileSignOut()" class="btn-header" style="background:#dc2626; border-color:#dc2626; padding:4px 8px; font-size:0.68rem; font-weight:800;">Sign Out</button>
      </div>
      <button id="mNavSignInBtn" class="btn-header primary" onclick="openMobileLogin()" style="padding:5px 12px; font-size:0.75rem;">Sign In</button>
    </div>'''

if old_m_header_right in m_html:
    m_html = m_html.replace(old_m_header_right, new_m_header_right, 1)
    print("Mobile header updated with Notification Bell and User Badge")
else:
    print("Warning: old_m_header_right not found")

# 2.3 Add Mobile Notification Bottom Sheet HTML
m_notif_sheet_html = '''  <!-- Mobile Notification Center Bottom Sheet -->
  <div class="sheet-overlay" id="mNotifSheet" style="display:none; align-items:flex-end;">
    <div class="sheet-card" style="max-height:85vh; border-radius:16px 16px 0 0; padding:18px; overflow-y:auto;">
      <div class="sheet-head" style="margin-bottom:12px;">
        <div style="display:flex; align-items:center; gap:8px;">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>
          <div>
            <div style="font-size:0.95rem; font-weight:800;">Notification Center</div>
            <div style="font-size:0.68rem; color:#38bdf8;">Tap any alert to Donate or Request blood</div>
          </div>
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
          <button onclick="markAllMobileNotifsRead()" style="background:none; border:none; color:#38bdf8; font-size:0.72rem; font-weight:700; cursor:pointer;">Mark Read</button>
          <button class="sheet-close" onclick="closeMobileNotifSheet()">&times;</button>
        </div>
      </div>

      <!-- Category Filter Tabs -->
      <div style="display:flex; gap:6px; margin-bottom:12px; overflow-x:auto;">
        <button class="m-grp-pill active" onclick="filterMobileNotifCategory('ALL', this)">All</button>
        <button class="m-grp-pill" onclick="filterMobileNotifCategory('DONATION', this)">Donations</button>
        <button class="m-grp-pill" onclick="filterMobileNotifCategory('APPROVAL', this)">Approvals</button>
        <button class="m-grp-pill" onclick="filterMobileNotifCategory('EMERGENCY', this)">Emergency</button>
      </div>

      <!-- Notifications Container -->
      <div id="mNotifItemsList">
        <!-- Rendered dynamically -->
      </div>
    </div>
  </div>'''

if 'id="mNotifSheet"' not in m_html:
    m_html = m_html.replace('<!-- Bottom Mobile Pill Tab Bar', m_notif_sheet_html + '\n  <!-- Bottom Mobile Pill Tab Bar', 1)
    print("Mobile Notification Sheet HTML added")

# 2.4 Update mobile fullscreen tabs to just "Donors" and "Recipients"
old_m_fs_tabs = '''    <div class="m-fs-tab-bar">
      <button class="m-fs-tab-btn active" id="mFsTabDonors" onclick="switchMobileFsTab('donors')">
        Donors (<span id="mFsDonorsCount">256</span>)
      </button>
      <button class="m-fs-tab-btn" id="mFsTabRecipients" onclick="switchMobileFsTab('recipients')">
        Recipients Who Want Blood (<span id="mFsRecipientsCount">64</span>)
      </button>
    </div>'''

new_m_fs_tabs = '''    <div class="m-fs-tab-bar">
      <button class="m-fs-tab-btn active" id="mFsTabDonors" onclick="switchMobileFsTab('donors')">
        Donors (<span id="mFsDonorsCount">0</span>)
      </button>
      <button class="m-fs-tab-btn" id="mFsTabRecipients" onclick="switchMobileFsTab('recipients')">
        Recipients (<span id="mFsRecipientsCount">0</span>)
      </button>
    </div>'''

if old_m_fs_tabs in m_html:
    m_html = m_html.replace(old_m_fs_tabs, new_m_fs_tabs, 1)
    print("Mobile fullscreen tab buttons updated")

with open(m_path, "w", encoding="utf-8") as f:
    f.write(m_html)

print("fix_mobile_and_desktop_web.py part 1 finished successfully")
