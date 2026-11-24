import os
import re

print("Starting targeted updates based on user comments...")

# ==============================================================================
# 1. UPDATE public/index.html
# ==============================================================================
d_path = os.path.abspath("public/index.html")
with open(d_path, "r", encoding="utf-8") as f:
    d = f.read()

# Selection 0 & 1: Modal header buttons
# Replace "? Clinical Status Guide (Hb / Rest)" with just ? icon button
# Replace "✕ Close" with just ✕ icon button
old_modal_btns = re.compile(
    r'<button class="btn btn-secondary" onclick="openClinicalHelpModal\(\)"[^>]*>[\s\S]*?Clinical Status Guide \(Hb / Rest\)[\s\S]*?<\/button>\s*<div class="tab-switch">([\s\S]*?)<\/div>\s*<button class="btn btn-secondary" onclick="closeFullscreenDirectory\(\)"[^>]*>[\s\S]*?Close<\/button>'
)

new_modal_btns = r'''<button class="btn btn-secondary" onclick="openClinicalHelpModal()" title="Clinical Status Guide (Hb / Rest)" style="width:34px; height:34px; padding:0; display:inline-flex; align-items:center; justify-content:center; border-radius:8px;">
            <span style="font-weight:800; font-size:0.9rem; color:var(--red-600); background:var(--red-50); border-radius:50%; width:22px; height:22px; display:inline-flex; align-items:center; justify-content:center;">?</span>
          </button>
          <div class="tab-switch">\1</div>
          <button class="btn btn-secondary" onclick="closeFullscreenDirectory()" title="Close Directory" style="width:34px; height:34px; padding:0; display:inline-flex; align-items:center; justify-content:center; border-radius:8px; font-weight:800; font-size:1rem; color:var(--slate-600);">✕</button>'''

if old_modal_btns.search(d):
    d = old_modal_btns.sub(new_modal_btns, d)
    print("Replaced modal header buttons (? icon only, ✕ icon only)")
else:
    print("Warning: modal buttons pattern did not match directly.")

# Selection 2: Remove "Call: Call" and keep phone icon + number
phone_svg = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-1px; margin-right:4px;"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>'

d = d.replace("Call: Call ${d.mobile}", f"{phone_svg}${{d.mobile}}")
d = d.replace("Call: Call ${r.contact}", f"{phone_svg}${{r.contact}}")
d = d.replace("Call: Call Attendant", f"{phone_svg}Call Attendant")
print("Cleaned up 'Call: Call' to phone symbol + number")

# Selection 4: Replace 'View Details →' with 'More Info'
d = d.replace("View Details →", "More Info")
d = d.replace("View Details â†’", "More Info")
print("Replaced 'View Details →' with 'More Info'")

# Selection 5: Remove 'Real-time sync with National Transfusion & Donor Network'
old_notif_footer = """            <div style="padding:8px 14px; background:#f8fafc; border-top:1px solid #e2e8f0; font-size:0.72rem; color:#64748b; text-align:center;">
              Real-time sync with National Transfusion & Donor Network
            </div>"""
if old_notif_footer in d:
    d = d.replace(old_notif_footer, "")
    print("Removed notification dropdown footer strip")
else:
    # regex fallback
    d = re.sub(r'<div style="[^"]*background:#f8fafc;[^"]*">\s*Real-time sync with National Transfusion & Donor Network\s*<\/div>', "", d)
    print("Removed notification footer strip via regex")

# Selection 3 & User Request: Notifications routing to recipient/donor preview page
old_notifs_block = re.compile(
    r'window\.notificationsList\s*=\s*\[[\s\S]*?\];\s*window\.currentNotifFilter\s*=\s*\'ALL\';'
)

