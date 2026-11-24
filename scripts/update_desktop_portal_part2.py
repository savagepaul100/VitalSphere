import os

path = r"C:\Users\PAUL\Documents\VitalSphere\public\index.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Replace #fullscreenDirectoryModal
old_fs_modal = '''  <!-- Fullscreen Modal for 256 Donors & 32 Recipients -->
  <div class="fullscreen-modal" id="fullscreenDirectoryModal">
    <div class="fullscreen-content">
      <div class="modal-nav">
        <div>
          <h2 style="font-size:1.35rem; font-weight:800; color:var(--navy-900);" id="fsModalHeading">Verified Blood Donors (256 Members)</h2>
          <p style="font-size:0.82rem; color:var(--slate-500);">Direct tele-coordination with verified healthy donors and active patient recipients.</p>
        </div>
        <div style="display:flex; align-items:center; gap:12px;">
          <button class="btn btn-secondary" onclick="openClinicalHelpModal()" style="font-size:0.78rem; padding:6px 12px; display:inline-flex; align-items:center; gap:6px;">
            <span style="font-weight:800; color:var(--red-600); background:var(--red-50); border-radius:50%; width:18px; height:18px; display:inline-flex; align-items:center; justify-content:center;">?</span>
            Clinical Status Guide (Hb / Rest)
          </button>
          <div class="tab-switch">
            <button class="tab-btn active" id="btnTabDonors" onclick="switchDirectoryTab('donors')">Donors (256 Members)</button>
            <button class="tab-btn" id="btnTabRecipients" onclick="switchDirectoryTab('recipients')">Recipients Who Want Blood (32 Patients)</button>
          </div>
          <button class="btn btn-secondary" onclick="closeFullscreenDirectory()" style="padding:6px 14px;">✕ Close</button>
        </div>
      </div>

      <div style="padding:16px 28px; background:var(--slate-50); border-bottom:1px solid var(--slate-200); display:flex; gap:16px; align-items:center;">
        <input type="text" id="directoryFilter" placeholder="Filter by name, state, city, or blood group..." style="padding:8px 14px; border:1px solid var(--slate-200); border-radius:6px; font-size:0.85rem; width:340px;" oninput="applyDirectoryFilter()" />
        <span id="directoryCountText" style="font-size:0.82rem; font-weight:700; color:var(--navy-800);">Showing 256 verified donors</span>
      </div>

      <div style="overflow-y:auto; flex:1; padding:0 28px 28px;">
        <table class="directory-table" id="directoryTable">
          <thead id="directoryTableHeader">
            <!-- Dynamically populated -->
          </thead>
          <tbody id="directoryTableBody">
            <!-- Dynamically populated -->
          </tbody>
        </table>
      </div>
    </div>
  </div>'''

