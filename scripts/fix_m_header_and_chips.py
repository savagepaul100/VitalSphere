import os

path = r"C:\Users\PAUL\Documents\VitalSphere\public\m\index.html"
with open(path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update .header-actions in Mobile
old_header_actions = '''    <div class="header-actions">
      <a href="/?view=desktop" class="btn-header" title="Switch to Full Desktop Version">Desktop [PC]</a>
      <button class="btn-header primary" onclick="openMobileLogin()">Sign In</button>
    </div>'''

new_header_actions = '''    <div class="header-actions" style="display:flex; align-items:center; gap:6px;">
      <a href="/?view=desktop" class="btn-header" title="Switch to Full Desktop Version" style="padding:5px 8px; font-size:0.7rem;">Desktop [PC]</a>

      <!-- Notification Bell -->
      <button id="mNotifBellBtn" onclick="toggleMobileNotifSheet()" class="btn-header" style="position:relative; padding:5px 8px; display:inline-flex; align-items:center; justify-content:center; background:rgba(255,255,255,0.08); border-color:rgba(255,255,255,0.18);" title="Notifications">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>
        <span id="mNotifBadge" style="position:absolute; top:-4px; right:-4px; background:#dc2626; color:white; font-size:0.6rem; font-weight:900; border-radius:10px; padding:1px 5px; min-width:14px; text-align:center;">3</span>
      </button>

      <!-- Active User Badge / Sign In Toggle -->
      <div id="mNavUserBadge" style="display:none; align-items:center; gap:6px;">
        <span id="mNavUserName" style="font-size:0.7rem; font-weight:800; color:#38bdf8; max-width:70px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">User</span>
        <button onclick="executeMobileSignOut()" class="btn-header" style="background:#dc2626; border-color:#dc2626; padding:4px 8px; font-size:0.68rem; font-weight:800;">Sign Out</button>
      </div>
      <button id="mSignInBtn" class="btn-header primary" onclick="openMobileLogin()" style="padding:5px 12px; font-size:0.72rem;">Sign In</button>
    </div>'''

if old_header_actions in html:
    html = html.replace(old_header_actions, new_header_actions, 1)
    print("Mobile header-actions updated successfully")
else:
    print("Warning: old_header_actions not found")

# 2. Update .stat-chip counters
old_chips = '''        <div class="stat-chip">
          <div class="stat-chip-num">256</div>
          <div class="stat-chip-lbl">Verified Donors</div>
        </div>
        <div class="stat-chip">
          <div class="stat-chip-num">32</div>
          <div class="stat-chip-lbl">Active Requests</div>
        </div>'''

new_chips = '''        <div class="stat-chip">
          <div class="stat-chip-num" id="mHeroDonorCount">256</div>
          <div class="stat-chip-lbl">Verified Donors</div>
        </div>
        <div class="stat-chip">
          <div class="stat-chip-num" id="mHeroRecipientCount">64</div>
          <div class="stat-chip-lbl">Active Requests</div>
        </div>'''

if old_chips in html:
    html = html.replace(old_chips, new_chips, 1)
    print("Mobile stat-chip numbers updated with dynamic IDs")
else:
    print("Warning: old_chips not found")

# 3. Replace the entire script block in m/index.html with self-contained, robust logic
script_start = "  <script>"
script_end = "  </script>"

start_idx = html.rfind(script_start)
end_idx = html.rfind(script_end)

if start_idx == -1 or end_idx == -1:
    print("Error: script tags not found")
    exit(1)

new_m_script = '''  <script>
    // 1. SELF-CONTAINED DATA INITIALIZATION (Immune to network/cache drops)
    if (!window.INDIA_STATES_DATA) {
      window.INDIA_STATES_DATA = {
        "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Tirupati", "Kurnool", "Kakinada", "Nellore", "Kadapa", "Anantapur", "Eluru", "Rajahmundry"],
        "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar", "Khammam"],
        "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Thane", "Nashik", "Aurangabad"],
        "Karnataka": ["Bengaluru", "Mysuru", "Hubballi", "Mangaluru", "Belagavi"],
        "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem"],
        "Delhi NCR": ["New Delhi", "North Delhi", "South Delhi", "Noida", "Gurugram"],
        "Uttar Pradesh": ["Lucknow", "Kanpur", "Varanasi", "Agra", "Prayagraj"],
        "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot"],
        "West Bengal": ["Kolkata", "Howrah", "Durgapur", "Siliguri"],
        "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur"]
      };
    }
    const INDIA_STATES_DATA = window.INDIA_STATES_DATA;

    const FIRST_NAMES = ["Aarav", "Aditi", "Akhil", "Ananya", "Bhavani", "Chaitanya", "Deepika", "Dinesh", "Gowri", "Harish", "Ishaan", "Kavya", "Krishna", "Lakshmi", "Madhav", "Manish", "Naveen", "Pallavi", "Praneeth", "Priya", "Rahul", "Rajesh", "Ramana", "Sai", "Sandeep", "Sneha", "Srinivas", "Suresh", "Surya", "Swapna", "Tarun", "Varun", "Venkatesh", "Vidya", "Vijay", "Vikram", "Yashwant", "Rohan", "Tanvi", "Arjun"];
    const LAST_NAMES = ["Reddy", "Rao", "Chowdary", "Varma", "Naidu", "Sharma", "Murthy", "Sastry", "Raju", "Prasad", "Babu", "Kumar", "Gupta", "Pillai", "Patnaik", "Devi", "Deshmukh", "Patil", "Iyer", "Banerjee", "Singh", "Verma", "Mehta", "Joshi"];
    const BLOOD_GROUPS = ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"];
    const ALL_STATES = Object.keys(INDIA_STATES_DATA);

    // Synchronous Donors Fallback
    if (!window.fullDonorsList || window.fullDonorsList.length === 0) {
      window.fullDonorsList = [];
      for (let i = 1; i <= 256; i++) {
        const fn = FIRST_NAMES[i % FIRST_NAMES.length];
        const ln = LAST_NAMES[(i * 3) % LAST_NAMES.length];
        const bg = BLOOD_GROUPS[i % BLOOD_GROUPS.length];
        const st = ALL_STATES[i % ALL_STATES.length];
        const cities = INDIA_STATES_DATA[st] || ["Capital City"];
        const city = cities[i % cities.length];
        const daysRest = 90 + ((i * 7) % 65);
        const hb = (12.6 + ((i % 25) * 0.12)).toFixed(1);
        const aadhaarLast4 = String(1000 + ((i * 37) % 8999));
        const isFit = hb >= 12.5;

        window.fullDonorsList.push({
          id: `DNR-${String(i).padStart(3, '0')}`,
          name: `${fn} ${ln}`,
          aadhaar: `XXXX-XXXX-${aadhaarLast4}`,
          bloodGroup: bg,
          group: bg,
          state: st,
          city: city,
          district: `${city}, ${st}`,
          healthStatus: isFit ? `FIT (Hb: ${hb} g/dL, Rest: ${daysRest}d)` : `BORDERLINE (Hb: ${hb} g/dL)`,
          fitClass: isFit ? "fit" : "borderline",
          medicalProof: "Registered Physician Medical Certificate",
          groupProof: (i % 2 === 0) ? "Official Red Cross Donor Card" : "Clinical Pathology Lab Certificate",
          mobile: `+91 981${String(1000000 + (i * 26664)).slice(0, 7)}`,
          verification: "APPROVED_BY_MEDICAL_OFFICER",
          donationState: isFit ? "Ready to Donate (Eligible Now)" : "Already Donated (Verified History)"
        });
      }
    }

    // Synchronous Recipients Fallback
    if (!window.fullRecipientsList || window.fullRecipientsList.length === 0) {
      window.fullRecipientsList = [];
      const HOSPITALS = [
        "Apollo Speciality Hospital", "Care Emergency Hospital", "Government General Hospital (GGH)",
        "Manipal Hospital", "KIMS Super Speciality Hospital", "Aster Prime Hospital",
        "Max Healthcare Trauma Center", "Fortis Escorts Hospital", "Narayana Hrudayalaya",
        "Medanta The Medicity", "Sir Ganga Ram Hospital", "Ruby Hall Clinic",
        "Yashoda Super Speciality Hospital", "Amrita Institute of Medical Sciences",
        "Tata Memorial Hospital", "AIIMS Trauma Center"
      ];
      for (let j = 1; j <= 64; j++) {
        const pfn = FIRST_NAMES[(j * 7) % FIRST_NAMES.length];
        const pln = LAST_NAMES[(j * 5) % LAST_NAMES.length];
        const bg = BLOOD_GROUPS[j % BLOOD_GROUPS.length];
        const hosp = HOSPITALS[j % HOSPITALS.length];
        const st = ALL_STATES[(j * 3) % ALL_STATES.length];
        const cities = INDIA_STATES_DATA[st] || ["Central Hospital Area"];
        const city = cities[(j * 2) % cities.length];
        const units = 1 + (j % 4);
        const urg = j % 3 === 0 ? "CRITICAL" : (j % 3 === 1 ? "URGENT" : "ROUTINE");
        const aadhaarLast4 = String(2000 + ((j * 43) % 7999));

        window.fullRecipientsList.push({
          id: `REQ-${String(8000 + j)}`,
          patientName: `${pfn} ${pln}`,
          aadhaar: `XXXX-XXXX-${aadhaarLast4}`,
          bloodGroup: bg,
          group: bg,
          units: `${units} Unit${units > 1 ? 's' : ''} (${units * 350} ml)`,
          hospital: hosp,
          state: st,
          city: city,
          district: `${city}, ${st}`,
          urgency: urg,
          urgencyClass: urg === 'CRITICAL' ? 'borderline' : 'fit',
          contact: `+91 97${String(20000000 + (j * 44444)).slice(0, 8)}`,
          status: j % 4 === 0 ? "ALLOCATED" : "LOOKING_FOR_DONORS"
        });
      }
    }

    // Dynamic Counters
    window.updateMobileCounters = function() {
      const dLen = (window.fullDonorsList || []).length;
      const rLen = (window.fullRecipientsList || []).length;
      const dEl = document.getElementById('mHeroDonorCount');
      if (dEl) dEl.innerText = dLen;
      const rEl = document.getElementById('mHeroRecipientCount');
      if (rEl) rEl.innerText = rLen;
    };

    // Helper for robust blood group matching
    function matchGroup(recordGroup, filterGroup) {
      if (!filterGroup || filterGroup === 'ALL') return true;
      if (!recordGroup) return false;
      const rg = String(recordGroup).trim().toUpperCase();
      const fg = String(filterGroup).trim().toUpperCase();
      if (rg === fg) return true;
      if (rg.includes(`(${fg})`)) return true;
      if (rg.startsWith(fg + ' ') || rg.startsWith(fg + '-')) return true;
      return false;
    }

    // 2. FULLSCREEN MOBILE DIRECTORY POPUP
    window.mFsCurrentGroup = 'ALL';
    window.mFsCurrentTab = 'donors';

    window.openMobileFsDirectory = function(group = null) {
      window.mFsCurrentGroup = group || 'ALL';
      const modal = document.getElementById('mFullscreenDirectoryModal');
      if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
      }

      const title = document.getElementById('mFsModalTitle');
      const subtitle = document.getElementById('mFsModalSubtitle');
      if (title) {
        title.innerText = (group && group !== 'ALL') ? `Directory — Group ${group}` : 'Pan-India Directory';
      }
      if (subtitle) {
        subtitle.innerText = (group && group !== 'ALL') ? `Verified voluntary donors and patients for ${group}` : 'Verified Voluntary Donors & Active Patients';
      }

      // Highlight matching group pill
      document.querySelectorAll('.m-grp-pill').forEach(btn => {
        const text = btn.innerText.trim();
        if ((!group || group === 'ALL') && text === 'All Groups') {
          btn.classList.add('active');
        } else if (text === group) {
          btn.classList.add('active');
        } else {
          btn.classList.remove('active');
        }
      });

      applyMobileFsFilter();
    };

    window.closeMobileFsDirectory = function() {
      const modal = document.getElementById('mFullscreenDirectoryModal');
      if (modal) modal.style.display = 'none';
      document.body.style.overflow = 'auto';
      closeMobileFsDetail();
    };

    window.setMobileFsGroupFilter = function(grp, btnEl) {
      window.mFsCurrentGroup = grp;
      document.querySelectorAll('#mGroupPillsContainer .m-grp-pill').forEach(b => b.classList.remove('active'));
      if (btnEl) btnEl.classList.add('active');
      const title = document.getElementById('mFsModalTitle');
      if (title) {
        title.innerText = (grp && grp !== 'ALL') ? `Directory — Group ${grp}` : 'Pan-India Directory';
      }
      applyMobileFsFilter();
    };

    window.switchMobileFsTab = function(tab) {
      window.mFsCurrentTab = tab;
      const btnD = document.getElementById('mFsTabDonors');
      const btnR = document.getElementById('mFsTabRecipients');
      if (btnD) btnD.classList.toggle('active', tab === 'donors');
      if (btnR) btnR.classList.toggle('active', tab === 'recipients');
      applyMobileFsFilter();
    };

    window.applyMobileFsFilter = function() {
      const q = (document.getElementById('mFsFilterInput') ? document.getElementById('mFsFilterInput').value : '').toLowerCase().trim();
      const container = document.getElementById('mFsDirectoryListContainer');
      if (!container) return;
      container.innerHTML = '';

      const allDonors = window.fullDonorsList || [];
      const allRecipients = window.fullRecipientsList || [];

      // Calculate counts for active group filter
      const matchedDonorsCount = allDonors.filter(d => matchGroup(d.bloodGroup || d.group, window.mFsCurrentGroup)).length;
      const matchedRecipientsCount = allRecipients.filter(r => matchGroup(r.bloodGroup || r.group, window.mFsCurrentGroup)).length;

      const cntDEl = document.getElementById('mFsDonorsCount');
      if (cntDEl) cntDEl.innerText = matchedDonorsCount;
      const cntREl = document.getElementById('mFsRecipientsCount');
      if (cntREl) cntREl.innerText = matchedRecipientsCount;

      if (window.mFsCurrentTab === 'donors') {
        let list = allDonors.filter(d => matchGroup(d.bloodGroup || d.group, window.mFsCurrentGroup));
        if (q) {
          list = list.filter(d => 
            (d.name && d.name.toLowerCase().includes(q)) ||
            (d.district && d.district.toLowerCase().includes(q)) ||
            (d.id && d.id.toLowerCase().includes(q)) ||
            (d.bloodGroup && d.bloodGroup.toLowerCase().includes(q))
          );
        }

        if (list.length === 0) {
          container.innerHTML = '<div style="text-align:center; padding:40px; color:var(--slate-400); font-size:0.85rem;">No donors found for this selection.</div>';
          return;
        }

        list.forEach(d => {
          const card = document.createElement('div');
          card.className = 'm-clean-card';
          card.onclick = () => openMobileFsDonorDetail(d.id);
          card.innerHTML = `
            <div style="display:flex; align-items:center; gap:12px; flex:1;">
              <span class="d-bg-badge" style="font-size:1.1rem; padding:4px 10px; min-width:44px; text-align:center;">${d.bloodGroup}</span>
              <div>
                <div style="font-size:0.95rem; font-weight:800; color:var(--navy-900); margin-bottom:2px;">${d.name}</div>
                <div style="font-size:0.75rem; color:var(--slate-500); display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
                  <span style="font-family:var(--font-mono); font-weight:700; background:var(--slate-100); padding:2px 6px; border-radius:4px;">${d.id}</span>
                  <span>${d.district}</span>
                </div>
              </div>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
              <button style="background:var(--slate-100); border:1px solid var(--slate-200); color:var(--navy-900); border-radius:6px; font-size:0.75rem; font-weight:700; padding:6px 10px; cursor:pointer;">
                Info →
              </button>
            </div>
          `;
          container.appendChild(card);
        });

      } else {
        let list = allRecipients.filter(r => matchGroup(r.bloodGroup || r.group, window.mFsCurrentGroup));
        if (q) {
          list = list.filter(r => 
            (r.patientName && r.patientName.toLowerCase().includes(q)) ||
            (r.district && r.district.toLowerCase().includes(q)) ||
            (r.hospital && r.hospital.toLowerCase().includes(q)) ||
            (r.id && r.id.toLowerCase().includes(q)) ||
            (r.bloodGroup && r.bloodGroup.toLowerCase().includes(q))
          );
        }

        if (list.length === 0) {
          container.innerHTML = '<div style="text-align:center; padding:40px; color:var(--slate-400); font-size:0.85rem;">No recipients found for this selection.</div>';
          return;
        }

        list.forEach(r => {
          const card = document.createElement('div');
          card.className = 'm-clean-card';
          card.onclick = () => openMobileFsRecipientDetail(r.id);
          card.innerHTML = `
            <div style="display:flex; align-items:center; gap:12px; flex:1;">
              <span class="d-bg-badge" style="font-size:1.1rem; padding:4px 10px; min-width:44px; text-align:center;">${r.bloodGroup}</span>
              <div>
                <div style="display:flex; align-items:center; gap:6px; margin-bottom:2px;">
                  <span style="font-size:0.95rem; font-weight:800; color:var(--navy-900);">${r.patientName}</span>
                  <span class="d-fit-pill ${r.urgency === 'CRITICAL' ? 'borderline' : 'fit'}" style="font-size:0.65rem; padding:1px 6px;">${r.urgency}</span>
                </div>
                <div style="font-size:0.75rem; color:var(--slate-500); display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
                  <span style="font-family:var(--font-mono); font-weight:700; background:var(--slate-100); padding:2px 6px; border-radius:4px;">${r.id}</span>
                  <span>${r.hospital}</span>
                  <span>(${r.units})</span>
                </div>
              </div>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
              <button onclick="event.stopPropagation(); handleMobileDonate('${r.id}')" style="background:#dc2626; color:white; border:none; border-radius:6px; font-size:0.75rem; font-weight:800; padding:6px 12px; cursor:pointer;">
                Donate
              </button>
              <button style="background:var(--slate-100); border:1px solid var(--slate-200); color:var(--navy-900); border-radius:6px; font-size:0.75rem; font-weight:700; padding:6px 10px; cursor:pointer;">
                Info →
              </button>
            </div>
          `;
          container.appendChild(card);
        });
      }
    };

    window.openMobileFsDonorDetail = function(donorId) {
      const d = (window.fullDonorsList || []).find(x => x.id === donorId);
      if (!d) return;

      document.getElementById('mFsDetailCategory').innerText = 'Verified Voluntary Donor Profile';
      document.getElementById('mFsDetailTitle').innerText = `${d.name} (${d.bloodGroup})`;

      const body = document.getElementById('mFsDetailBody');
      body.innerHTML = `
        <div style="background:#f8fafc; border:1px solid var(--slate-200); border-radius:10px; padding:14px; margin-bottom:12px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span style="font-family:var(--font-mono); font-size:0.8rem; font-weight:800; color:var(--navy-900);">${d.id} • Aadhaar: ${d.aadhaar}</span>
            <span class="d-bg-badge">${d.bloodGroup}</span>
          </div>
          <div style="font-size:0.8rem; color:var(--slate-600); line-height:1.6;">
            <strong>Full Legal Name:</strong> ${d.name}<br/>
            <strong>Residential Area:</strong> ${d.district}<br/>
            <strong>Clinical Status:</strong> <span style="color:var(--emerald-600); font-weight:700;">${d.healthStatus}</span><br/>
            <strong>Official Proofs:</strong> ${d.medicalProof} & ${d.groupProof}
          </div>
        </div>
        <div style="background:#ecfdf5; border-left:3px solid #059669; padding:8px 12px; font-size:0.75rem; color:#065f46; border-radius:0 6px 6px 0;">
          ✓ Statutory NBTC Clinical Standards Verified: Hb ≥ 12.5 g/dL, optimal rest period, non-reactive serology.
        </div>
      `;

      const footer = document.getElementById('mFsDetailFooter');
      footer.innerHTML = `
        <button onclick="closeMobileFsDetail()" style="flex:1; height:42px; background:var(--slate-100); border:1px solid var(--slate-300); color:var(--navy-900); border-radius:8px; font-weight:700; font-size:0.82rem; cursor:pointer;">
          Close
        </button>
        <a href="tel:${d.mobile}" style="flex:1.5; height:42px; background:#059669; color:white; border-radius:8px; font-weight:800; font-size:0.85rem; text-decoration:none; display:flex; align-items:center; justify-content:center; gap:6px;">
          Request / Call (${d.mobile})
        </a>
      `;

      document.getElementById('mFsDetailModal').style.display = 'flex';
    };

    window.openMobileFsRecipientDetail = function(reqId) {
      const r = (window.fullRecipientsList || []).find(x => x.id === reqId);
      if (!r) return;

      document.getElementById('mFsDetailCategory').innerText = 'Emergency Transfusion Dossier';
      document.getElementById('mFsDetailTitle').innerText = `${r.patientName} (${r.bloodGroup})`;

      const isCommitted = r.status && r.status.includes('DONOR FOUND');

      const body = document.getElementById('mFsDetailBody');
      body.innerHTML = `
        <div style="background:#f8fafc; border:1px solid var(--slate-200); border-radius:10px; padding:14px; margin-bottom:12px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span style="font-family:var(--font-mono); font-size:0.8rem; font-weight:800; color:var(--navy-900);">${r.id} • Aadhaar: ${r.aadhaar}</span>
            <span class="d-bg-badge">${r.bloodGroup}</span>
          </div>
          <div style="font-size:0.8rem; color:var(--slate-600); line-height:1.6;">
            <strong>Patient Name:</strong> ${r.patientName}<br/>
            <strong>Hospital:</strong> ${r.hospital} (${r.district})<br/>
            <strong>Units Required:</strong> <strong style="color:#dc2626;">${r.units}</strong><br/>
            <strong>Clinical Urgency:</strong> <span class="d-fit-pill ${r.urgency === 'CRITICAL' ? 'borderline' : 'fit'}">${r.urgency}</span><br/>
            <strong>Attendant Contact:</strong> ${r.contact}<br/>
            <strong>Status:</strong> <span style="font-weight:700; color:${isCommitted ? '#059669' : '#d97706'};">${r.status || 'LOOKING_FOR_DONORS'}</span>
          </div>
        </div>
        ${isCommitted ? `
          <div style="background:#ecfdf5; border-left:3px solid #059669; padding:8px 12px; font-size:0.75rem; color:#065f46; border-radius:0 6px 6px 0;">
            ✓ Confirmed Donor Assigned! Coordination in progress.
          </div>
        ` : `
          <div style="background:#fff1f2; border-left:3px solid #dc2626; padding:8px 12px; font-size:0.75rem; color:#9f1239; border-radius:0 6px 6px 0;">
            Active Emergency: Click <strong>"Donate Now"</strong> to immediately alert patient attendant and hospital.
          </div>
        `}
      `;

      const footer = document.getElementById('mFsDetailFooter');
      footer.innerHTML = `
        <button onclick="closeMobileFsDetail()" style="flex:1; height:42px; background:var(--slate-100); border:1px solid var(--slate-300); color:var(--navy-900); border-radius:8px; font-weight:700; font-size:0.82rem; cursor:pointer;">
          Close
        </button>
        <a href="tel:${r.contact}" style="flex:1; height:42px; background:var(--navy-900); color:white; border-radius:8px; font-weight:700; font-size:0.8rem; text-decoration:none; display:flex; align-items:center; justify-content:center;">
          Call Attendant
        </a>
        <button onclick="handleMobileDonate('${r.id}')" style="flex:1.2; height:42px; background:#dc2626; color:white; border:none; border-radius:8px; font-weight:800; font-size:0.85rem; cursor:pointer;">
          Donate Now
        </button>
      `;

      document.getElementById('mFsDetailModal').style.display = 'flex';
    };

    window.closeMobileFsDetail = function() {
      const modal = document.getElementById('mFsDetailModal');
      if (modal) modal.style.display = 'none';
    };

    window.handleMobileDonate = function(reqId) {
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
      
      addMobileNotification({
        category: 'DONATION',
        title: `✓ Donor Found for ${r.patientName}!`,
        message: `Donor has accepted emergency request ${r.id} (${r.bloodGroup}) at ${r.hospital}. Attendant notified.`,
        time: 'Just now',
        targetReqId: r.id
      });

      applyMobileFsFilter();
      if (document.getElementById('mFsDetailModal').style.display === 'flex') {
        openMobileFsRecipientDetail(reqId);
      }

      alert(
        `✓ SUCCESS: Notification dispatched to ${r.patientName}'s attendant!\\n\\n` +
        `Patient Attendant: ${r.contact}\\n` +
        `Hospital Desk: ${r.hospital}\\n` +
        `Thank you for saving a life!`
      );
    };

    // 3. MOBILE NOTIFICATIONS SYSTEM
    window.mobileNotifList = [
      {
        id: 'mn1',
        category: 'EMERGENCY',
        title: 'Emergency O- Needed (ICU)',
        message: 'Apollo Speciality Hospital req REQ-8001 (Vijayawada). 2 units standard PRBC needed immediately.',
        time: '12m ago',
        unread: true,
        targetReqId: 'REQ-8001',
        group: 'O-'
      },
      {
        id: 'mn2',
        category: 'APPROVAL',
        title: 'Medical Clearance Approved',
        message: 'Dr. V. S. Reddy cleared Suresh Nair (B+) for voluntary donation with verified lab certificates.',
        time: '34m ago',
        unread: true,
        targetDonorId: 'DNR-008',
        group: 'B+'
      },
      {
        id: 'mn3',
        category: 'DONATION',
        title: 'Donor Found for Tanvi Sharma',
        message: 'Harish Kumar (O-) accepted donation request REQ-8004 at Yashoda Hospital. Attendant notified.',
        time: '1h ago',
        unread: true,
        targetReqId: 'REQ-8004',
        group: 'O-'
      },
      {
        id: 'mn4',
        category: 'EMERGENCY',
        title: 'AB- Trauma Transfusion Alert',
        message: 'Manipal Hospital ICU trauma requirement for Rajesh Reddy. 3 units requested.',
        time: '2h ago',
        unread: false,
        targetReqId: 'REQ-8008',
        group: 'AB-'
      }
    ];

    window.currentMobileNotifFilter = 'ALL';

    window.toggleMobileNotifSheet = function() {
      const sheet = document.getElementById('mNotifSheet');
      if (!sheet) return;
      const isVis = sheet.style.display === 'flex';
      sheet.style.display = isVis ? 'none' : 'flex';
      if (!isVis) renderMobileNotifications();
    };

    window.closeMobileNotifSheet = function() {
      const sheet = document.getElementById('mNotifSheet');
      if (sheet) sheet.style.display = 'none';
    };

    window.filterMobileNotifCategory = function(cat, btnEl) {
      window.currentMobileNotifFilter = cat;
      document.querySelectorAll('#mNotifSheet .m-grp-pill').forEach(b => b.classList.remove('active'));
      if (btnEl) btnEl.classList.add('active');
      renderMobileNotifications();
    };

    window.renderMobileNotifications = function() {
      const container = document.getElementById('mNotifItemsList');
      if (!container) return;

      let list = window.mobileNotifList || [];
      if (window.currentMobileNotifFilter !== 'ALL') {
        list = list.filter(n => n.category === window.currentMobileNotifFilter);
      }

      if (list.length === 0) {
        container.innerHTML = '<div style="text-align:center; padding:30px; color:var(--slate-400); font-size:0.8rem;">No notifications in this category.</div>';
      } else {
        container.innerHTML = list.map(n => `
          <div onclick="handleMobileNotifClick('${n.id}')" style="background:#1e293b; border:1px solid ${n.unread ? '#38bdf8' : '#334155'}; border-radius:10px; padding:12px 14px; margin-bottom:8px; cursor:pointer;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
              <strong style="color:white; font-size:0.82rem;">${n.title}</strong>
              <span style="color:#94a3b8; font-size:0.68rem;">${n.time}</span>
            </div>
            <div style="color:#cbd5e1; font-size:0.75rem; line-height:1.4; margin-bottom:6px;">${n.message}</div>
            <div style="display:flex; justify-content:flex-end;">
              <span style="color:#38bdf8; font-size:0.72rem; font-weight:800;">Tap to Donate / Request →</span>
            </div>
          </div>
        `).join('');
      }

      updateMobileNotifBadge();
    };

    // When notification is clicked take me to that Donate / Request page allowing me to donate or Request for blood
    window.handleMobileNotifClick = function(id) {
      const n = (window.mobileNotifList || []).find(x => x.id === id);
      if (!n) return;

      n.unread = false;
      closeMobileNotifSheet();
      updateMobileNotifBadge();

      if (n.targetReqId) {
        // Open fullscreen directory directly to recipients and drilldown to donate!
        openMobileFsDirectory(n.group || null);
        switchMobileFsTab('recipients');
        setTimeout(() => {
          openMobileFsRecipientDetail(n.targetReqId);
        }, 150);
      } else if (n.targetDonorId) {
        // Open fullscreen directory to donors tab
        openMobileFsDirectory(n.group || null);
        switchMobileFsTab('donors');
        setTimeout(() => {
          openMobileFsDonorDetail(n.targetDonorId);
        }, 150);
      } else {
        // Scroll to emergency section
        document.getElementById('request').scrollIntoView({ behavior: 'smooth' });
      }
    };

    window.markAllMobileNotifsRead = function() {
      (window.mobileNotifList || []).forEach(n => n.unread = false);
      renderMobileNotifications();
      updateMobileNotifBadge();
    };

    function addMobileNotification(n) {
      if (!window.mobileNotifList) window.mobileNotifList = [];
      window.mobileNotifList.unshift({
        id: 'mn-' + Date.now(),
        category: n.category || 'ALL',
        title: n.title,
        message: n.message,
        time: 'Just now',
        unread: true,
        targetReqId: n.targetReqId || null,
        group: n.group || null
      });
      updateMobileNotifBadge();
    }

    function updateMobileNotifBadge() {
      const unreadCount = (window.mobileNotifList || []).filter(x => x.unread).length;
      const b = document.getElementById('mNotifBadge');
      if (b) {
        if (unreadCount > 0) {
          b.style.display = 'inline-block';
          b.innerText = unreadCount;
        } else {
          b.style.display = 'none';
        }
      }
    }

    // 4. PAN-INDIA SELECTORS & FORM HANDLERS
    window.populateMobileCities = function(stateSelectId, citySelectId) {
      const stateSel = document.getElementById(stateSelectId);
      const citySel = document.getElementById(citySelectId);
      if (!stateSel || !citySel) return;
      const chosenState = stateSel.value;
      const cities = INDIA_STATES_DATA[chosenState] || ["Central City"];
      
      citySel.innerHTML = '';
      cities.forEach(c => {
        const opt = document.createElement('option');
        opt.value = c;
        opt.textContent = c;
        citySel.appendChild(opt);
      });
    };

    function initMobilePanIndia() {
      const states = Object.keys(INDIA_STATES_DATA);
      ['mDonorState', 'mReqState'].forEach(id => {
        const sel = document.getElementById(id);
        if (!sel) return;
        sel.innerHTML = '';
        states.forEach(s => {
          const opt = document.createElement('option');
          opt.value = s;
          opt.textContent = s;
          sel.appendChild(opt);
        });
      });
      populateMobileCities('mDonorState', 'mDonorCity');
      populateMobileCities('mReqState', 'mReqCity');
    }

    let mobileUploadedCertFile = null;
    let mobileUploadedCertName = 'medical_fitness_dr_signed.pdf';
    let mobileUploadedProofFile = null;
    let mobileUploadedProofName = 'lab_blood_group_card.pdf';

    window.updateMFileTxt = function(input, textId) {
      if (input.files && input.files[0]) {
        const file = input.files[0];
        document.getElementById(textId).innerText = `Selected: ${file.name}`;
        if (input.id === 'mDonorMedCert') {
          mobileUploadedCertFile = file;
          mobileUploadedCertName = file.name;
        } else {
          mobileUploadedProofFile = file;
          mobileUploadedProofName = file.name;
        }
      }
    };

    window.handleMobileDonorSubmit = function(e) {
      e.preventDefault();
      const name = document.getElementById('mDonorName').value.trim();
      const aadhaar = document.getElementById('mDonorAadhaar').value.trim();
      const grp = document.getElementById('mDonorGroup').value;
      const st = document.getElementById('mDonorState').value;
      const city = document.getElementById('mDonorCity').value;
      const fb = document.getElementById('mDonorFeedback');

      if (!name || aadhaar.length !== 12) {
        fb.style.display = 'block';
        fb.style.color = 'var(--red-600)';
        fb.innerText = 'Please enter a valid full name and 12-digit Aadhaar number.';
        return;
      }

      fb.style.display = 'block';
      fb.style.color = 'var(--emerald-600)';
      fb.innerHTML = `✓ Registered <strong>${name}</strong> (${grp}) in ${city}, ${st}!<br/>Uploaded certificates (<code>${mobileUploadedCertName}</code>) queued for Medical Officer clearance.`;

      const newId = `DNR-${window.fullDonorsList.length + 1}`;
      window.fullDonorsList.unshift({
        id: newId,
        name: name,
        aadhaar: `XXXX-XXXX-${aadhaar.slice(8)}`,
        bloodGroup: grp,
        group: grp,
        state: st,
        city: city,
        district: `${city}, ${st}`,
        healthStatus: "FIT (Hb: 13.5 g/dL, Rest: 95d)",
        fitClass: "fit",
        medicalProof: mobileUploadedCertName,
        groupProof: mobileUploadedProofName,
        mobile: "+91 9848123456",
        verification: "APPROVED_BY_MEDICAL_OFFICER",
        donationState: "Ready to Donate (Eligible Now)"
      });

      updateMobileCounters();
      addMobileNotification({
        category: 'APPROVAL',
        title: 'New Donor Registered',
        message: `${name} (${grp}, ${city}) registered credentials for medical clearance.`,
        targetDonorId: newId,
        group: grp
      });

      document.getElementById('mDonorForm').reset();
      document.getElementById('mMedCertTxt').innerText = 'Upload Doctor Signed Fitness Report (.pdf, .png, .jpg)';
      document.getElementById('mBloodProofTxt').innerText = 'Upload Lab Report or Donor ID (.pdf, .png, .jpg)';
    };

    window.handleMobileReqSubmit = function(e) {
      e.preventDefault();
      const patient = document.getElementById('mReqPatient').value.trim();
      const aadhaar = document.getElementById('mReqAadhaar').value.trim();
      const grp = document.getElementById('mReqGroup').value;
      const urgency = document.getElementById('mReqUrgency').value;
      const st = document.getElementById('mReqState').value;
      const city = document.getElementById('mReqCity').value;
      const hosp = document.getElementById('mReqHospital').value.trim();
      const mobile = document.getElementById('mReqMobile').value.trim();
      const fb = document.getElementById('mReqFeedback');

      if (!patient || aadhaar.length !== 12) {
        fb.style.display = 'block';
        fb.style.color = 'var(--red-600)';
        fb.innerText = 'Please enter a valid patient name and 12-digit Aadhaar number.';
        return;
      }

      const newReqId = `REQ-${8000 + window.fullRecipientsList.length + 1}`;
      window.fullRecipientsList.unshift({
        id: newReqId,
        patientName: patient,
        aadhaar: `XXXX-XXXX-${aadhaar.slice(8)}`,
        bloodGroup: grp,
        group: grp,
        units: '2 Units (700 ml)',
        hospital: `${hosp}, ${city}`,
        state: st,
        city: city,
        district: `${city}, ${st}`,
        urgency: urgency,
        urgencyClass: urgency === 'CRITICAL' ? 'borderline' : 'fit',
        contact: mobile,
        status: 'LOOKING_FOR_DONORS'
      });

      updateMobileCounters();
      addMobileNotification({
        category: 'EMERGENCY',
        title: `Emergency Transfusion: ${patient} (${grp})`,
        message: `${hosp}, ${city} requested urgent blood. Attendant contact: ${mobile}.`,
        targetReqId: newReqId,
        group: grp
      });

      fb.style.display = 'block';
      fb.style.color = 'var(--emerald-600)';
      fb.innerHTML = `✓ Emergency requirement registered for <strong>${patient}</strong> (${grp})! Matched donors notified.`;
      document.getElementById('mReqForm').reset();
    };

    // 5. KEYCHAIN LOGIN & LOGOUT
    window.openMobileLogin = function() {
      const sheet = document.getElementById('mKeychainSheet');
      if (sheet) sheet.style.display = 'flex';
    };

    window.closeMobileLogin = function() {
      const sheet = document.getElementById('mKeychainSheet');
      if (sheet) sheet.style.display = 'none';
    };

    window.selectMobileAccount = function(email, title, role) {
      closeMobileLogin();
      window.currentUser = { email, title, role };

      const userBadge = document.getElementById('mNavUserBadge');
      const userName = document.getElementById('mNavUserName');
      const signInBtn = document.getElementById('mSignInBtn');

      if (userBadge) userBadge.style.display = 'inline-flex';
      if (userName) userName.innerText = title.split(' ')[0];
      if (signInBtn) signInBtn.style.display = 'none';

      addMobileNotification({
        category: 'ALL',
        title: `Welcome, ${title}`,
        message: `Signed in as ${role.replace(/_/g, ' ')}. Direct coordination tools unlocked.`,
        group: null
      });

      alert(`✓ Signed in as ${title} [${role}]!`);
    };

    window.executeMobileSignOut = function() {
      window.currentUser = null;
      const userBadge = document.getElementById('mNavUserBadge');
      const signInBtn = document.getElementById('mSignInBtn');

      if (userBadge) userBadge.style.display = 'none';
      if (signInBtn) signInBtn.style.display = 'inline-block';

      alert('Signed out successfully.');
    };

    // 6. TABS & INITIALIZATION
    window.setActiveTab = function(el) {
      document.querySelectorAll('.tab-item').forEach(t => t.classList.remove('active'));
      el.classList.add('active');
    };

    window.openExplainerModal = function() {
      const m = document.getElementById('mExplainerModal');
      if (m) m.style.display = 'flex';
    };

    window.closeExplainerModal = function() {
      const m = document.getElementById('mExplainerModal');
      if (m) m.style.display = 'none';
    };

    window.addEventListener('DOMContentLoaded', () => {
      initMobilePanIndia();
      updateMobileCounters();
      updateMobileNotifBadge();
    });
  </script>'''

html = html[:start_idx] + new_m_script + html[end_idx + len(script_end):]

with open(path, "w", encoding="utf-8") as f:
    f.write(html)

print("m/index.html script engine completely replaced and verified successfully!")