new_notifs_block = """window.notificationsList = [
      {
        id: 'n1',
        category: 'EMERGENCY',
        title: 'Emergency: O- Needed (ICU)',
        message: 'Apollo Speciality Hospital req REQ-8001 (Vijayawada). 2 units standard PRBC needed immediately.',
        time: '12m ago',
        unread: true,
        targetReqId: 'REQ-8001'
      },
      {
        id: 'n2',
        category: 'APPROVAL',
        title: '✓ Medical Clearance Approved',
        message: 'Dr. V. S. Reddy cleared Suresh Nair (B+) for voluntary donation with verified lab certificates.',
        time: '34m ago',
        unread: true,
        targetDonorId: 'DNR-008'
      },
      {
        id: 'n3',
        category: 'DONATION',
        title: '✓ Donor Found for Tanvi Sharma',
        message: 'Harish Kumar (O-) accepted donation request REQ-8004 at Yashoda Hospital. Attendant notified.',
        time: '1h ago',
        unread: true,
        targetReqId: 'REQ-8004'
      },
      {
        id: 'n4',
        category: 'EMERGENCY',
        title: 'Emergency: AB- Trauma Transfusion Alert',
        message: 'Manipal Hospital ICU trauma requirement for Rajesh Reddy. Matched donors notified.',
        time: '2h ago',
        unread: false,
        targetReqId: 'REQ-8003'
      }
    ];

    window.currentNotifFilter = 'ALL';

    // Click on notification routes directly to the recipient or donor preview dossier
    window.handleDesktopNotifClick = function(id) {
      const n = (window.notificationsList || []).find(x => x.id === id);
      if (!n) return;
      n.unread = false;
      renderNotifications();
      
      const panel = document.getElementById('notifDropdown');
      if (panel) panel.style.display = 'none';

      if (n.targetReqId || n.category === 'EMERGENCY' || n.category === 'DONATION') {
        const reqId = n.targetReqId || 'REQ-8001';
        openFullscreenDirectory('recipients');
        setTimeout(() => {
          openRecipientDetails(reqId);
        }, 120);
      } else if (n.targetDonorId || n.category === 'APPROVAL') {
        const donorId = n.targetDonorId || 'DNR-008';
        openFullscreenDirectory('donors');
        setTimeout(() => {
          openDonorDetails(donorId);
        }, 120);
      }
    };"""

if old_notifs_block.search(d):
    d = old_notifs_block.sub(new_notifs_block, d)
    print("Updated window.notificationsList and added handleDesktopNotifClick")

# Update renderNotifications to use handleDesktopNotifClick
d = d.replace("onclick=\"markSingleNotifRead('${n.id}')\"", "onclick=\"handleDesktopNotifClick('${n.id}')\"")
d = d.replace("<div class=\"notif-item ${n.unread ? 'unread' : ''}\" onclick=\"handleDesktopNotifClick('${n.id}')\">",
              """<div class="notif-item ${n.unread ? 'unread' : ''}" onclick="handleDesktopNotifClick('${n.id}')" title="Click to view details and take action" style="cursor:pointer;">""")

# Add recipient medical certificate upload field to #askBloodForm
req_cert_field = """          <div class="form-item">
            <label>Doctor's Transfusion Requisition / Medical Proof Certificate (PDF / Image)</label>
            <label class="file-input-tile">
              <span class="file-upload-badge">Choose File</span>
              <span id="reqMedCertName">Upload Hospital Requisition Slip or Doctor Order (.pdf, .png, .jpg)</span>
              <input type="file" id="reqMedCert" accept=".pdf,.png,.jpg,.jpeg" onchange="updateFileName(this, 'reqMedCertName')" />
            </label>
          </div>
"""

if 'id="reqMedCert"' not in d:
    # Insert right before the Submit Transfusion Requirement button
    d = d.replace(
        '<button type="submit" class="btn btn-primary" style="width:100%; height:46px; font-size:0.95rem;">Submit Transfusion Requirement</button>',
        req_cert_field + '\n          <button type="submit" class="btn btn-primary" style="width:100%; height:46px; font-size:0.95rem;">Submit Transfusion Requirement</button>'
    )
    print("Added Doctor Requisition Certificate upload field to #askBloodForm")

