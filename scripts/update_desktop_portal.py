import os, re

path = r"C:\Users\PAUL\Documents\VitalSphere\public\index.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update CSS: Fix sticky th top: 76px -> top: 0, and add clean list, notification, and clearance console styles
old_th_css = '''.directory-table th {
      background: var(--slate-100);
      padding: 12px 14px;
      text-align: left;
      font-weight: 700;
      color: var(--navy-900);
      border-bottom: 1px solid var(--slate-200);
      position: sticky;
      top: 76px;
      z-index: 10;
    }'''

new_th_and_notif_css = '''.directory-table th {
      background: var(--slate-100);
      padding: 12px 14px;
      text-align: left;
      font-weight: 700;
      color: var(--navy-900);
      border-bottom: 1px solid var(--slate-200);
      position: sticky;
      top: 0; /* FIXED: top was 76px which floated down into content */
      z-index: 10;
    }

    /* CLEAN MODERN CARD ROW STYLING (Uncluttered, High Legibility) */
    .clean-list-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 16px 20px;
      background: white;
      border: 1px solid var(--slate-200);
      border-radius: 10px;
      margin-bottom: 10px;
      transition: all 0.15s ease;
      cursor: pointer;
    }

    .clean-list-item:hover {
      border-color: var(--red-600);
      box-shadow: 0 4px 14px rgba(220, 38, 38, 0.08);
      transform: translateY(-1px);
    }

    .clean-list-info {
      display: flex;
      align-items: center;
      gap: 16px;
      flex: 1;
    }

    .clean-reg-badge {
      font-family: var(--font-mono);
      font-weight: 700;
      font-size: 0.78rem;
      background: var(--slate-100);
      color: var(--navy-800);
      padding: 4px 8px;
      border-radius: 6px;
      border: 1px solid var(--slate-200);
    }

    .clean-name-title {
      font-size: 0.96rem;
      font-weight: 800;
      color: var(--navy-900);
      margin-bottom: 3px;
    }

    .clean-meta-sub {
      font-size: 0.78rem;
      color: var(--slate-500);
      display: flex;
      gap: 12px;
      align-items: center;
    }

    /* NOTIFICATION DROPDOWN PANEL */
    .notif-dropdown {
      position: absolute;
      top: 48px;
      right: 0;
      width: 400px;
      max-height: 520px;
      background: white;
      border: 1px solid var(--slate-200);
      border-radius: 14px;
      box-shadow: 0 20px 50px rgba(15, 23, 42, 0.22);
      z-index: 1000;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      animation: notifSlideDown 0.18s ease-out;
    }

    @keyframes notifSlideDown {
      from { opacity: 0; transform: translateY(-8px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .notif-header {
      padding: 14px 18px;
      background: var(--navy-950);
      color: white;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .notif-tabs {
      display: flex;
      background: var(--slate-100);
      border-bottom: 1px solid var(--slate-200);
      padding: 6px 12px;
      gap: 6px;
    }

    .notif-tab {
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 0.72rem;
      font-weight: 700;
      color: var(--slate-600);
      cursor: pointer;
      border: none;
      background: transparent;
      transition: all 0.12s;
    }

    .notif-tab.active {
      background: white;
      color: var(--navy-900);
      box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }

    .notif-list {
      flex: 1;
      overflow-y: auto;
      max-height: 380px;
    }

    .notif-item {
      padding: 12px 16px;
      display: flex;
      gap: 12px;
      align-items: flex-start;
      border-bottom: 1px solid var(--slate-100);
      transition: background 0.12s;
      cursor: pointer;
    }

    .notif-item:hover {
      background: var(--slate-50);
    }

    .notif-item.unread {
      background: #f0fdf4;
      border-left: 3.5px solid var(--emerald-600);
    }

    .notif-icon-bubble {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.9rem;
      flex-shrink: 0;
    }

    /* FULLSCREEN CANDIDATE CLEARANCE CONSOLE OVERLAY */
    .authority-fullscreen-overlay {
      position: fixed;
      inset: 0;
      background: #090e1a;
      z-index: 500;
      display: none;
      flex-direction: column;
      overflow-y: auto;
      color: white;
    }'''

