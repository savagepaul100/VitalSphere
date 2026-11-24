import os, re

path = r"C:\Users\PAUL\Documents\VitalSphere\public\m\index.html"
with open(path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update stock-card click handlers in #inventory so clicking any group opens the Fullscreen Modal
for grp in ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"]:
    html = html.replace(f'onclick="filterDirectoryByGroup(\'{grp}\')"', f'onclick="openMobileFsDirectory(\'{grp}\')"')

# 2. Update .bottom-tab-bar CSS to floating pill style
old_tab_bar_css = '''.bottom-tab-bar {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      height: 64px;
      background: var(--navy-950);
      border-top: 1px solid rgba(255, 255, 255, 0.1);
      display: flex;
      justify-content: space-around;
      align-items: center;
      z-index: 1000;
      padding-bottom: env(safe-area-inset-bottom, 0px);
    }

    .tab-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      color: var(--slate-400);
      text-decoration: none;
      font-size: 0.65rem;
      font-weight: 700;
      gap: 3px;
      flex: 1;
      height: 100%;
    }

    .tab-item.active {
      color: var(--red-600);
    }

    .tab-icon {
      font-size: 1.2rem;
    }'''

new_tab_bar_css = '''.bottom-tab-bar {
      position: fixed;
      bottom: 16px;
      left: 50%;
      transform: translateX(-50%);
      width: calc(100% - 28px);
      max-width: 440px;
      height: 58px;
      background: rgba(10, 17, 32, 0.96);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.18);
      border-radius: 9999px;
      display: flex;
      justify-content: space-around;
      align-items: center;
      z-index: 1200;
      box-shadow: 0 12px 36px rgba(0, 0, 0, 0.45), 0 2px 10px rgba(0, 0, 0, 0.25);
      padding: 0 10px;
    }

    .tab-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      color: var(--slate-400);
      text-decoration: none;
      font-size: 0.62rem;
      font-weight: 700;
      gap: 2px;
      flex: 1;
      height: 100%;
      transition: color 0.15s ease;
      cursor: pointer;
    }

    .tab-item.active {
      color: #38bdf8;
    }

    .tab-icon {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 22px;
      height: 22px;
    }

    /* Fullscreen Mobile Directory Modal */
    .m-fs-modal {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: #f8fafc;
      z-index: 2500;
      display: none;
      flex-direction: column;
      overflow: hidden;
    }

    .m-fs-head {
      background: var(--navy-950);
      padding: 14px 18px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      display: flex;
      align-items: center;
      justify-content: space-between;
      color: white;
    }

    .m-group-pills-bar {
      display: flex;
      gap: 8px;
      padding: 10px 16px;
      background: white;
      border-bottom: 1px solid var(--slate-200);
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
      scrollbar-width: none;
    }
    .m-group-pills-bar::-webkit-scrollbar { display: none; }

    .m-grp-pill {
      padding: 5px 12px;
      border-radius: 20px;
      font-size: 0.78rem;
      font-weight: 800;
      border: 1px solid var(--slate-200);
      background: var(--slate-50);
      color: var(--navy-900);
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.15s ease;
    }
    .m-grp-pill.active {
      background: #dc2626;
      border-color: #dc2626;
      color: white;
    }

    .m-fs-tab-bar {
      display: flex;
      background: white;
      border-bottom: 1px solid var(--slate-200);
    }
    .m-fs-tab-btn {
      flex: 1;
      padding: 12px 10px;
      border: none;
      background: none;
      font-size: 0.82rem;
      font-weight: 800;
      color: var(--slate-500);
      border-bottom: 3px solid transparent;
      cursor: pointer;
      text-align: center;
    }
    .m-fs-tab-btn.active {
      color: #dc2626;
      border-bottom-color: #dc2626;
    }

    .m-clean-card {
      background: white;
      border: 1px solid var(--slate-200);
      border-radius: 10px;
      padding: 14px 16px;
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      cursor: pointer;
      box-shadow: 0 1px 3px rgba(0,0,0,0.04);
      transition: all 0.15s ease;
    }
    .m-clean-card:active {
      background: var(--slate-50);
      transform: scale(0.99);
    }'''

if old_tab_bar_css in html:
    html = html.replace(old_tab_bar_css, new_tab_bar_css, 1)
    print("Updated bottom tab bar CSS and added m-fs-modal styles")
else:
    print("Warning: old_tab_bar_css not found")

# 3. Replace bottom tab bar HTML with clean SVG icons (No emojis!)
old_bottom_tab_html = '''  <!-- Bottom Mobile Tab Bar -->
  <nav class="bottom-tab-bar">
    <a href="#home" class="tab-item active" onclick="setActiveTab(this)">
      <span class="tab-icon">🏠</span>
      <span>Home</span>
    </a>
    <a href="#inventory" class="tab-item" onclick="setActiveTab(this)">
      <span class="tab-icon">🩸</span>
      <span>Stock</span>
    </a>
    <a href="#register" class="tab-item" onclick="setActiveTab(this)">
      <span class="tab-icon">✍️</span>
      <span>Register</span>
    </a>
    <a href="#request" class="tab-item" onclick="setActiveTab(this)">
      <span class="tab-icon">🚨</span>
      <span>Emergency</span>
    </a>
    <a href="#directory" class="tab-item" onclick="setActiveTab(this)">
      <span class="tab-icon">👥</span>
      <span>Directory</span>
    </a>
  </nav>'''

new_bottom_tab_html = '''  <!-- Bottom Mobile Pill Tab Bar (Crisp Vector Icons, No Emojis) -->
  <nav class="bottom-tab-bar">
    <a href="#home" class="tab-item active" onclick="setActiveTab(this)">
      <span class="tab-icon">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
      </span>
      <span>Home</span>
    </a>
    <a href="#inventory" class="tab-item" onclick="setActiveTab(this)">
      <span class="tab-icon">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>
      </span>
      <span>Stock</span>
    </a>
    <a href="#register" class="tab-item" onclick="setActiveTab(this)">
      <span class="tab-icon">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
      </span>
      <span>Register</span>
    </a>
    <a href="#request" class="tab-item" onclick="setActiveTab(this)">
      <span class="tab-icon">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
      </span>
      <span>Emergency</span>
    </a>
    <div class="tab-item" onclick="openMobileFsDirectory(null)">
      <span class="tab-icon">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
      </span>
      <span>Directory</span>
    </div>
  </nav>'''

if old_bottom_tab_html in html:
    html = html.replace(old_bottom_tab_html, new_bottom_tab_html, 1)
    print("Replaced bottom tab bar HTML with vector icons pill")
else:
    print("Warning: old_bottom_tab_html not found")

# 4. Insert Fullscreen Mobile Directory Modal HTML and Drilldown Modal HTML
m_fs_modal_html = '''  <!-- FULLSCREEN MOBILE DIRECTORY MODAL (POPUP ON BLOOD GROUP CLICK) -->
  <div class="m-fs-modal" id="mFullscreenDirectoryModal">
    <!-- Top Bar -->
    <div class="m-fs-head">
      <div>
        <h2 style="font-size:1.15rem; font-weight:800; color:white; margin:0;" id="mFsModalTitle">Blood Directory</h2>
        <span style="font-size:0.72rem; color:#94a3b8;" id="mFsModalSubtitle">Verified Voluntary Donors & Active Patients</span>
      </div>
      <button onclick="closeMobileFsDirectory()" style="background:rgba(255,255,255,0.12); border:1px solid rgba(255,255,255,0.2); color:white; border-radius:8px; padding:6px 14px; font-weight:800; font-size:0.82rem; cursor:pointer;">
        ✕ Close
      </button>
    </div>

    <!-- Group Filter Pills (Horizontal Scroll) -->
    <div class="m-group-pills-bar" id="mGroupPillsContainer">
      <button class="m-grp-pill active" onclick="setMobileFsGroupFilter('ALL', this)">All Groups</button>
      <button class="m-grp-pill" onclick="setMobileFsGroupFilter('O-', this)">O-</button>
      <button class="m-grp-pill" onclick="setMobileFsGroupFilter('O+', this)">O+</button>
      <button class="m-grp-pill" onclick="setMobileFsGroupFilter('A-', this)">A-</button>
      <button class="m-grp-pill" onclick="setMobileFsGroupFilter('A+', this)">A+</button>
      <button class="m-grp-pill" onclick="setMobileFsGroupFilter('B-', this)">B-</button>
      <button class="m-grp-pill" onclick="setMobileFsGroupFilter('B+', this)">B+</button>
      <button class="m-grp-pill" onclick="setMobileFsGroupFilter('AB-', this)">AB-</button>
      <button class="m-grp-pill" onclick="setMobileFsGroupFilter('AB+', this)">AB+</button>
    </div>

    <!-- Tab Switcher: Donors vs Recipients -->
    <div class="m-fs-tab-bar">
      <button class="m-fs-tab-btn active" id="mFsTabDonors" onclick="switchMobileFsTab('donors')">
        Donors (<span id="mFsDonorsCount">256</span>)
      </button>
      <button class="m-fs-tab-btn" id="mFsTabRecipients" onclick="switchMobileFsTab('recipients')">
        Recipients Who Want Blood (<span id="mFsRecipientsCount">64</span>)
      </button>
    </div>

    <!-- Search Input -->
    <div style="padding:10px 16px; background:white; border-bottom:1px solid var(--slate-200);">
      <input type="text" id="mFsFilterInput" placeholder="Search by name, reg no, state or city..." style="width:100%; padding:9px 12px; border:1px solid var(--slate-200); border-radius:8px; font-size:0.82rem; box-sizing:border-box;" oninput="applyMobileFsFilter()" />
    </div>

    <!-- Clean List (Only Reg No, Name, Blood Group, Location/Urgency) -->
    <div style="flex:1; overflow-y:auto; padding:14px 16px 80px;" id="mFsDirectoryListContainer">
      <!-- Dynamically populated -->
    </div>
  </div>

  <!-- Mobile Detailed Info Drilldown Bottom Sheet / Modal -->
  <div class="sheet-overlay" id="mFsDetailModal" style="display:none; align-items:flex-end;">
    <div class="sheet-card" style="max-height:85vh; border-radius:16px 16px 0 0; padding:20px; overflow-y:auto;">
      <div class="sheet-head" style="margin-bottom:14px;">
        <div>
          <span style="font-size:0.68rem; font-weight:800; color:#dc2626; text-transform:uppercase;" id="mFsDetailCategory">Dossier File</span>
          <h3 style="font-size:1.15rem; font-weight:800; color:var(--navy-900); margin-top:2px;" id="mFsDetailTitle">Dossier Details</h3>
        </div>
        <button class="sheet-close" onclick="closeMobileFsDetail()">&times;</button>
      </div>

      <div id="mFsDetailBody" style="font-size:0.85rem;">
        <!-- Dynamically rendered -->
      </div>

      <div style="margin-top:16px; display:flex; gap:10px;" id="mFsDetailFooter">
        <!-- Dynamically rendered -->
      </div>
    </div>
  </div>
'''

if 'id="mFullscreenDirectoryModal"' not in html:
    html = html.replace('<!-- Bottom Mobile Pill Tab Bar', m_fs_modal_html + '\n  <!-- Bottom Mobile Pill Tab Bar', 1)
    print("Inserted mFullscreenDirectoryModal and mFsDetailModal HTML")

with open(path, "w", encoding="utf-8") as f:
    f.write(html)

print("HTML structure updated successfully")