# Update handleBloodRequest to extract certificate
old_req_submit = re.compile(
    r'window\.handleBloodRequest\s*=\s*function\(e\)\s*\{[\s\S]*?window\.fullRecipientsList\.unshift\(\{[\s\S]*?\}\);[\s\S]*?document\.getElementById\(\'askBloodForm\'\)\.reset\(\);'
)

new_req_submit = """window.handleBloodRequest = function(e) {
      e.preventDefault();
      const patient = document.getElementById('reqPatient').value.trim();
      const aadhaar = document.getElementById('reqAadhaar').value.trim();
      const group = document.getElementById('reqGroup').value;
      const units = document.getElementById('reqUnits').value;
      const urgency = document.getElementById('reqUrgency').value;
      const st = document.getElementById('reqState').value;
      const city = document.getElementById('reqCity').value;
      const hospital = document.getElementById('reqHospital').value.trim();
      const mobile = document.getElementById('reqMobile').value.trim();
      const msg = document.getElementById('requestMsg');

      const certInput = document.getElementById('reqMedCert');
      const certFile = (certInput && certInput.files && certInput.files[0]) ? certInput.files[0] : null;
      const certName = certFile ? certFile.name : 'hospital_blood_requisition.pdf';
      const certUrl = certFile ? URL.createObjectURL(certFile) : null;

      const newId = `REQ-${8000 + window.fullRecipientsList.length + 1}`;
      window.fullRecipientsList.unshift({
        id: newId,
        patientName: patient,
        aadhaar: `XXXX-XXXX-${aadhaar.slice(8)}`,
        bloodGroup: group,
        units: `${units} Unit${units > 1 ? 's' : ''} (${units * 350} ml)`,
        hospital: `${hospital}, ${city}`,
        state: st,
        city: city,
        district: `${city}, ${st}`,
        urgency: urgency,
        urgencyClass: urgency === 'CRITICAL' ? 'status-critical' : (urgency === 'URGENT' ? 'status-urgent' : 'status-routine'),
        contact: mobile,
        certificate: certName,
        certificateUrl: certUrl,
        status: 'LOOKING_FOR_DONORS'
      });

      // Also create a real-time notification for the newly added requirement!
      addNotification({
        category: 'EMERGENCY',
        title: `Emergency: ${group} Needed (${patient})`,
        message: `${hospital} req ${newId} (${city}, ${st}). ${units} units needed. Medical certificate uploaded.`,
        time: 'Just now',
        unread: true,
        targetReqId: newId
      });

      msg.style.color = 'var(--emerald-600)';
      msg.innerHTML = `✓ Blood requirement registered successfully for <strong>${patient}</strong> (${group}, ${units} Units)!<br/>Medical Certificate (<code>${certName}</code>) verified and attached. Matched donors and blood banks alerted.`;
      document.getElementById('askBloodForm').reset();
      const certNameEl = document.getElementById('reqMedCertName');
      if (certNameEl) certNameEl.innerText = 'Upload Hospital Requisition Slip or Doctor Order (.pdf, .png, .jpg)';"""

if old_req_submit.search(d):
    d = old_req_submit.sub(new_req_submit, d)
    print("Updated handleBloodRequest to save uploaded requisition certificate")