if old_th_css in content:
    content = content.replace(old_th_css, new_th_and_notif_css, 1)
    print("CSS updated successfully")
else:
    print("Warning: old_th_css not found")

# 2. Update Navbar: Sign In / Sign Out button toggle and Notification Bell
old_nav_buttons = '''      <div style="display:flex; gap:10px;">
        <button class="btn btn-secondary" onclick="openFullscreenDirectory('donors')">View 256 Donors</button>
        <button class="btn btn-primary" onclick="openLoginModal()">Sign In</button>
      </div>'''

new_nav_buttons = '''      <div style="display:flex; gap:10px; align-items:center;" id="navAuthArea">
        <button class="btn btn-secondary" onclick="openFullscreenDirectory('donors')">View 256 Donors</button>
        
        <!-- Notification Bell (Available for logged-in & guest users) -->
        <div style="position:relative;">
          <button id="notifBellBtn" onclick="toggleNotificationPanel()" class="btn btn-secondary" style="padding:6px 12px; display:inline-flex; align-items:center; gap:6px; position:relative; background:white;" title="Notifications & Transfusion Alerts">
            <span style="font-size:1.05rem;">🔔</span>
            <span id="notifBadge" style="background:#dc2626; color:white; font-size:0.68rem; font-weight:800; border-radius:10px; padding:1px 6px; display:none;">0</span>
          </button>
          
          <!-- Notification Dropdown Panel -->
          <div id="notifDropdown" class="notif-dropdown" style="display:none;">
            <div class="notif-header">
              <div style="display:flex; align-items:center; gap:8px;">
                <span style="font-size:1.05rem;">🔔</span>
                <span style="font-weight:800; font-size:0.92rem;">Notification Center</span>
                <span id="notifUnreadPill" style="font-size:0.7rem; background:#dc2626; padding:2px 7px; border-radius:10px; font-weight:800;">3 Unread</span>
              </div>
              <button onclick="markAllNotificationsRead()" style="background:none; border:none; color:#38bdf8; font-size:0.75rem; font-weight:700; cursor:pointer;">Mark All Read</button>
            </div>
            <div class="notif-tabs">
              <button class="notif-tab active" onclick="switchNotifFilter('ALL', this)">All Updates</button>
              <button class="notif-tab" onclick="switchNotifFilter('DONATION', this)">Donations</button>
              <button class="notif-tab" onclick="switchNotifFilter('APPROVAL', this)">Approvals</button>
              <button class="notif-tab" onclick="switchNotifFilter('EMERGENCY', this)">Emergency</button>
            </div>
            <div class="notif-list" id="notifItemsContainer">
              <!-- Dynamically populated -->
            </div>
            <div style="padding:8px 14px; background:#f8fafc; border-top:1px solid #e2e8f0; font-size:0.72rem; color:#64748b; text-align:center;">
              Real-time sync with National Transfusion & Donor Network
            </div>
          </div>
        </div>

        <!-- Auth Toggle: When signed in shows user badge + Sign Out button, when logged out shows Sign In -->
        <div id="navUserBadge" style="display:none; align-items:center; gap:8px;">
          <div style="display:flex; flex-direction:column; align-items:flex-end;">
            <span id="navUserName" style="font-size:0.82rem; font-weight:800; color:var(--navy-900); max-width:140px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">User</span>
            <span id="navUserRole" style="font-size:0.68rem; font-weight:700; color:var(--emerald-600);">Active</span>
          </div>
          <button class="btn btn-secondary" onclick="executeSignOut()" style="color:#dc2626; border-color:#fca5a5; font-size:0.8rem; padding:6px 12px; font-weight:700;" title="Sign out of current account">Sign Out</button>
        </div>
        <button id="navSignInBtn" class="btn btn-primary" onclick="openLoginModal()">Sign In</button>
      </div>'''

if old_nav_buttons in content:
    content = content.replace(old_nav_buttons, new_nav_buttons, 1)
    print("Navbar buttons updated successfully")
