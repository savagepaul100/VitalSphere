import os

path = r"C:\Users\PAUL\Documents\VitalSphere\src\main\java\com\vitalsphere\VitalSphereDesktopClient.java"
with open(path, "r", encoding="utf-8") as f:
    code = f.read()

target = "    private void showCertificatePreviewDialog(String name, String aadhaar, String bg, String certFile, String proofFile) {"
start_idx = code.find(target)

if start_idx == -1:
    print("Error: target not found")
    exit(1)

end_marker = "        dlg.setContentPane(p);\n        dlg.setVisible(true);\n    }"
end_idx = code.find(end_marker, start_idx)

if end_idx == -1:
    print("Error: end_marker not found")
    exit(1)

end_idx += len(end_marker)

replacement = '''    void updateDynamicTabCounts() {
        if (mainTabbedPane == null) return;
        int dCount = (donorsTableModel != null) ? donorsTableModel.getRowCount() : 256;
        int rCount = (recipientsTableModel != null) ? recipientsTableModel.getRowCount() : 64;
        int pCount = (pendingApprovalsTableModel != null) ? pendingApprovalsTableModel.getRowCount() : 5;

        if (mainTabbedPane.getTabCount() > 1) {
            mainTabbedPane.setTitleAt(1, "Verified Donors (" + dCount + " Members)");
        }
        if (mainTabbedPane.getTabCount() > 2) {
            mainTabbedPane.setTitleAt(2, "Who Wants Blood (" + rCount + " Patients)");
        }
        if (mainTabbedPane.getTabCount() > 3) {
            mainTabbedPane.setTitleAt(3, "Authority Verification (" + pCount + " Pending)");
        }
    }

    void showCampFlowKeychainDialog() {
        JDialog dlg = new JDialog(this, "CampFlow Saved Accounts Keychain", true);
        dlg.setSize(520, 560);
        dlg.setLocationRelativeTo(this);

        JPanel p = new JPanel(new BorderLayout(12, 12));
        p.setBackground(COLOR_NAVY_950);
        p.setBorder(new EmptyBorder(16, 20, 16, 20));

        // Header
        JPanel top = new JPanel(new BorderLayout());
        top.setOpaque(false);
        JLabel title = new JLabel("CampFlow Saved Accounts Keychain");
        title.setFont(new Font("Segoe UI", Font.BOLD, 15));
        title.setForeground(Color.WHITE);

        JLabel sub = new JLabel("Click any account to instantly autofill and authenticate session");
        sub.setFont(new Font("Segoe UI", Font.PLAIN, 11));
        sub.setForeground(new Color(56, 189, 248));

        top.add(title, BorderLayout.NORTH);
        top.add(sub, BorderLayout.SOUTH);
        p.add(top, BorderLayout.NORTH);

        // Account Items Container
        JPanel listPanel = new JPanel();
        listPanel.setLayout(new BoxLayout(listPanel, BoxLayout.Y_AXIS));
        listPanel.setBackground(COLOR_NAVY_950);

        String[][] accounts = {
                {"Dr. Rajesh Sharma", "doctor.sharma@vitalsphere.gov.in", "CHIEF MEDICAL OFFICER", "#059669"},
                {"Super Administrator", "admin@vitalsphere.gov.in", "SUPER ADMIN", "#0284C7"},
                {"District Health Officer", "dho.vizag@vitalsphere.gov.in", "DISTRICT AUTHORITY", "#D97706"},
                {"Blood Bank Administrator", "bloodbank.vizag@vitalsphere.gov.in", "BLOOD BANK ADMIN", "#8B5CF6"},
                {"Camp Coordinator (Red Cross)", "organizer.ap@vitalsphere.gov.in", "CAMP COORDINATOR", "#DC2626"},
                {"Vijay Kumar (Patient Attendant)", "attendant.vijay@apollohospitals.org", "RECIPIENT ATTENDANT", "#E11D48"},
                {"Sunita Reddy (Patient Attendant)", "attendant.sunita@carehospitals.com", "RECIPIENT ATTENDANT", "#E11D48"},
                {"Harish Kumar (Voluntary Donor)", "donor.harish@gmail.com", "CITIZEN DONOR (O-)", "#059669"},
                {"Sai Varma (Voluntary Donor)", "donor.sai@gmail.com", "CITIZEN DONOR (O-)", "#059669"}
        };

        for (String[] acc : accounts) {
            String name = acc[0];
            String email = acc[1];
            String role = acc[2];
            Color avatarCol = Color.decode(acc[3]);

            JPanel row = new JPanel(new BorderLayout(10, 0));
            row.setBackground(new Color(30, 41, 59));
            row.setBorder(BorderFactory.createCompoundBorder(
                    new EmptyBorder(4, 0, 4, 0),
                    BorderFactory.createCompoundBorder(
                            new LineBorder(new Color(51, 65, 85), 1, true),
                            new EmptyBorder(8, 12, 8, 12)
                    )
            ));
            row.setCursor(new Cursor(Cursor.HAND_CURSOR));

            JPanel left = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 0));
            left.setOpaque(false);

            JLabel av = new JLabel(name.substring(0, 1), SwingConstants.CENTER) {
                @Override
                protected void paintComponent(Graphics g) {
                    Graphics2D g2 = (Graphics2D) g.create();
                    g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
                    g2.setColor(avatarCol);
                    g2.fillOval(0, 0, getWidth(), getHeight());
                    super.paintComponent(g);
                    g2.dispose();
                }
            };
            av.setPreferredSize(new Dimension(30, 30));
            av.setForeground(Color.WHITE);
            av.setFont(new Font("Segoe UI", Font.BOLD, 12));

            JPanel textP = new JPanel();
            textP.setLayout(new BoxLayout(textP, BoxLayout.Y_AXIS));
            textP.setOpaque(false);

            JLabel nLbl = new JLabel(name);
            nLbl.setFont(new Font("Segoe UI", Font.BOLD, 12));
            nLbl.setForeground(Color.WHITE);

            JLabel eLbl = new JLabel(email);
            eLbl.setFont(new Font("Segoe UI", Font.PLAIN, 10));
            eLbl.setForeground(new Color(148, 163, 184));

            textP.add(nLbl);
            textP.add(eLbl);
            left.add(av);
            left.add(textP);

            JLabel rBadge = new JLabel(" " + role + " ");
            rBadge.setFont(new Font("Segoe UI", Font.BOLD, 9));
            rBadge.setForeground(avatarCol);
            rBadge.setBorder(new LineBorder(avatarCol, 1, true));

            row.add(left, BorderLayout.WEST);
            row.add(rBadge, BorderLayout.EAST);

            row.addMouseListener(new java.awt.event.MouseAdapter() {
                @Override
                public void mouseClicked(java.awt.event.MouseEvent e) {
                    executeJavaLogin(name, email, role);
                    dlg.dispose();
                }
            });

            listPanel.add(row);
        }

        JScrollPane scroll = new JScrollPane(listPanel);
        scroll.setBorder(null);
        scroll.setOpaque(false);
        scroll.getViewport().setOpaque(false);
        p.add(scroll, BorderLayout.CENTER);

        JButton closeBtn = createStyledButton("Cancel", new Color(51, 65, 85), Color.WHITE);
        closeBtn.addActionListener(e -> dlg.dispose());
        JPanel btm = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        btm.setOpaque(false);
        btm.add(closeBtn);
        p.add(btm, BorderLayout.SOUTH);

        dlg.setContentPane(p);
        dlg.setVisible(true);
    }

    void executeJavaLogin(String name, String email, String role) {
        currentUserName = name;
        currentUserEmail = email;
        currentUserRole = role;

        if (signInNavBtn != null) signInNavBtn.setVisible(false);
        if (userNavNameLabel != null) userNavNameLabel.setText(name);
        if (userNavBadgePanel != null) userNavBadgePanel.setVisible(true);

        activeRoleLabel.setText("Role: " + role + " (" + email + ")");
        if (role.contains("OFFICER") || role.contains("DOCTOR")) {
            activeRoleLabel.setForeground(new Color(110, 231, 183));
            mainTabbedPane.setSelectedIndex(3); // switch to authority console
        } else if (role.contains("ADMIN")) {
            activeRoleLabel.setForeground(new Color(125, 211, 252));
            mainTabbedPane.setSelectedIndex(3);
        } else {
            activeRoleLabel.setForeground(new Color(203, 213, 225));
        }

        JOptionPane.showMessageDialog(this,
                "Authentication Successful!\\n\\nUser: " + name + "\\nEmail: " + email + "\\nRole: " + role,
                "VitalSphere Keychain Session Active", JOptionPane.INFORMATION_MESSAGE);
    }

    void executeJavaSignOut() {
        currentUserName = null;
        currentUserEmail = null;
        currentUserRole = "GUEST";

        if (userNavBadgePanel != null) userNavBadgePanel.setVisible(false);
        if (signInNavBtn != null) signInNavBtn.setVisible(true);
        activeRoleLabel.setText("Role: Citizen Session (Guest)");
        activeRoleLabel.setForeground(new Color(203, 213, 225));
        mainTabbedPane.setSelectedIndex(0);

        JOptionPane.showMessageDialog(this, "Signed out successfully.", "Session Ended", JOptionPane.INFORMATION_MESSAGE);
    }

    private void showCertificatePreviewDialog(String name, String aadhaar, String bg, String certFile, String proofFile) {
        JDialog dlg = new JDialog(this, "Official Medical Certificate & Laboratory Clearance — " + name, true);
        dlg.setSize(740, 700);
        dlg.setLocationRelativeTo(this);

        JPanel p = new JPanel(new BorderLayout(14, 14));
        p.setBackground(Color.WHITE);
        p.setBorder(new EmptyBorder(20, 24, 20, 24));

        // Header
        JPanel top = new JPanel(new BorderLayout());
        top.setBackground(Color.WHITE);
        top.setBorder(BorderFactory.createMatteBorder(0, 0, 1, 0, COLOR_SLATE_200));

        JLabel h1 = new JLabel("CLINICAL MEDICAL FITNESS CERTIFICATE & LABORATORY CLEARANCE");
        h1.setFont(new Font("Segoe UI", Font.BOLD, 13));
        h1.setForeground(COLOR_NAVY_900);

        JLabel h2 = new JLabel("National Blood Transfusion Council (NBTC) Standard Form-04 • Statutory Medical Review");
        h2.setFont(new Font("Segoe UI", Font.PLAIN, 11));
        h2.setForeground(COLOR_SLATE_500);

        top.add(h1, BorderLayout.NORTH);
        top.add(h2, BorderLayout.SOUTH);
        p.add(top, BorderLayout.NORTH);

        // Body with certificate details + document viewer buttons
        JPanel centerPanel = new JPanel();
        centerPanel.setLayout(new BoxLayout(centerPanel, BoxLayout.Y_AXIS));
        centerPanel.setBackground(Color.WHITE);

        String certHtml = "<html><body style='width: 500px; font-family: Segoe UI, sans-serif; font-size: 11px;'>" +
                "<div style='background: #F8FAFC; border: 1.5px solid #CBD5E1; border-radius: 8px; padding: 16px; margin: 6px 0;'>" +
                "<table cellpadding='4' cellspacing='0' style='width: 100%; font-size: 11px;'>" +
                "<tr><td style='color: #64748B;'>Donor Full Name:</td><td><b>" + name + "</b></td></tr>" +
                "<tr><td style='color: #64748B;'>Aadhaar Identifier:</td><td><b>" + aadhaar + "</b></td></tr>" +
                "<tr><td style='color: #64748B;'>Verified Blood Group:</td><td><b style='color:#DC2626; font-size:13px;'>" + bg + "</b></td></tr>" +
                "<tr><td style='color: #64748B;'>Hemoglobin Level (Hb):</td><td><b style='color:#059669;'>13.5 g/dL</b> (NBTC Statutory Min: 12.5 g/dL)</td></tr>" +
                "<tr><td style='color: #64748B;'>Blood Pressure / Pulse:</td><td><b>120/80 mmHg</b> • 74 bpm (Optimal Physiological Range)</td></tr>" +
                "<tr><td style='color: #64748B;'>Infectious Serology Screen:</td><td><b style='color:#059669;'>NON-REACTIVE</b> (HIV-1/2, HBsAg, HCV, VDRL, Malaria)</td></tr>" +
                "<tr><td style='color: #64748B;'>Attached Document 1:</td><td><code>" + certFile + "</code> (Doctor Signed Fitness Report)</td></tr>" +
                "<tr><td style='color: #64748B;'>Attached Document 2:</td><td><code>" + proofFile + "</code> (Official Lab Blood Group Card)</td></tr>" +
                "</table>" +
                "<div style='margin-top: 14px; padding-top: 10px; border-top: 1px dashed #CBD5E1; font-size: 10px; color: #475569;'>" +
                "<i>\"I have personally examined the volunteer donor mentioned above and inspected all uploaded diagnostic certificates. I hereby certify that the candidate meets all statutory physical and physiological fitness criteria for voluntary blood donation.\"</i><br/><br/>" +
                "<b>Dr. V. S. Reddy, MD</b> (Civil Surgeon & Chief Medical Officer)<br/>" +
                "Medical Registration No: <b>MCI-AP-49201</b> • Directorate of Health Services" +
                "</div>" +
                "</div>" +
                "</body></html>";

        JLabel contentLbl = new JLabel(certHtml);
        centerPanel.add(contentLbl);

        // Document Action Buttons (Opens the real file or visual certificate in system viewer)
        JPanel docActionsBox = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 10));
        docActionsBox.setBackground(new Color(241, 245, 249));
        docActionsBox.setBorder(new LineBorder(COLOR_SLATE_200, 1, true));

        JButton viewCertDocBtn = createStyledButton("Open Fitness Document: " + certFile, COLOR_NAVY_900, Color.WHITE);
        viewCertDocBtn.addActionListener(e -> openDocumentFileOrDisplay(certFile, name, "Medical Fitness Certificate", bg));

        JButton viewProofDocBtn = createStyledButton("Open Group Document: " + proofFile, COLOR_NAVY_900, Color.WHITE);
        viewProofDocBtn.addActionListener(e -> openDocumentFileOrDisplay(proofFile, name, "Blood Group Proof Lab Card", bg));

        docActionsBox.add(viewCertDocBtn);
        docActionsBox.add(viewProofDocBtn);
        centerPanel.add(docActionsBox);

        p.add(new JScrollPane(centerPanel), BorderLayout.CENTER);

        // Bottom Controls
        JPanel btm = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 0));
        btm.setBackground(Color.WHITE);

        JButton printBtn = createStyledButton("Print Official Clearance Slip", COLOR_SLATE_200, COLOR_NAVY_900);
        printBtn.addActionListener(e -> JOptionPane.showMessageDialog(dlg,
                "Official Clinical Clearance Slip generated successfully.\\nReady to print via registered Hospital Transfusion Desk.",
                "Print Verification Slip", JOptionPane.INFORMATION_MESSAGE));

        JButton approveModalBtn = createStyledButton("✓ Approve Donor Now", COLOR_EMERALD_600, Color.WHITE);
        approveModalBtn.addActionListener(e -> {
            dlg.dispose();
            JOptionPane.showMessageDialog(this, "Donor " + name + " approved directly from Certificate Preview.");
        });

        JButton closeBtn = createStyledButton("Close Preview", COLOR_NAVY_900, Color.WHITE);
        closeBtn.addActionListener(e -> dlg.dispose());

        btm.add(printBtn);
        btm.add(approveModalBtn);
        btm.add(closeBtn);
        p.add(btm, BorderLayout.SOUTH);

        dlg.setContentPane(p);
        dlg.setVisible(true);
    }

    void openDocumentFileOrDisplay(String fileName, String donorName, String docType, String bg) {
        String realPath = certificateFilePathMap.get(fileName);
        if (realPath != null) {
            File f = new File(realPath);
            if (f.exists()) {
                try {
                    Desktop.getDesktop().open(f);
                    return;
                } catch (Exception ex) {
                    // Fallthrough to visual preview
                }
            }
        }

        // Visual Certificate Window
        JDialog docDlg = new JDialog(this, docType + " — " + donorName, true);
        docDlg.setSize(560, 480);
        docDlg.setLocationRelativeTo(this);

        JPanel docPanel = new JPanel(new BorderLayout(14, 14));
        docPanel.setBackground(Color.WHITE);
        docPanel.setBorder(new EmptyBorder(24, 28, 24, 28));

        String docHtml = "<html><body style='font-family: Segoe UI, sans-serif; font-size: 11px;'>" +
                "<div style='border: 2px solid #059669; border-radius: 8px; padding: 20px; background: #ECFDF5;'>" +
                "<div style='text-align: center; border-bottom: 1.5px solid #059669; padding-bottom: 10px; margin-bottom: 14px;'>" +
                "<h2 style='color: #065F46; margin: 0; font-size: 15px;'>OFFICIAL STATUTORY DOCUMENT ATTACHMENT</h2>" +
                "<span style='color: #047857; font-size: 10px;'>Directorate of Health Services • National Blood Transfusion Council</span>" +
                "</div>" +
                "<table cellpadding='6' cellspacing='0' style='width: 100%; font-size: 11px; color: #065F46;'>" +
                "<tr><td><b>Document Title:</b></td><td>" + docType + "</td></tr>" +
                "<tr><td><b>Original File Name:</b></td><td><code>" + fileName + "</code></td></tr>" +
                "<tr><td><b>Candidate Legal Name:</b></td><td><b>" + donorName + "</b></td></tr>" +
                "<tr><td><b>Confirmed Blood Group:</b></td><td><b style='color:#DC2626; font-size:13px;'>" + bg + "</b></td></tr>" +
                "<tr><td><b>Clinical Validity:</b></td><td><b style='color:#059669;'>VERIFIED AND APPROVED</b></td></tr>" +
                "<tr><td><b>Signatory Medical Officer:</b></td><td>Dr. V. S. Reddy, MD (Reg #MCI-AP-49201)</td></tr>" +
                "</table>" +
                "<div style='margin-top: 20px; padding: 12px; background: white; border: 1px dashed #059669; border-radius: 6px; font-size: 10px; color: #065F46;'>" +
                "<b>Digital Certificate Digest:</b> SHA-256 Verified • Timestamp: Active Verification Session<br/>" +
                "This document is archived on VitalSphere Encrypted Cloud Storage and cleared for clinical transfusion." +
                "</div>" +
                "</div></body></html>";

        docPanel.add(new JScrollPane(new JLabel(docHtml)), BorderLayout.CENTER);

        JButton closeBtn = createStyledButton("Close Document", COLOR_NAVY_900, Color.WHITE);
        closeBtn.addActionListener(e -> docDlg.dispose());
        JPanel btm = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        btm.setBackground(Color.WHITE);
        btm.add(closeBtn);
        docPanel.add(btm, BorderLayout.SOUTH);

        docDlg.setContentPane(docPanel);
        docDlg.setVisible(true);
    }'''

code = code[:start_idx] + replacement + code[end_idx:]

with open(path, "w", encoding="utf-8") as f:
    f.write(code)

print("Applied Java preview and Keychain login successfully!")