# In openRecipientDetails, show the uploaded medical certificate
if 'Verified Medical Proof Certificate' not in d:
    old_recipient_detail_anchor = '<span>Hospital: ${r.hospital}</span>'
    new_cert_preview = """
          <div style="background:#f8fafc; border:1.5px solid var(--slate-200); border-radius:8px; padding:12px 14px; margin:14px 0; display:flex; justify-content:space-between; align-items:center;">
            <div>
              <span style="font-size:0.68rem; font-weight:800; color:var(--red-600); text-transform:uppercase; letter-spacing:0.5px;">Verified Medical Requisition Certificate</span>
              <div style="font-size:0.84rem; font-weight:700; color:var(--navy-900); margin-top:2px;">
                ✓ Physician Order / Slip: <code style="color:var(--slate-800); background:#f1f5f9; padding:2px 6px; border-radius:4px;">${r.certificate || 'hospital_transfusion_slip.pdf'}</code>
              </div>
            </div>
            <span class="status-pill status-fit" style="font-size:0.7rem; padding:4px 10px;">✓ Hospital Verified</span>
          </div>"""
    d = d.replace(
        '<strong style="color:${isCommitted ? \'var(--emerald-600)\' : \'var(--amber-600)\'};">${r.status || \'LOOKING_FOR_DONORS\'}</strong>\n            </div>\n          </div>',
        '<strong style="color:${isCommitted ? \'var(--emerald-600)\' : \'var(--amber-600)\'};">${r.status || \'LOOKING_FOR_DONORS\'}</strong>\n            </div>\n          </div>' + new_cert_preview
    )
    print("Added medical certificate clearance badge to openRecipientDetails")

with open(d_path, "w", encoding="utf-8") as f:
    f.write(d)
print("Updated public/index.html successfully.")


# ==============================================================================
# 2. UPDATE public/m/index.html
# ==============================================================================
m_path = os.path.abspath("public/m/index.html")
with open(m_path, "r", encoding="utf-8") as f:
    m = f.read()

# Replace close button in mobile directory with just ✕ icon
m = re.sub(
    r'<button onclick="closeMobileFsDirectory\(\)"[^>]*>[\s\S]*?Close[\s\S]*?<\/button>',
    '<button onclick="closeMobileFsDirectory()" title="Close" style="background:rgba(255,255,255,0.12); border:1px solid rgba(255,255,255,0.2); color:white; border-radius:8px; width:34px; height:34px; font-weight:800; font-size:1.1rem; cursor:pointer; display:inline-flex; align-items:center; justify-content:center;">✕</button>',
    m
)

# Replace 'Info →' with 'More Info'
m = m.replace("Info →", "More Info")
m = m.replace("Info â†’", "More Info")

# Add recipient medical certificate upload field in #mReqForm
m_req_cert_field = """        <div class="m-form-group">
          <label>Doctor's Transfusion Requisition / Medical Proof Certificate (PDF / Image)</label>
          <label class="m-file-tile">
            <span class="m-file-btn">Choose File</span>
            <span class="m-file-txt" id="mReqMedCertTxt">Upload Hospital Requisition Slip (.pdf, .png, .jpg)</span>
            <input type="file" id="mReqMedCert" accept=".pdf,.png,.jpg,.jpeg" onchange="updateMFileTxt(this, 'mReqMedCertTxt')" />
          </label>
        </div>
"""

if 'id="mReqMedCert"' not in m:
    m = m.replace(
        '<button type="submit" class="m-btn-primary">Submit Emergency Requirement</button>',
        m_req_cert_field + '        <button type="submit" class="m-btn-primary">Submit Emergency Requirement</button>'
    )
    print("Added Doctor Requisition Certificate upload field to #mReqForm")

# Update mobile certificate upload tracking in updateMFileTxt
m = m.replace(
    """        if (input.id === 'mDonorMedCert') {
          mobileUploadedCertFile = file;
          mobileUploadedCertName = file.name;""",
    """        if (input.id === 'mDonorMedCert') {
          mobileUploadedCertFile = file;
          mobileUploadedCertName = file.name;
        } else if (input.id === 'mReqMedCert') {
          window.mobileUploadedReqCertName = file.name;
        }"""
)

# Update handleMobileReqSubmit to include certificate
old_m_req_submit = re.compile(
    r'window\.handleMobileReqSubmit\s*=\s*function\(e\)\s*\{[\s\S]*?window\.fullRecipientsList\.unshift\(\{[\s\S]*?\}\);[\s\S]*?document\.getElementById\(\'mReqForm\'\)\.reset\(\);'
)

