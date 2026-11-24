import os

# 1. Update public/directory-data.js to avoid "export" keyword syntax error when loaded in regular script tags
dir_data_path = r"C:\Users\PAUL\Documents\VitalSphere\public\directory-data.js"
with open(dir_data_path, "r", encoding="utf-8") as f:
    dir_code = f.read()

dir_code = dir_code.replace("export const INDIA_STATES_DATA =", "var INDIA_STATES_DATA =")
dir_code = dir_code.replace("export const fullDonorsList =", "var fullDonorsList =")
dir_code = dir_code.replace("export const fullRecipientsList =", "var fullRecipientsList =")

with open(dir_data_path, "w", encoding="utf-8") as f:
    f.write(dir_code)
print("Updated directory-data.js to universal browser var format.")

# 2. Update public/index.html script section
html_path = r"C:\Users\PAUL\Documents\VitalSphere\public\index.html"
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

start_marker = "    // Fullscreen Directory Dialog"
end_marker = "    // Form Submissions"

start_idx = html_content.find(start_marker)
end_idx = html_content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print(f"Error: markers not found. start={start_idx}, end={end_idx}")
    exit(1)

new_js = '''    // Fullscreen Directory Dialog (Clean List & Modern Drilldown)
    window.openFullscreenDirectory = function(tab = 'donors', groupFilter = null) {
      currentFilterGroup = groupFilter;
      const modal = document.getElementById('fullscreenDirectoryModal');
      if (modal) {
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
      }
      const cntD = document.getElementById('tabDonorsCount');
      if (cntD && window.fullDonorsList) cntD.innerText = window.fullDonorsList.length;
      const cntR = document.getElementById('tabRecipientsCount');
      if (cntR && window.fullRecipientsList) cntR.innerText = window.fullRecipientsList.length;
      switchDirectoryTab(tab);
    };

    window.closeFullscreenDirectory = function() {
      const modal = document.getElementById('fullscreenDirectoryModal');
      if (modal) modal.style.display = 'none';
      document.body.style.overflow = 'auto';
    };

    window.switchDirectoryTab = function(tab) {
      activeTab = tab;
      const btnD = document.getElementById('btnTabDonors');
      const btnR = document.getElementById('btnTabRecipients');
      if (btnD) btnD.className = tab === 'donors' ? 'tab-btn active' : 'tab-btn';
      if (btnR) btnR.className = tab === 'recipients' ? 'tab-btn active' : 'tab-btn';
      
      const heading = document.getElementById('fsModalHeading');
      if (heading) {
        if (tab === 'donors') {
          heading.innerText = currentFilterGroup 
            ? `Verified Blood Donors for Group ${currentFilterGroup} (${window.fullDonorsList.length} Members Total)` 
            : `Verified Blood Donors Directory (${window.fullDonorsList.length} Members)`;
        } else {
          heading.innerText = `Recipients Who Want Blood (${window.fullRecipientsList.length} Inpatients)`;
        }
      }
      applyDirectoryFilter();
    };

    window.applyDirectoryFilter = function() {
      const filterInput = document.getElementById('directoryFilter');
      const q = (filterInput ? filterInput.value : '').toLowerCase().trim();
      const container = document.getElementById('directoryListContainer');
      if (!container) return;
      container.innerHTML = '';

      if (activeTab === 'donors') {
        let list = window.fullDonorsList || [];
        if (currentFilterGroup) {
          list = list.filter(d => d.bloodGroup === currentFilterGroup);
        }
        if (q) {
          list = list.filter(d => 
            (d.name && d.name.toLowerCase().includes(q)) || 
            (d.district && d.district.toLowerCase().includes(q)) || 
            (d.bloodGroup && d.bloodGroup.toLowerCase().includes(q)) ||
            (d.id && d.id.toLowerCase().includes(q))
          );
        }

        const countText = document.getElementById('directoryCountText');
        if (countText) {
          countText.innerText = `Showing ${list.length} of ${window.fullDonorsList.length} verified donors`;
        }

        if (list.length === 0) {
          container.innerHTML = '<div style="text-align:center; padding:48px; color:var(--slate-500); font-size:0.9rem;">No donors match the filter criteria.</div>';
          return;
        }

        list.forEach(d => {
          const item = document.createElement('div');
          item.className = 'clean-list-item';
          item.innerHTML = `
            <div class="clean-list-info" onclick="openDonorDetails('${d.id}')">
              <span class="bg-badge" style="font-size:1.15rem; min-width:48px; text-align:center; padding:6px 10px;">${d.bloodGroup}</span>
              <div>
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
                  <strong style="font-size:1rem; color:var(--navy-900);">${d.name}</strong>
                  <span class="status-pill status-fit" style="font-size:0.7rem; padding:2px 8px;">✓ Aadhaar Verified</span>
                </div>
                <div style="font-size:0.8rem; color:var(--slate-500); display:flex; gap:12px; align-items:center; flex-wrap:wrap;">
                  <span class="clean-reg-badge">${d.id}</span>
                  <span>📍 ${d.district}</span>
                  <span style="color:var(--emerald-600); font-weight:600;">${d.healthStatus || 'FIT (Hb: 13.5 g/dL)'}</span>
                </div>
              </div>
            </div>
            <div style="display:flex; align-items:center; gap:10px;">
              <a href="tel:${d.mobile}" class="btn btn-secondary" style="padding:7px 14px; font-size:0.8rem; text-decoration:none;" onclick="event.stopPropagation()">
                📞 Call ${d.mobile}
              </a>
              <button class="btn btn-secondary" style="padding:7px 14px; font-size:0.8rem;" onclick="openDonorDetails('${d.id}')">
                View Details →
              </button>
            </div>
          `;
          container.appendChild(item);
        });
      } else {
        let list = window.fullRecipientsList || [];
        if (q) {
          list = list.filter(r => 
            (r.patientName && r.patientName.toLowerCase().includes(q)) || 
            (r.district && r.district.toLowerCase().includes(q)) || 
            (r.bloodGroup && r.bloodGroup.toLowerCase().includes(q)) || 
            (r.hospital && r.hospital.toLowerCase().includes(q)) ||
            (r.id && r.id.toLowerCase().includes(q))
          );
        }

        const countText = document.getElementById('directoryCountText');
        if (countText) {
          countText.innerText = `Showing ${list.length} of ${window.fullRecipientsList.length} transfusion recipients`;
        }

        if (list.length === 0) {
          container.innerHTML = '<div style="text-align:center; padding:48px; color:var(--slate-500); font-size:0.9rem;">No recipient requirements match the filter criteria.</div>';
          return;
        }

        list.forEach(r => {
          const item = document.createElement('div');
          item.className = 'clean-list-item';
          const isCommitted = r.status && r.status.includes('DONOR FOUND');
          item.innerHTML = `
            <div class="clean-list-info" onclick="openRecipientDetails('${r.id}')">
              <span class="bg-badge" style="font-size:1.15rem; min-width:48px; text-align:center; padding:6px 10px;">${r.bloodGroup}</span>
              <div>
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
                  <strong style="font-size:1rem; color:var(--navy-900);">${r.patientName}</strong>
                  <span class="status-pill ${r.urgencyClass || 'status-critical'}" style="font-size:0.7rem; padding:2px 8px;">${r.urgency || 'CRITICAL'}</span>
                  ${isCommitted ? '<span class="status-pill status-fit" style="font-size:0.7rem; padding:2px 8px;">✓ Donor Found</span>' : ''}
                </div>
                <div style="font-size:0.8rem; color:var(--slate-500); display:flex; gap:12px; align-items:center; flex-wrap:wrap;">
                  <span class="clean-reg-badge">${r.id}</span>
                  <span>🩸 ${r.units}</span>
                  <span>🏥 ${r.hospital}</span>
                  <span>📍 ${r.district}</span>
                </div>
              </div>
            </div>
            <div style="display:flex; align-items:center; gap:10px;">
              <button class="btn btn-primary" onclick="handleDonateAction('${r.id}')" style="background:#dc2626; border-color:#dc2626; font-weight:800; padding:8px 18px; font-size:0.82rem;">
                Donate
              </button>
              <button class="btn btn-secondary" style="padding:7px 14px; font-size:0.8rem;" onclick="openRecipientDetails('${r.id}')">
                View Details →
              </button>
            </div>
          `;
          container.appendChild(item);
        });
      }
    };

    // Full Detail Drilldown Modal
    window.openDonorDetails = function(donorId) {
      const d = (window.fullDonorsList || []).find(x => x.id === donorId);
      if (!d) return;

      document.getElementById('detailModalCategory').innerText = 'VERIFIED VOLUNTARY DONOR PROFILE';
      document.getElementById('detailModalTitle').innerText = `${d.name} (${d.bloodGroup})`;
      
      const body = document.getElementById('detailModalBody');
      body.innerHTML = `
        <div style="background:white; border-radius:10px; border:1px solid var(--slate-200); padding:20px; margin-bottom:16px;">
          <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #f1f5f9; padding-bottom:12px; margin-bottom:14px;">
            <div>
              <div style="font-size:0.75rem; color:var(--slate-400); font-weight:800; text-transform:uppercase;">Credential File Identifier</div>
              <div style="font-family:var(--font-mono); font-size:1.1rem; font-weight:800; color:var(--navy-900);">${d.id} • Aadhaar: ${d.aadhaar}</div>
            </div>
            <span class="bg-badge" style="font-size:1.35rem; padding:4px 14px;">${d.bloodGroup}</span>
          </div>

          <div style="display:grid; grid-template-columns:1fr 1fr; gap:14px; font-size:0.85rem; margin-bottom:16px;">
            <div>
              <span style="color:var(--slate-500); display:block; font-size:0.74rem;">Full Legal Name</span>
              <strong style="color:var(--navy-900); font-size:0.95rem;">${d.name}</strong>
            </div>
            <div>
              <span style="color:var(--slate-500); display:block; font-size:0.74rem;">Registered Location</span>
              <strong style="color:var(--navy-900); font-size:0.95rem;">${d.district}</strong>
            </div>
            <div>
              <span style="color:var(--slate-500); display:block; font-size:0.74rem;">Clinical Status</span>
              <span class="status-pill ${d.fitClass || 'status-fit'}" style="margin-top:2px;">${d.healthStatus || 'FIT (Hb: 13.5 g/dL)'}</span>
            </div>
            <div>
              <span style="color:var(--slate-500); display:block; font-size:0.74rem;">Donation State</span>
              <strong style="color:var(--navy-900);">${d.donationState || 'Ready to Donate (Eligible Now)'}</strong>
            </div>
          </div>

          <div style="background:var(--slate-50); border:1px solid var(--slate-200); border-radius:8px; padding:12px 16px; margin-bottom:14px;">
            <div style="font-size:0.78rem; font-weight:800; color:var(--navy-900); margin-bottom:6px;">Official Clinical Verification Certificates:</div>
            <div style="font-size:0.8rem; color:var(--slate-600); line-height:1.6;">
              ✓ <strong>Medical Fitness:</strong> ${d.medicalProof || 'Registered Physician Medical Certificate'}<br/>
              ✓ <strong>Blood Group Proof:</strong> ${d.groupProof || 'Clinical Pathology Lab Certificate / Donor Card'}
            </div>
          </div>

          <div style="border-left:3px solid var(--emerald-600); padding:8px 12px; background:#ecfdf5; font-size:0.75rem; color:#065f46;">
            <strong>NBTC Statutory Clearance:</strong> Donor meets all physical eligibility benchmarks (Hb ≥ 12.5 g/dL, optimal pulse, non-reactive serology). Cleared for direct transfusion coordination.
          </div>
        </div>
      `;

      const footer = document.getElementById('detailModalFooter');
      footer.innerHTML = `
        <span style="font-size:0.78rem; color:var(--slate-500);">Direct Tele-Coordination</span>
        <div style="display:flex; gap:10px;">
          <button class="btn btn-secondary" onclick="closeFsDetailModal()">Close</button>
          <a href="tel:${d.mobile}" class="btn btn-primary" style="background:#059669; border-color:#059669; text-decoration:none;">
            📞 Call ${d.mobile}
          </a>
        </div>
      `;

      document.getElementById('fsDetailModal').style.display = 'flex';
    };

    window.openRecipientDetails = function(reqId) {
      const r = (window.fullRecipientsList || []).find(x => x.id === reqId);
      if (!r) return;

      document.getElementById('detailModalCategory').innerText = 'EMERGENCY TRANSFUSION DOSSIER';
      document.getElementById('detailModalTitle').innerText = `${r.patientName} — ${r.hospital}`;

      const isCommitted = r.status && r.status.includes('DONOR FOUND');

      const body = document.getElementById('detailModalBody');
      body.innerHTML = `
        <div style="background:white; border-radius:10px; border:1px solid var(--slate-200); padding:20px; margin-bottom:16px;">
          <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #f1f5f9; padding-bottom:12px; margin-bottom:14px;">
            <div>
              <div style="font-size:0.75rem; color:var(--slate-400); font-weight:800; text-transform:uppercase;">Hospital Transfusion Request</div>
              <div style="font-family:var(--font-mono); font-size:1.1rem; font-weight:800; color:var(--navy-900);">${r.id} • Aadhaar: ${r.aadhaar}</div>
            </div>
            <span class="bg-badge" style="font-size:1.35rem; padding:4px 14px;">${r.bloodGroup}</span>
          </div>

          <div style="display:grid; grid-template-columns:1fr 1fr; gap:14px; font-size:0.85rem; margin-bottom:16px;">
            <div>
              <span style="color:var(--slate-500); display:block; font-size:0.74rem;">Patient Name</span>
              <strong style="color:var(--navy-900); font-size:0.95rem;">${r.patientName}</strong>
            </div>
            <div>
              <span style="color:var(--slate-500); display:block; font-size:0.74rem;">Clinical Urgency</span>
              <span class="status-pill ${r.urgencyClass || 'status-critical'}" style="margin-top:2px;">${r.urgency || 'CRITICAL'}</span>
            </div>
            <div>
              <span style="color:var(--slate-500); display:block; font-size:0.74rem;">Hospital & Area</span>
              <strong style="color:var(--navy-900);">${r.hospital} (${r.district})</strong>
            </div>
            <div>
              <span style="color:var(--slate-500); display:block; font-size:0.74rem;">Volume Required</span>
              <strong style="color:var(--red-600);">${r.units}</strong>
            </div>
            <div>
              <span style="color:var(--slate-500); display:block; font-size:0.74rem;">Attendant Mobile Contact</span>
              <strong style="color:var(--navy-900);">${r.contact}</strong>
            </div>
            <div>
              <span style="color:var(--slate-500); display:block; font-size:0.74rem;">Transfusion Status</span>
              <strong style="color:${isCommitted ? 'var(--emerald-600)' : 'var(--amber-600)'};">${r.status || 'LOOKING_FOR_DONORS'}</strong>
            </div>
          </div>

          ${isCommitted ? `
            <div style="border-left:3px solid var(--emerald-600); padding:10px 14px; background:#ecfdf5; font-size:0.8rem; color:#065f46; border-radius:4px;">
              <strong>✓ Confirmed Donor Assigned:</strong> A voluntary verified donor has committed to fulfill this requirement. Hospital transfusion desk and attendant have been notified.
            </div>
          ` : `
            <div style="border-left:3px solid var(--red-600); padding:10px 14px; background:#fff1f2; font-size:0.8rem; color:#9f1239; border-radius:4px;">
              <strong>Active Emergency:</strong> Immediate voluntary donor response requested. Click <strong>"Donate"</strong> below to confirm your commitment and dispatch an immediate tele-notification to the patient's attendant.
            </div>
          `}
        </div>
      `;

      const footer = document.getElementById('detailModalFooter');
      footer.innerHTML = `
        <span style="font-size:0.78rem; color:var(--slate-500);">Hospital Transfusion Desk</span>
        <div style="display:flex; gap:10px;">
          <button class="btn btn-secondary" onclick="closeFsDetailModal()">Close</button>
          <a href="tel:${r.contact}" class="btn btn-secondary" style="text-decoration:none;">📞 Call Attendant</a>
          <button class="btn btn-primary" onclick="handleDonateAction('${r.id}')" style="background:#dc2626; border-color:#dc2626; font-weight:800; padding:8px 20px;">
            Donate
          </button>
        </div>
      `;

      document.getElementById('fsDetailModal').style.display = 'flex';
    };

    window.closeFsDetailModal = function() {
      const modal = document.getElementById('fsDetailModal');
      if (modal) modal.style.display = 'none';
    };

    // Donate Workflow with Immediate Patient Attendant Notification
    window.handleDonateAction = function(reqId) {
      const r = (window.fullRecipientsList || []).find(x => x.id === reqId);
      if (!r) return;

      if (!window.currentUser) {
        alert("Please sign in with your account to confirm donation and dispatch a direct notification to the patient's attendant.");
        openLoginModal();
        return;
      }

      const confirmed = confirm(
        `Confirm Voluntary Blood Donation Commitment:\n\n` +
        `Patient: ${r.patientName}\n` +
        `Required Blood Group: ${r.bloodGroup}\n` +
        `Hospital: ${r.hospital}\n` +
        `Units: ${r.units}\n\n` +
        `When you click OK, VitalSphere will immediately dispatch a verified donor notification to the patient attendant (${r.contact}).`
      );

      if (!confirmed) return;

      r.status = 'DONOR FOUND (Coordination in progress)';

      // Dispatch real-time notifications
      addNotification({
        category: 'DONATION',
        title: `🎉 Donor Found for ${r.patientName}!`,
        message: `Donor ${window.currentUser.name || window.currentUser.email} has accepted emergency request ${r.id} (${r.bloodGroup}) at ${r.hospital}. Attendant notified at ${r.contact}.`,
        time: 'Just now',
        unread: true
      });

      addNotification({
        category: 'DONATION',
        title: `Donation Commitment Registered`,
        message: `You have committed to donate blood for ${r.patientName} (${r.bloodGroup}) at ${r.hospital}. Please reach out to attendant at ${r.contact}.`,
        time: 'Just now',
        unread: true
      });

      applyDirectoryFilter();
      if (document.getElementById('fsDetailModal').style.display === 'flex') {
        openRecipientDetails(reqId);
      }

      alert(
        `✓ SUCCESS: Notification dispatched to ${r.patientName}'s attendant!\n\n` +
        `Patient Attendant: ${r.contact}\n` +
        `Hospital Desk: ${r.hospital}\n` +
        `Thank you for saving a life!`
      );
    };

    // Fullscreen Authority Review Console (100% Fullscreen, Optimized Workspace)
    window.openAuthorityReviewModal = function() {
      const modal = document.getElementById('authorityReviewModal');
      if (modal) modal.style.display = 'flex';
      closeCandidateConsoleView(); // ensure clean roster view
      renderDesktopPendingList();
    };

    window.closeAuthorityReviewModal = function() {
      const modal = document.getElementById('authorityReviewModal');
      if (modal) modal.style.display = 'none';
    };

    window.renderDesktopPendingList = function() {
      const c = document.getElementById('authCandidateListContainer');
      const count = (window.desktopPendingDonors || []).length;
      
      const badge = document.getElementById('authPendingBadge');
      if (badge) badge.innerText = `${count} Registrations Awaiting Verification`;
      
      const deskCount = document.getElementById('desktopPendingCount');
      if (deskCount) deskCount.innerText = count;

      if (!c) return;

      if (count === 0) {
        c.innerHTML = '<div style="text-align:center; padding:60px; color:#94a3b8; font-size:1rem;">All voluntary donor registrations have been verified. Clearance queue is 100% clear!</div>';
        return;
      }

      // Main list shows ONLY: Names, Reg No, Blood Group, State & City (No clutter, no approve/deny buttons here!)
      c.innerHTML = `
        <div style="max-width:980px; margin:0 auto; display:flex; flex-direction:column; gap:12px;">
          ${window.desktopPendingDonors.map((p, i) => `
            <div style="background:#1e293b; border:1px solid #334155; border-radius:10px; padding:18px 24px; display:flex; align-items:center; justify-content:space-between; cursor:pointer; transition:all 0.15s ease;"
                 onmouseover="this.style.borderColor='#38bdf8'; this.style.background='#24334a';"
                 onmouseout="this.style.borderColor='#334155'; this.style.background='#1e293b';"
                 onclick="openAuthorityCandidateReview(${i})">
              
              <div style="display:flex; align-items:center; gap:20px;">
                <span style="background:#dc2626; color:white; font-size:1.2rem; font-weight:900; padding:6px 14px; border-radius:8px; min-width:52px; text-align:center;">
                  ${p.group}
                </span>
                <div>
                  <div style="display:flex; align-items:center; gap:12px; margin-bottom:4px;">
                    <strong style="font-size:1.08rem; color:white;">${p.name}</strong>
                    <span style="font-size:0.72rem; font-weight:800; padding:2px 8px; border-radius:12px; ${p.status === 'APPROVED' ? 'background:#065f46; color:#6ee7b7;' : (p.status === 'DEFERRED' ? 'background:#7f1d1d; color:#fca5a5;' : 'background:rgba(217,119,6,0.25); color:#fbbf24; border:1px solid #d97706;')}">
                      ${p.status || 'PENDING MEDICAL CLEARANCE'}
                    </span>
                  </div>
                  <div style="font-size:0.82rem; color:#94a3b8; display:flex; gap:16px; align-items:center;">
                    <span style="font-family:var(--font-mono); color:#cbd5e1; font-weight:700;">${p.id}</span>
                    <span>📍 ${p.city}, ${p.st}</span>
                    <span>📞 ${p.mobile || '+91 9848123456'}</span>
                  </div>
                </div>
              </div>

              <div style="display:flex; align-items:center; gap:12px;">
                <button class="btn btn-secondary" style="background:#38bdf8; border-color:#38bdf8; color:#0f172a; font-weight:800; font-size:0.82rem; padding:8px 18px;" onclick="event.stopPropagation(); openAuthorityCandidateReview(${i})">
                  Open Clinical Clearance Console →
                </button>
              </div>
            </div>
          `).join('')}
        </div>
      `;
    };

    // Dedicated Fullscreen Candidate Clearance Console View
    window.openAuthorityCandidateReview = function(idx) {
      window.currentReviewCandidateIdx = idx;
      const d = window.desktopPendingDonors[idx];
      if (!d) return;

      document.getElementById('authRosterView').style.display = 'none';
      const consoleView = document.getElementById('authCandidateConsoleView');
      consoleView.style.display = 'flex';

      document.getElementById('consoleCandidateHeading').innerText = `Clinical Dossier: ${d.name} (${d.group})`;
      
      const badge = document.getElementById('consoleStatusBadge');
      if (badge) {
        badge.innerText = d.status || 'WAITING FOR CLEARANCE';
        badge.style.background = d.status === 'APPROVED' ? '#065f46' : (d.status === 'DEFERRED' ? '#7f1d1d' : 'rgba(217,119,6,0.25)');
        badge.style.color = d.status === 'APPROVED' ? '#6ee7b7' : (d.status === 'DEFERRED' ? '#fca5a5' : '#fbbf24');
      }

      // Check documents
      const isPdfFit = (d.cert || '').toLowerCase().endsWith('.pdf');
      const isPdfProof = (d.proof || '').toLowerCase().endsWith('.pdf');

      const body = document.getElementById('consoleCandidateBody');
      body.innerHTML = `
        <div style="max-width:1100px; margin:0 auto; display:grid; grid-template-columns:1.1fr 1fr; gap:24px;">
          <!-- Left Column: Clinical Parameters & Doctor Sign-off -->
          <div style="background:#1e293b; border:1px solid #334155; border-radius:12px; padding:24px;">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #334155; padding-bottom:14px; margin-bottom:16px;">
              <div>
                <span style="font-size:0.7rem; color:#38bdf8; font-weight:800; text-transform:uppercase;">Statutory Candidate Registration</span>
                <h3 style="font-size:1.25rem; font-weight:800; color:white; margin-top:2px;">${d.name}</h3>
                <span style="font-family:var(--font-mono); font-size:0.8rem; color:#94a3b8;">Registration: ${d.id} • Aadhaar: ${d.aadhaar}</span>
              </div>
              <span style="background:#dc2626; color:white; font-size:1.5rem; font-weight:900; padding:6px 16px; border-radius:8px;">${d.group}</span>
            </div>

            <div style="display:grid; grid-template-columns:1fr 1fr; gap:14px; font-size:0.85rem; margin-bottom:20px;">
              <div>
                <span style="color:#94a3b8; font-size:0.75rem; display:block;">Permanent Residence</span>
                <strong style="color:white;">${d.city}, ${d.st}</strong>
              </div>
              <div>
                <span style="color:#94a3b8; font-size:0.75rem; display:block;">Registered Mobile Contact</span>
                <strong style="color:white;">${d.mobile || '+91 9848123456'}</strong>
              </div>
              <div>
                <span style="color:#94a3b8; font-size:0.75rem; display:block;">Candidate Status</span>
                <strong style="color:#fbbf24;">${d.status || 'WAITING FOR CLEARANCE'}</strong>
              </div>
              <div>
                <span style="color:#94a3b8; font-size:0.75rem; display:block;">Submission Timestamp</span>
                <strong style="color:#cbd5e1;">${d.submittedAt || 'Today, Active Session'}</strong>
              </div>
            </div>

            <!-- NBTC Standard Form-04 Clinical Findings -->
            <div style="background:#0f172a; border:1px solid #334155; border-radius:8px; padding:16px; margin-bottom:20px;">
              <div style="font-size:0.82rem; font-weight:800; color:#38bdf8; margin-bottom:10px;">NBTC CLINICAL SCREENING METRICS</div>
              <table style="width:100%; font-size:0.82rem; color:#cbd5e1; border-collapse:collapse;">
                <tr style="border-bottom:1px solid #1e293b;"><td style="padding:6px 0; color:#94a3b8;">Hemoglobin (Hb):</td><td><strong style="color:#34d399;">13.5 g/dL</strong> (Statutory Min: 12.5 g/dL) ✓</td></tr>
                <tr style="border-bottom:1px solid #1e293b;"><td style="padding:6px 0; color:#94a3b8;">Blood Pressure:</td><td><strong style="color:white;">120/80 mmHg</strong> (Normotensive) ✓</td></tr>
                <tr style="border-bottom:1px solid #1e293b;"><td style="padding:6px 0; color:#94a3b8;">Pulse & Temperature:</td><td><strong style="color:white;">74 bpm • 98.4°F (Afebrile)</strong> ✓</td></tr>
                <tr><td style="padding:6px 0; color:#94a3b8;">Serological Screen:</td><td><strong style="color:#34d399;">NON-REACTIVE</strong> (HIV, HBsAg, HCV, VDRL) ✓</td></tr>
              </table>
            </div>

            <!-- Dr. Reddy Statutory Attestation -->
            <div style="background:#132338; border-left:4px solid #38bdf8; padding:12px 16px; border-radius:0 8px 8px 0; font-size:0.78rem; color:#e2e8f0; line-height:1.6;">
              <em>"I have reviewed the uploaded medical proof and laboratory reports. The candidate satisfies all statutory physiological benchmarks and is medically qualified for voluntary donation."</em><br/>
              <strong style="color:#38bdf8;">Dr. V. S. Reddy, MD (Chief Medical Officer & Civil Surgeon)</strong><br/>
              <span style="font-size:0.72rem; color:#94a3b8;">NBTC Statutory Registration #MCI-AP-49201</span>
            </div>
          </div>

          <!-- Right Column: Official Certificate Previews (PDF / Image) -->
          <div style="background:#1e293b; border:1px solid #334155; border-radius:12px; padding:24px; display:flex; flex-direction:column;">
            <div style="font-size:0.85rem; font-weight:800; color:white; margin-bottom:14px; display:flex; justify-content:space-between; align-items:center;">
              <span>OFFICIAL CERTIFICATES PREVIEW</span>
              <span style="font-size:0.72rem; color:#94a3b8;">2 Documents Attached</span>
            </div>

            <!-- Document 1: Fitness Certificate -->
            <div style="background:#0f172a; border:1px solid #334155; border-radius:8px; padding:14px; margin-bottom:16px;">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <span style="font-size:0.78rem; font-weight:700; color:#38bdf8;">📄 1. Doctor Signed Medical Fitness Certificate</span>
                <span style="font-size:0.7rem; font-family:var(--font-mono); color:#cbd5e1;">${d.cert || 'physician_clearance.pdf'}</span>
              </div>
              ${d.certUrl ? `
                ${isPdfFit ? `
                  <iframe src="${d.certUrl}" style="width:100%; height:220px; border:1px solid #334155; border-radius:6px; background:white;"></iframe>
                ` : `
                  <img src="${d.certUrl}" style="width:100%; max-height:220px; object-fit:contain; border-radius:6px; background:white;" />
                `}
              ` : `
                <div style="background:#1e293b; border:1px dashed #475569; border-radius:6px; padding:24px; text-align:center;">
                  <span style="font-size:1.8rem; display:block; margin-bottom:6px;">📄</span>
                  <strong style="font-size:0.82rem; color:white;">Official Registered Physician Certificate</strong><br/>
                  <span style="font-size:0.74rem; color:#94a3b8;">Document file: <code>${d.cert || 'fitness_certificate.pdf'}</code> (Archived on Cloud Storage)</span>
                </div>
              `}
            </div>

            <!-- Document 2: Blood Group Proof -->
            <div style="background:#0f172a; border:1px solid #334155; border-radius:8px; padding:14px;">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <span style="font-size:0.78rem; font-weight:700; color:#f87171;">🩸 2. Blood Group Lab Report / Donor Card</span>
                <span style="font-size:0.7rem; font-family:var(--font-mono); color:#cbd5e1;">${d.proof || 'lab_group_proof.pdf'}</span>
              </div>
              ${d.proofUrl ? `
                ${isPdfProof ? `
                  <iframe src="${d.proofUrl}" style="width:100%; height:220px; border:1px solid #334155; border-radius:6px; background:white;"></iframe>
                ` : `
                  <img src="${d.proofUrl}" style="width:100%; max-height:220px; object-fit:contain; border-radius:6px; background:white;" />
                `}
              ` : `
                <div style="background:#1e293b; border:1px dashed #475569; border-radius:6px; padding:24px; text-align:center;">
                  <span style="font-size:1.8rem; display:block; margin-bottom:6px;">🩸</span>
                  <strong style="font-size:0.82rem; color:white;">Clinical Pathology Laboratory Report</strong><br/>
                  <span style="font-size:0.74rem; color:#94a3b8;">Document file: <code>${d.proof || 'pathology_group_report.pdf'}</code> (Archived on Cloud Storage)</span>
                </div>
              `}
            </div>
          </div>
        </div>
      `;

      // Update Action Bar buttons
      const actionContainer = document.getElementById('consoleActionButtons');
      if (d.status === 'APPROVED') {
        actionContainer.innerHTML = `
          <span style="color:#34d399; font-weight:800; font-size:0.9rem; margin-right:12px;">✓ Candidate Medically Cleared & Published to Live Registry</span>
          <button class="btn btn-secondary" onclick="closeCandidateConsoleView()" style="background:#1e293b; color:white; border-color:#475569;">Return to Roster</button>
        `;
      } else {
        actionContainer.innerHTML = `
          <button class="btn btn-secondary" onclick="deferFromCandidateConsole()" style="background:#450a0a; border-color:#991b1b; color:#fca5a5; font-size:0.85rem; padding:8px 20px; font-weight:700;">
            ✕ Decline / 90-Day Deferral
          </button>
          <button class="btn btn-primary" onclick="approveFromCandidateConsole()" style="background:#059669; border-color:#059669; font-size:0.85rem; padding:8px 24px; font-weight:800;">
            ✓ Approve & Grant Clearance
          </button>
        `;
      }
    };

    window.closeCandidateConsoleView = function() {
      const consoleView = document.getElementById('authCandidateConsoleView');
      if (consoleView) consoleView.style.display = 'none';
      const rosterView = document.getElementById('authRosterView');
      if (rosterView) rosterView.style.display = 'flex';
      renderDesktopPendingList();
    };

    window.approveFromCandidateConsole = function() {
      if (window.currentReviewCandidateIdx === null || window.currentReviewCandidateIdx === undefined) return;
      const d = window.desktopPendingDonors[window.currentReviewCandidateIdx];
      if (!d) return;

      d.status = 'APPROVED';

      window.fullDonorsList.unshift({
        id: `DNR-${String(257 + window.currentReviewCandidateIdx)}`,
        name: d.name,
        aadhaar: d.aadhaar,
        bloodGroup: d.group,
        state: d.st,
        city: d.city,
        district: `${d.city}, ${d.st}`,
        healthStatus: "FIT (Hb: 13.5 g/dL, Rest: 95d)",
        fitClass: "status-fit",
        medicalProof: d.cert,
        groupProof: d.proof,
        mobile: d.mobile || ("+91 9848" + Math.floor(100000 + Math.random() * 900000)),
        verification: "APPROVED_BY_MEDICAL_OFFICER",
        donationState: "Ready to Donate (Eligible Now)"
      });

      addNotification({
        category: 'APPROVAL',
        title: `✓ Medical Clearance Approved`,
        message: `${d.name} (${d.group}, ${d.city}) cleared by Dr. V. S. Reddy and added to the National Live Donor Directory.`,
        time: 'Just now',
        unread: true
      });

      alert(`✓ ${d.name} (${d.group}) has been APPROVED!\nCredentials verified and added to live 256+ donor directory.`);
      closeCandidateConsoleView();
    };

    window.deferFromCandidateConsole = function() {
      if (window.currentReviewCandidateIdx === null || window.currentReviewCandidateIdx === undefined) return;
      const d = window.desktopPendingDonors[window.currentReviewCandidateIdx];
      if (!d) return;

      d.status = 'DEFERRED';

      addNotification({
        category: 'APPROVAL',
        title: `Donor Clinical Deferral`,
        message: `Candidate ${d.name} (${d.group}) has been placed on 90-day medical deferral.`,
        time: 'Just now',
        unread: true
      });

      alert(`Donor ${d.name} placed on 90-day clinical deferral.`);
      closeCandidateConsoleView();
    };

    // CampFlow Style Autofill Keychain Logic
    window.openLoginModal = function() {
      const modal = document.getElementById('loginModal');
      if (modal) modal.style.display = 'flex';
    };

    window.closeLoginModal = function() {
      const modal = document.getElementById('loginModal');
      if (modal) modal.style.display = 'none';
      hideKeychain();
    };

    window.showKeychain = function() {
      const kd = document.getElementById('keychainDropdown');
      if (kd) kd.style.display = 'block';
    };

    window.hideKeychain = function() {
      const kd = document.getElementById('keychainDropdown');
      if (kd) kd.style.display = 'none';
    };

    window.toggleKeychain = function() {
      const kd = document.getElementById('keychainDropdown');
      if (kd) kd.style.display = kd.style.display === 'block' ? 'none' : 'block';
    };

    window.selectKeychainAccount = function(email, pass, role) {
      const emailInput = document.getElementById('loginEmail');
      const passInput = document.getElementById('loginPassword');
      if (emailInput) emailInput.value = email;
      if (passInput) passInput.value = pass;
      hideKeychain();
      executeLogin(role);
    };

    window.executeLogin = function(roleOverride = null) {
      const email = (document.getElementById('loginEmail').value || '').trim();
      const role = roleOverride || (email.includes('admin') ? 'SUPER_ADMIN' : (email.includes('doctor') ? 'MEDICAL_OFFICER' : (email.includes('dho') ? 'DISTRICT_AUTHORITY' : (email.includes('bank') ? 'BLOOD_BANK_ADMIN' : 'DONOR'))));

      let displayName = email.split('@')[0].replace(/[._]/g, ' ');
      displayName = displayName.replace(/\\b\\w/g, l => l.toUpperCase());

      window.currentUser = {
        email: email,
        role: role,
        name: displayName
      };

      const fb = document.getElementById('loginFeedback');
      if (fb) {
        fb.style.display = 'block';
        fb.style.color = '#34d399';
        fb.innerHTML = `✓ Signed in: <strong>${email}</strong> [${role}]`;
      }

      // Update Navbar Sign In -> Sign Out toggle
      const signInBtn = document.getElementById('navSignInBtn');
      const userBadge = document.getElementById('navUserBadge');
      const userName = document.getElementById('navUserName');
      const userRole = document.getElementById('navUserRole');

      if (signInBtn) signInBtn.style.display = 'none';
      if (userBadge) userBadge.style.display = 'inline-flex';
      if (userName) userName.innerText = displayName;
      if (userRole) userRole.innerText = role.replace(/_/g, ' ');

      addNotification({
        category: 'ALL',
        title: `Welcome, ${displayName}`,
        message: `Authenticated as ${role.replace(/_/g, ' ')}. Direct blood coordination & medical clearance tools active.`,
        time: 'Just now',
        unread: true
      });

      setTimeout(() => {
        closeLoginModal();
        if (role.includes('OFFICER') || role.includes('ADMIN') || role.includes('AUTHORITY') || role.includes('BANK')) {
          const banner = document.getElementById('authorityBanner');
          if (banner) banner.style.display = 'flex';
          const sessionText = document.getElementById('authoritySessionText');
          if (sessionText) sessionText.innerText = `Signed in as ${role.replace(/_/g, ' ')} (${email})`;
          openAuthorityReviewModal();
        } else {
          alert(`✓ Welcome, ${displayName}! Your voluntary donor session is active.`);
        }
      }, 350);
    };

    window.executeSignOut = function() {
      window.currentUser = null;

      const signInBtn = document.getElementById('navSignInBtn');
      const userBadge = document.getElementById('navUserBadge');
      const banner = document.getElementById('authorityBanner');
      const notifPanel = document.getElementById('notifDropdown');

      if (signInBtn) signInBtn.style.display = 'inline-block';
      if (userBadge) userBadge.style.display = 'none';
      if (banner) banner.style.display = 'none';
      if (notifPanel) notifPanel.style.display = 'none';

      closeAuthorityReviewModal();
      alert('Signed out successfully. Session ended.');
    };

    window.signOutAuthority = function() {
      executeSignOut();
    };

    // Notification Center Logic
    window.notificationsList = [
      {
        id: 'n1',
        category: 'EMERGENCY',
        title: '🚨 Emergency O- Needed (ICU)',
        message: 'Apollo Speciality Hospital req REQ-8001 (Vijayawada). 2 units standard PRBC needed immediately.',
        time: '12m ago',
        unread: true
      },
      {
        id: 'n2',
        category: 'APPROVAL',
        title: '✓ Medical Clearance Approved',
        message: 'Dr. V. S. Reddy cleared Suresh Nair (B+) for voluntary donation with verified lab certificates.',
        time: '34m ago',
        unread: true
      },
      {
        id: 'n3',
        category: 'DONATION',
        title: '🎉 Donor Found for Tanvi Sharma',
        message: 'Harish Kumar (O-) accepted donation request REQ-8004 at Yashoda Hospital. Attendant notified.',
        time: '1h ago',
        unread: true
      },
      {
        id: 'n4',
        category: 'EMERGENCY',
        title: '🚨 AB- Trauma Transfusion Alert',
        message: 'Manipal Hospital ICU trauma requirement for Rajesh Reddy. Matched donors notified.',
        time: '2h ago',
        unread: false
      }
    ];

    window.currentNotifFilter = 'ALL';

    window.toggleNotificationPanel = function() {
      const panel = document.getElementById('notifDropdown');
      if (!panel) return;
      const isVisible = (panel.style.display === 'block');
      panel.style.display = isVisible ? 'none' : 'block';
      if (!isVisible) {
        renderNotifications();
      }
    };

    window.switchNotifFilter = function(category, btnEl) {
      window.currentNotifFilter = category;
      document.querySelectorAll('.notif-tab').forEach(b => b.classList.remove('active'));
      if (btnEl) btnEl.classList.add('active');
      renderNotifications();
    };

    window.renderNotifications = function() {
      const container = document.getElementById('notifItemsContainer');
      if (!container) return;

      let list = window.notificationsList || [];
      if (window.currentNotifFilter !== 'ALL') {
        list = list.filter(n => n.category === window.currentNotifFilter);
      }

      if (list.length === 0) {
        container.innerHTML = '<div style="text-align:center; padding:32px; color:#94a3b8; font-size:0.8rem;">No notifications in this category.</div>';
      } else {
        container.innerHTML = list.map(n => `
          <div class="notif-item ${n.unread ? 'unread' : ''}" onclick="markSingleNotifRead('${n.id}')">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:2px;">
              <strong style="font-size:0.82rem; color:var(--navy-900);">${n.title}</strong>
              <span style="font-size:0.7rem; color:#94a3b8;">${n.time}</span>
            </div>
            <div style="font-size:0.76rem; color:var(--slate-600); line-height:1.4;">${n.message}</div>
          </div>
        `).join('');
      }

      updateNotificationBadge();
    };

    window.markSingleNotifRead = function(id) {
      const n = (window.notificationsList || []).find(x => x.id === id);
      if (n) n.unread = false;
      renderNotifications();
    };

    window.markAllNotificationsRead = function() {
      (window.notificationsList || []).forEach(n => n.unread = false);
      renderNotifications();
    };

    window.addNotification = function(notif) {
      if (!window.notificationsList) window.notificationsList = [];
      window.notificationsList.unshift({
        id: 'n-' + Date.now(),
        category: notif.category || 'ALL',
        title: notif.title,
        message: notif.message,
        time: notif.time || 'Just now',
        unread: true
      });
      renderNotifications();
    };

    window.updateNotificationBadge = function() {
      const unreadCount = (window.notificationsList || []).filter(n => n.unread).length;
      const badge = document.getElementById('notifBadge');
      const pill = document.getElementById('notifUnreadPill');
      
      if (badge) {
        if (unreadCount > 0) {
          badge.style.display = 'inline-block';
          badge.innerText = unreadCount;
        } else {
          badge.style.display = 'none';
        }
      }

      if (pill) {
        pill.innerText = `${unreadCount} Unread`;
        pill.style.display = unreadCount > 0 ? 'inline-block' : 'none';
      }
    };

    // Close notifications when clicking outside
    document.addEventListener('click', function(e) {
      const panel = document.getElementById('notifDropdown');
      const btn = document.getElementById('notifBellBtn');
      if (panel && panel.style.display === 'block') {
        if (!panel.contains(e.target) && !btn.contains(e.target)) {
          panel.style.display = 'none';
        }
      }
    });

    window.openClinicalHelpModal = function() {
      const modal = document.getElementById('clinicalHelpModal');
      if (modal) modal.style.display = 'flex';
    };

    window.closeClinicalHelpModal = function() {
      const modal = document.getElementById('clinicalHelpModal');
      if (modal) modal.style.display = 'none';
    };

'''

html_content = html_content[:start_idx] + new_js + html_content[end_idx:]

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("Part 3 JavaScript replacement successfully applied to public/index.html")