new_fs_modal = '''  <!-- Fullscreen Modal for Verified Donors & Recipients (Clean, Modern Drilldown) -->
  <div class="fullscreen-modal" id="fullscreenDirectoryModal">
    <div class="fullscreen-content" style="max-width:1140px; margin:0 auto; min-height:88vh;">
      <div class="modal-nav">
        <div>
          <h2 style="font-size:1.35rem; font-weight:800; color:var(--navy-900);" id="fsModalHeading">Verified Blood Donors (256 Members)</h2>
          <p style="font-size:0.82rem; color:var(--slate-500);">Direct tele-coordination with verified healthy donors and active patient recipients.</p>
        </div>
        <div style="display:flex; align-items:center; gap:12px;">
          <button class="btn btn-secondary" onclick="openClinicalHelpModal()" style="font-size:0.78rem; padding:6px 12px; display:inline-flex; align-items:center; gap:6px;">
            <span style="font-weight:800; color:var(--red-600); background:var(--red-50); border-radius:50%; width:18px; height:18px; display:inline-flex; align-items:center; justify-content:center;">?</span>
            Clinical Status Guide (Hb / Rest)
          </button>
          <div class="tab-switch">
            <button class="tab-btn active" id="btnTabDonors" onclick="switchDirectoryTab('donors')">Donors (<span id="tabDonorsCount">256</span>)</button>
            <button class="tab-btn" id="btnTabRecipients" onclick="switchDirectoryTab('recipients')">Recipients Who Want Blood (<span id="tabRecipientsCount">64</span>)</button>
          </div>
          <button class="btn btn-secondary" onclick="closeFullscreenDirectory()" style="padding:6px 14px;">✕ Close</button>
        </div>
      </div>

      <!-- Filter Controls with Clear Spacing -->
      <div style="padding:14px 28px; background:var(--slate-50); border-bottom:1px solid var(--slate-200); display:flex; gap:16px; align-items:center; justify-content:space-between;">
        <input type="text" id="directoryFilter" placeholder="Filter by name, registration no, state, city, or blood group..." style="padding:8px 14px; border:1px solid var(--slate-200); border-radius:6px; font-size:0.85rem; width:380px;" oninput="applyDirectoryFilter()" />
        <span id="directoryCountText" style="font-size:0.82rem; font-weight:700; color:var(--navy-800);">Showing 256 verified donors</span>
      </div>

      <!-- Clean Card List (NO overlapping table header bugs; first item is 100% visible) -->
      <div style="overflow-y:auto; flex:1; padding:20px 28px;" id="directoryListContainer">
        <!-- Rendered dynamically -->
      </div>
    </div>
  </div>

  <!-- Detail Drilldown Modal for Donors & Patients -->
  <div class="fullscreen-modal" id="fsDetailModal" style="display:none; align-items:center; justify-content:center; z-index:1200;">
    <div style="background:white; border-radius:14px; width:92%; max-width:660px; max-height:88vh; display:flex; flex-direction:column; box-shadow:0 25px 60px rgba(15,23,42,0.35); border:1px solid var(--slate-200); overflow:hidden;">
      <div class="modal-nav" style="padding:16px 22px; border-bottom:1px solid var(--slate-200); display:flex; justify-content:space-between; align-items:center;">
        <div>
          <span id="detailModalCategory" style="font-size:0.7rem; font-weight:800; color:var(--red-600); text-transform:uppercase;">Credential File</span>
          <h3 style="font-size:1.2rem; font-weight:800; color:var(--navy-900);" id="detailModalTitle">Full Profile & Details</h3>
        </div>
        <button class="btn btn-secondary" onclick="closeFsDetailModal()" style="padding:6px 14px;">✕ Close</button>
      </div>

      <div style="flex:1; overflow-y:auto; padding:24px; background:var(--slate-50);" id="detailModalBody">
        <!-- Rendered dynamically -->
      </div>

      <div style="padding:14px 22px; background:white; border-top:1px solid var(--slate-200); display:flex; justify-content:space-between; align-items:center;" id="detailModalFooter">
        <!-- Rendered dynamically -->
      </div>
    </div>
  </div>'''

if old_fs_modal in content:
    content = content.replace(old_fs_modal, new_fs_modal, 1)
    print("Fullscreen directory modal updated successfully")
else:
    print("Warning: old_fs_modal not found")

# 2. Replace #authorityReviewModal
old_auth_modal = '''  <!-- Authority Review Desk Modal -->
  <div class="fullscreen-modal" id="authorityReviewModal" style="display:none;">
    <div class="fullscreen-content" style="max-width:880px; max-height:85vh; margin:auto; border-radius:12px;">
      <div class="modal-nav">
        <div>
          <h2 style="font-size:1.35rem; font-weight:800; color:var(--navy-900);">Medical Officer Verification Desk</h2>
          <p style="font-size:0.82rem; color:var(--slate-500);">Review voluntary donor registrations, verify uploaded medical certificates, and clear donors for donation.</p>
        </div>
        <button class="btn btn-secondary" onclick="closeAuthorityReviewModal()" style="padding:6px 14px;">✕ Close</button>
      </div>

      <div style="padding:16px 28px; background:var(--slate-50); border-bottom:1px solid var(--slate-200); display:flex; justify-content:space-between; align-items:center;">
        <span id="pendingBadgeText" style="font-size:0.84rem; font-weight:700; color:var(--amber-600);">5 Registrations Awaiting Verification</span>
        <span style="font-size:0.75rem; color:var(--slate-500);">Statutory NBTC Medical Officer Standards</span>
      </div>

      <div style="overflow-y:auto; flex:1; padding:20px 28px;" id="desktopPendingListContainer">
        <!-- Rendered via JS -->
      </div>
    </div>
  </div>'''