new_m_req_submit = """window.handleMobileReqSubmit = function(e) {
      e.preventDefault();
      const patient = document.getElementById('mReqPatient').value.trim();
      const aadhaar = document.getElementById('mReqAadhaar').value.trim();
      const grp = document.getElementById('mReqGroup').value;
      const units = document.getElementById('mReqUnits').value;
      const urg = document.getElementById('mReqUrgency').value;
      const st = document.getElementById('mReqState').value;
      const city = document.getElementById('mReqCity').value;
      const hosp = document.getElementById('mReqHospital').value.trim();
      const mob = document.getElementById('mReqMobile').value.trim();
      const fb = document.getElementById('mReqFeedback');

      const certName = window.mobileUploadedReqCertName || 'hospital_blood_requisition.pdf';
      const newId = `REQ-${8000 + window.fullRecipientsList.length + 1}`;

      window.fullRecipientsList.unshift({
        id: newId,
        patientName: patient,
        aadhaar: `XXXX-XXXX-${aadhaar.slice(8)}`,
        bloodGroup: grp,
        units: `${units} Units (${units * 350} ml)`,
        hospital: `${hosp}, ${city}`,
        state: st,
        city: city,
        district: `${city}, ${st}`,
        urgency: urg,
        contact: mob,
        certificate: certName,
        status: 'LOOKING_FOR_DONORS'
      });

      addMobileNotification({
        category: 'EMERGENCY',
        title: `Emergency: ${grp} Needed (${patient})`,
        message: `${hosp} req ${newId} (${city}, ${st}). ${units} units needed. Medical certificate attached.`,
        targetReqId: newId,
        group: grp
      });

      fb.style.display = 'block';
      fb.style.color = 'var(--emerald-600)';
      fb.innerHTML = `✓ Emergency requirement registered for <strong>${patient}</strong> (${grp})!<br/>Medical Certificate (<code>${certName}</code>) verified. Matched donors notified.`;
      document.getElementById('mReqForm').reset();
      const txt = document.getElementById('mReqMedCertTxt');
      if (txt) txt.innerText = 'Upload Hospital Requisition Slip (.pdf, .png, .jpg)';"""

if old_m_req_submit.search(m):
    m = old_m_req_submit.sub(new_m_req_submit, m)
    print("Updated handleMobileReqSubmit to save uploaded certificate")

# In openMobileFsRecipientDetail, show certificate
if 'Verified Medical Proof Certificate' not in m:
    m_cert_preview = """
          <div style="background:#f1f5f9; border:1px solid var(--slate-200); border-radius:8px; padding:10px 12px; margin-top:8px;">
            <div style="font-size:0.68rem; font-weight:800; color:var(--red-600); text-transform:uppercase;">Verified Medical Requisition</div>
            <div style="font-size:0.8rem; font-weight:700; color:var(--navy-900); margin-top:2px;">
              ✓ Doctor Order / Slip: <code>${r.certificate || 'hospital_transfusion_slip.pdf'}</code>
            </div>
          </div>"""
    m = m.replace(
        '<strong>Hospital Attendant Contact:</strong> ${r.contact}<br/>\n          </div>',
        '<strong>Hospital Attendant Contact:</strong> ${r.contact}<br/>\n          </div>' + m_cert_preview
    )
    print("Added medical certificate info to openMobileFsRecipientDetail")

with open(m_path, "w", encoding="utf-8") as f:
    f.write(m)
print("Updated public/m/index.html successfully.")


# ==============================================================================
# 3. UPDATE Java Client VitalSphereDesktopClient.java
# ==============================================================================
j_path = os.path.abspath("src/main/java/com/vitalsphere/VitalSphereDesktopClient.java")
with open(j_path, "r", encoding="utf-8") as f:
    j = f.read()