else:
    print("Warning: old_nav_buttons not found")

# 3. Add more recipients to Keychain (Patient attendants)
old_keychain_recipients = '''            <div class="keychain-row" onclick="selectKeychainAccount('patient.tarun@vitalsphere.demo', 'Patient@2026', 'RECIPIENT')">
              <div class="account-avatar" style="background:#475569;">T</div>
              <div class="account-meta">
                <div class="acc-name">D. Tarun (Attendant)</div>
                <div class="acc-mail">patient.tarun@vitalsphere.demo</div>
              </div>
              <div class="account-badge-role" style="color:#94a3b8; background:rgba(148,163,184,0.1);">RECIPIENT</div>
            </div>'''

new_keychain_recipients = '''            <div style="padding:10px 14px 2px; font-size:0.68rem; font-weight:800; color:#38bdf8; text-transform:uppercase;">Patient Attendants / Recipients (5)</div>

            <div class="keychain-row" onclick="selectKeychainAccount('patient.tarun@vitalsphere.demo', 'Patient@2026', 'RECIPIENT')">
              <div class="account-avatar" style="background:#dc2626;">T</div>
              <div class="account-meta">
                <div class="acc-name">D. Tarun (Attendant - O- Patient)</div>
                <div class="acc-mail">patient.tarun@vitalsphere.demo</div>
              </div>
              <div class="account-badge-role" style="color:#f87171; background:rgba(220,38,38,0.15);">O- RECIPIENT</div>
            </div>

            <div class="keychain-row" onclick="selectKeychainAccount('patient.ramesh@vitalsphere.demo', 'Patient@2026', 'RECIPIENT')">
              <div class="account-avatar" style="background:#0284c7;">R</div>
              <div class="account-meta">
                <div class="acc-name">S. Ramesh (Attendant - B+ Patient)</div>
                <div class="acc-mail">patient.ramesh@vitalsphere.demo</div>
              </div>
              <div class="account-badge-role" style="color:#38bdf8; background:rgba(2,132,199,0.15);">B+ RECIPIENT</div>
            </div>

            <div class="keychain-row" onclick="selectKeychainAccount('patient.kavita@vitalsphere.demo', 'Patient@2026', 'RECIPIENT')">
              <div class="account-avatar" style="background:#d97706;">K</div>
              <div class="account-meta">
                <div class="acc-name">P. Kavita (Attendant - A- Critical ICU)</div>
                <div class="acc-mail">patient.kavita@vitalsphere.demo</div>
              </div>
              <div class="account-badge-role" style="color:#fbbf24; background:rgba(217,119,6,0.15);">A- CRITICAL</div>
            </div>

            <div class="keychain-row" onclick="selectKeychainAccount('patient.anjali@vitalsphere.demo', 'Patient@2026', 'RECIPIENT')">
              <div class="account-avatar" style="background:#8b5cf6;">A</div>
              <div class="account-meta">
                <div class="acc-name">V. Anjali (Attendant - AB- Surgery)</div>
                <div class="acc-mail">patient.anjali@vitalsphere.demo</div>
              </div>
              <div class="account-badge-role" style="color:#c084fc; background:rgba(139,92,246,0.15);">AB- RECIPIENT</div>
            </div>

            <div class="keychain-row" onclick="selectKeychainAccount('patient.suresh@vitalsphere.demo', 'Patient@2026', 'RECIPIENT')">
              <div class="account-avatar" style="background:#059669;">S</div>
              <div class="account-meta">
                <div class="acc-name">M. Suresh (Attendant - O+ Emergency)</div>
                <div class="acc-mail">patient.suresh@vitalsphere.demo</div>
              </div>
              <div class="account-badge-role" style="color:#34d399; background:rgba(5,150,105,0.15);">O+ RECIPIENT</div>
            </div>'''

if old_keychain_recipients in content:
    content = content.replace(old_keychain_recipients, new_keychain_recipients, 1)
    print("Keychain recipients updated successfully")
else:
    print("Warning: old_keychain_recipients not found")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("Part 1 finished successfully")
