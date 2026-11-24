import os

path = r"C:\Users\PAUL\Documents\VitalSphere\public\m\index.html"
with open(path, "r", encoding="utf-8") as f:
    html = f.read()

target = "    // Explainer Modal"

fs_js = '''    // Fullscreen Mobile Directory Modal Logic (Blood Group Tap / Directory Pill Tap)
    window.mFsCurrentGroup = 'ALL';
    window.mFsCurrentTab = 'donors';

    window.openMobileFsDirectory = function(group = null) {
      window.mFsCurrentGroup = group || 'ALL';
      const modal = document.getElementById('mFullscreenDirectoryModal');
      if (modal) modal.style.display = 'flex';

      const title = document.getElementById('mFsModalTitle');
      const subtitle = document.getElementById('mFsModalSubtitle');
      if (title) {
        title.innerText = (group && group !== 'ALL') ? `Directory — Group ${group}` : 'Pan-India Directory';
      }
      if (subtitle) {
        subtitle.innerText = (group && group !== 'ALL') ? `Verified voluntary donors and patients for ${group}` : 'Verified Voluntary Donors & Active Patients';
      }

      // Update pills
      document.querySelectorAll('.m-grp-pill').forEach(btn => {
        const text = btn.innerText.trim();
        if ((group === null || group === 'ALL') && text === 'All Groups') {
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
      closeMobileFsDetail();
    };

    window.setMobileFsGroupFilter = function(grp, btnEl) {
      window.mFsCurrentGroup = grp;
      document.querySelectorAll('.m-grp-pill').forEach(b => b.classList.remove('active'));
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

      if (window.mFsCurrentTab === 'donors') {
        let list = window.fullDonorsList || [];
        if (window.mFsCurrentGroup && window.mFsCurrentGroup !== 'ALL') {
          list = list.filter(d => d.bloodGroup === window.mFsCurrentGroup);
        }
        if (q) {
          list = list.filter(d => 
            (d.name && d.name.toLowerCase().includes(q)) ||
            (d.district && d.district.toLowerCase().includes(q)) ||
            (d.id && d.id.toLowerCase().includes(q)) ||
            (d.bloodGroup && d.bloodGroup.toLowerCase().includes(q))
          );
        }

        const countEl = document.getElementById('mFsDonorsCount');
        if (countEl) countEl.innerText = list.length;

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
        let list = window.fullRecipientsList || [];
        if (window.mFsCurrentGroup && window.mFsCurrentGroup !== 'ALL') {
          list = list.filter(r => r.bloodGroup === window.mFsCurrentGroup);
        }
        if (q) {
          list = list.filter(r => 
            (r.patientName && r.patientName.toLowerCase().includes(q)) ||
            (r.district && r.district.toLowerCase().includes(q)) ||
            (r.hospital && r.hospital.toLowerCase().includes(q)) ||
            (r.id && r.id.toLowerCase().includes(q)) ||
            (r.bloodGroup && r.bloodGroup.toLowerCase().includes(q))
          );
        }

        const countEl = document.getElementById('mFsRecipientsCount');
        if (countEl) countEl.innerText = list.length;

        if (list.length === 0) {
          container.innerHTML = '<div style="text-align:center; padding:40px; color:var(--slate-400); font-size:0.85rem;">No recipients found for this selection.</div>';
          return;
        }

        list.forEach(r => {
          const card = document.createElement('div');
          card.className = 'm-clean-card';
          card.onclick = () => openMobileFsRecipientDetail(r.id);
          const isCommitted = r.status && r.status.includes('DONOR FOUND');
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
            <strong>Official Proofs:</strong> ${d.medicalProof || 'Registered Physician Certificate'} & ${d.groupProof || 'Clinical Pathology Report'}
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

    // Explainer Modal'''

if target in html:
    html = html.replace(target, fs_js, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Mobile fullscreen directory JS added successfully")
else:
    print("Target not found")