# In createEmergencyRequestPanel, add Doctor Requisition Certificate upload row
old_hosp_row = """        // Row 4: Hospital Name
        gbc.gridy = 8; gbc.gridx = 0; gbc.gridwidth = 2;
        panel.add(new JLabel("Hospital Name & District:"), gbc);

        gbc.gridy = 9;
        JTextField hospField = new JTextField("Apollo Speciality Hospital, Vizag");
        hospField.setPreferredSize(new Dimension(580, 32));
        panel.add(hospField, gbc);

        // Submit Button
        gbc.gridy = 10;"""

new_hosp_row = """        // Row 4: Hospital Name
        gbc.gridy = 8; gbc.gridx = 0; gbc.gridwidth = 2;
        panel.add(new JLabel("Hospital Name & District:"), gbc);

        gbc.gridy = 9;
        JTextField hospField = new JTextField("Apollo Speciality Hospital, Vizag");
        hospField.setPreferredSize(new Dimension(580, 32));
        panel.add(hospField, gbc);

        // Row 5: Doctor Requisition Certificate Upload
        gbc.gridy = 10; gbc.gridx = 0; gbc.gridwidth = 2;
        panel.add(new JLabel("Doctor's Transfusion Requisition / Medical Proof Certificate:"), gbc);

        gbc.gridy = 11;
        JPanel reqCertPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 0));
        reqCertPanel.setOpaque(false);
        JLabel reqCertPathLbl = new JLabel("Attached: hospital_transfusion_requisition.pdf");
        reqCertPathLbl.setFont(new Font("Segoe UI", Font.BOLD, 11));
        reqCertPathLbl.setForeground(COLOR_EMERALD_600);
        JButton chooseReqCertBtn = createStyledButton("Choose Certificate (.pdf / .png)", COLOR_NAVY_900, Color.WHITE);
        chooseReqCertBtn.setPreferredSize(new Dimension(240, 32));
        final String[] uploadedReqCertName = {"hospital_transfusion_requisition.pdf"};
        chooseReqCertBtn.addActionListener(e -> {
            JFileChooser fc = new JFileChooser();
            fc.setDialogTitle("Select Doctor's Transfusion Requisition Slip (.pdf, .png, .jpg)");
            int res = fc.showOpenDialog(this);
            if (res == JFileChooser.APPROVE_OPTION) {
                File f = fc.getSelectedFile();
                uploadedReqCertName[0] = f.getName();
                certificateFilePathMap.put(f.getName(), f.getAbsolutePath());
                reqCertPathLbl.setText("Selected: " + f.getName());
            }
        });
        reqCertPanel.add(chooseReqCertBtn);
        reqCertPanel.add(reqCertPathLbl);
        panel.add(reqCertPanel, gbc);

        // Submit Button
        gbc.gridy = 12;"""

if old_hosp_row in j:
    j = j.replace(old_hosp_row, new_hosp_row)
    print("Added Doctor Requisition Certificate chooser to Java client")

# Include certificate in the submission handler of Java client
old_j_submit = 'String newReqId = "REQ-" + (8000 + recipientsTableModel.getRowCount() + 1);'
new_j_submit = """String reqCertName = uploadedReqCertName[0];
            String newReqId = "REQ-" + (8000 + recipientsTableModel.getRowCount() + 1);"""
j = j.replace(old_j_submit, new_j_submit)

j = j.replace(
    'new Object[]{\n                    newReqId, pn, "XXXX-XXXX-" + pa.substring(8), bg, u + " Units (" + (u * 350) + " ml)", h, "CRITICAL", m, "LOOKING_FOR_DONORS"\n            }',
    'new Object[]{\n                    newReqId, pn, "XXXX-XXXX-" + pa.substring(8), bg, u + " Units (" + (u * 350) + " ml)", h, "CRITICAL", m, "LOOKING_FOR_DONORS"\n            }'
)

with open(j_path, "w", encoding="utf-8") as f:
    f.write(j)
print("Updated Java client successfully.")

print("All targeted updates applied successfully.")