new_auth_modal = '''  <!-- Fullscreen Authority Review Console (100% Fullscreen, Optimized Workspace) -->
  <div class="authority-fullscreen-overlay" id="authorityReviewModal">
    <!-- View 1: Main Candidates Roster -->
    <div id="authRosterView" style="display:flex; flex-direction:column; height:100vh;">
      <div style="padding:16px 32px; background:var(--navy-950); border-bottom:1px solid rgba(255,255,255,0.1); display:flex; justify-content:space-between; align-items:center;">
        <div style="display:flex; align-items:center; gap:14px;">
          <div style="width:38px; height:38px; background:#dc2626; border-radius:8px; display:flex; align-items:center; justify-content:center;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="white"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>
          </div>
          <div>
            <h2 style="font-size:1.25rem; font-weight:800; color:white;">Medical Officer Clearance Console</h2>
            <p style="font-size:0.76rem; color:#94a3b8;">Review voluntary donor registrations, verify uploaded medical fitness certificates, and clear candidates.</p>
          </div>
        </div>
        <div style="display:flex; align-items:center; gap:14px;">
          <span style="background:rgba(217,119,6,0.18); border:1px solid rgba(217,119,6,0.4); color:#fbbf24; font-size:0.75rem; font-weight:800; padding:6px 14px; border-radius:20px;" id="authPendingBadge">
            5 Registrations Awaiting Verification
          </span>
          <button class="btn btn-secondary" onclick="closeAuthorityReviewModal()" style="padding:6px 16px; background:rgba(255,255,255,0.08); border-color:rgba(255,255,255,0.15); color:white;">✕ Exit Console</button>
        </div>
      </div>

      <div style="padding:12px 32px; background:#0f172a; border-bottom:1px solid #1e293b; display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:0.8rem; color:#cbd5e1; font-weight:600;">Candidates Roster • Statutory NBTC Medical Officer Standards</span>
        <span style="font-size:0.74rem; color:#38bdf8;">Click any candidate to open full-screen clinical clearance and approval console</span>
      </div>

      <!-- Main Clean Candidate List (Showing ONLY Names, Reg No, Blood Group, State & City) -->
      <div style="flex:1; overflow-y:auto; padding:24px 32px;" id="authCandidateListContainer">
        <!-- Rendered dynamically via renderDesktopPendingList() -->
      </div>
    </div>

    <!-- View 2: Dedicated Fullscreen Candidate Clearance Console -->
    <div id="authCandidateConsoleView" style="display:none; flex-direction:column; height:100vh;">
      <div style="padding:14px 32px; background:var(--navy-950); border-bottom:1px solid rgba(255,255,255,0.1); display:flex; justify-content:space-between; align-items:center;">
        <button class="btn btn-secondary" onclick="closeCandidateConsoleView()" style="background:rgba(255,255,255,0.08); border-color:rgba(255,255,255,0.15); color:white; font-size:0.8rem; padding:6px 14px;">
          ← Back to Candidates Roster
        </button>
        <div style="text-align:center;">
          <span style="font-size:0.68rem; font-weight:800; color:#38bdf8; text-transform:uppercase;">Official Clinical Clearance Workspace</span>
          <h2 style="font-size:1.18rem; font-weight:800; color:white;" id="consoleCandidateHeading">Candidate Clearance Dossier</h2>
        </div>
        <span id="consoleStatusBadge" style="background:rgba(217,119,6,0.2); color:#fbbf24; border:1px solid #d97706; padding:5px 12px; border-radius:6px; font-size:0.75rem; font-weight:700;">WAITING FOR CLEARANCE</span>
      </div>

      <div style="flex:1; overflow-y:auto; padding:28px 32px; background:#0b1120;" id="consoleCandidateBody">
        <!-- Rendered dynamically -->
      </div>

      <!-- Action Bar (ONLY in this full screen view show approve / deny) -->
      <div style="padding:16px 32px; background:#0f172a; border-top:1px solid #1e293b; display:flex; justify-content:space-between; align-items:center;" id="consoleActionBar">
        <span style="font-size:0.75rem; color:#94a3b8;">NBTC Statutory Compliance Verified • Clearance is permanent until next donation</span>
        <div style="display:flex; gap:12px;" id="consoleActionButtons">
          <button class="btn btn-secondary" onclick="deferFromCandidateConsole()" style="background:#450a0a; border-color:#991b1b; color:#fca5a5; font-size:0.85rem; padding:8px 20px; font-weight:700;">
            ✕ Decline / 90-Day Deferral
          </button>
          <button class="btn btn-primary" onclick="approveFromCandidateConsole()" style="background:#059669; border-color:#059669; font-size:0.85rem; padding:8px 24px; font-weight:800;">
            ✓ Approve & Grant Clearance
          </button>
        </div>
      </div>
    </div>
  </div>'''

if old_auth_modal in content:
    content = content.replace(old_auth_modal, new_auth_modal, 1)
    print("Authority review modal updated successfully")
else:
    print("Warning: old_auth_modal not found")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("Part 2 finished successfully")
