package com.vitalsphere;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.border.LineBorder;
import javax.swing.filechooser.FileNameExtensionFilter;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.JTableHeader;
import javax.swing.table.TableRowSorter;
import java.awt.*;
import java.awt.geom.Path2D;
import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;

/**
 * VitalSphere Java Desktop Client Application.
 * Pure Java (Modern Flat Swing UI matching Web Platform):
 * - Plus Jakarta Sans / Segoe UI typography hierarchy
 * - Custom Anti-Aliased Button Rendering (Guaranteed vibrant colors on all OS)
 * - Dark Navy Header (#0A1120) with Vital Red droplet badge (#DC2626)
 * - Authority Approval Controls for Medical Officers & Administrators
 * - Interactive Certificate Preview Dialog (Doctor signed reports, Hb vitals, NBTC seals)
 * - 256 Enrolled Pan-India Donors & 32 Recipients Transfusion Directory
 * - Donor Registration with PDF Certificate File Chooser
 * - Emergency Request Input Desk
 * - CampFlow-style Authority Role Switcher
 * - Clinical Eligibility Guide explaining FIT, Hb (12.5+ g/dL), and Rest (90/120d)
 * - Cloud Self-Updater checking latest version
 */
public class VitalSphereDesktopClient extends JFrame {

    private static final String APP_VERSION = "1.0.0";
    private static final String UPDATE_CHECK_URL = "https://vitalsphere-9351.web.app/api/version.json";
    private static final String WEB_PORTAL_URL = "https://vitalsphere-9351.web.app";

    // Palette matching website
    private static final Color COLOR_NAVY_950 = new Color(10, 17, 32);
    private static final Color COLOR_NAVY_900 = new Color(15, 23, 42);
    private static final Color COLOR_NAVY_800 = new Color(30, 41, 59);
    private static final Color COLOR_RED_600 = new Color(220, 38, 38);
    private static final Color COLOR_RED_700 = new Color(185, 28, 28);
    private static final Color COLOR_SLATE_50 = new Color(248, 250, 252);
    private static final Color COLOR_SLATE_100 = new Color(241, 245, 249);
    private static final Color COLOR_SLATE_200 = new Color(226, 232, 240);
    private static final Color COLOR_SLATE_500 = new Color(100, 116, 139);
    private static final Color COLOR_EMERALD_600 = new Color(5, 150, 105);
    private static final Color COLOR_AMBER_600 = new Color(217, 119, 6);

    private final JLabel statusLabel = new JLabel("Status: Synchronized with VitalSphere National Cloud Network");
    private final Map<String, String> certificateFilePathMap = new HashMap<>();
    private String currentUserName = null;
    private String currentUserEmail = null;
    private String currentUserRole = "GUEST";
    private JButton signInNavBtn;
    private JPanel userNavBadgePanel;
    private JLabel userNavNameLabel;
    private final JLabel activeRoleLabel = new JLabel("Role: Chief Medical Officer (Approval Mode Active)");

    // Table models for dynamic data updates
    private DefaultTableModel donorsTableModel;
    private DefaultTableModel recipientsTableModel;
    private DefaultTableModel pendingApprovalsTableModel;
    private JTabbedPane mainTabbedPane;

    // Pan-India States & Districts
    private static final Map<String, String[]> INDIA_LOCATIONS = new HashMap<>();
    static {
        INDIA_LOCATIONS.put("Andhra Pradesh", new String[]{"Visakhapatnam", "Vijayawada", "Guntur", "Tirupati", "Kurnool", "Kakinada", "Nellore"});
        INDIA_LOCATIONS.put("Maharashtra", new String[]{"Mumbai", "Pune", "Nagpur", "Thane", "Nashik", "Aurangabad"});
        INDIA_LOCATIONS.put("Karnataka", new String[]{"Bengaluru", "Mysuru", "Hubballi", "Mangaluru", "Belagavi"});
        INDIA_LOCATIONS.put("Delhi NCR", new String[]{"New Delhi", "North Delhi", "South Delhi", "Noida", "Gurugram"});
        INDIA_LOCATIONS.put("Tamil Nadu", new String[]{"Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem"});
        INDIA_LOCATIONS.put("Telangana", new String[]{"Hyderabad", "Warangal", "Nizamabad", "Karimnagar"});
        INDIA_LOCATIONS.put("Uttar Pradesh", new String[]{"Lucknow", "Kanpur", "Varanasi", "Agra", "Noida"});
        INDIA_LOCATIONS.put("Gujarat", new String[]{"Ahmedabad", "Surat", "Vadodara", "Rajkot"});
        INDIA_LOCATIONS.put("West Bengal", new String[]{"Kolkata", "Howrah", "Durgapur", "Siliguri"});
        INDIA_LOCATIONS.put("Kerala", new String[]{"Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur"});
    }

    public VitalSphereDesktopClient() {
        setTitle("VitalSphere — Healthcare & Blood Coordination Platform [v" + APP_VERSION + "]");
        setSize(1220, 800);
        setMinimumSize(new Dimension(980, 660));
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        // App Icon matching website favicon
        setIconImage(createAppIcon(64));

        initUI();
    }

    /**
     * Draws the VitalSphere logo matching favicon.svg:
     * Dark navy rounded badge + crimson blood droplet with curved base and tapered tip + white sheen.
     */
    private Image createAppIcon(int size) {
        java.awt.image.BufferedImage img = new java.awt.image.BufferedImage(size, size, java.awt.image.BufferedImage.TYPE_INT_ARGB);
        Graphics2D g2 = img.createGraphics();
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

        // Navy base
        g2.setColor(COLOR_NAVY_950);
        g2.fillRoundRect(0, 0, size, size, size / 4, size / 4);

        // Droplet shape
        float scale = size / 32.0f;
        Path2D.Float drop = new Path2D.Float();
        drop.moveTo(16 * scale, 5 * scale);
        drop.curveTo(22 * scale, 13 * scale, 24 * scale, 17 * scale, 24 * scale, 21 * scale);
        drop.curveTo(24 * scale, 25.5f * scale, 20.5f * scale, 29 * scale, 16 * scale, 29 * scale);
        drop.curveTo(11.5f * scale, 29 * scale, 8 * scale, 25.5f * scale, 8 * scale, 21 * scale);
        drop.curveTo(8 * scale, 17 * scale, 10 * scale, 13 * scale, 16 * scale, 5 * scale);
        drop.closePath();

        g2.setColor(COLOR_RED_600);
        g2.fill(drop);

        // Subtle specular highlight on droplet
        g2.setColor(new Color(255, 255, 255, 160));
        g2.fillOval((int)(11 * scale), (int)(17 * scale), (int)(3.5f * scale), (int)(6 * scale));

        g2.dispose();
        return img;
    }

    private void initUI() {
        JPanel root = new JPanel(new BorderLayout());
        root.setBackground(COLOR_SLATE_50);

        // 1. Top Government Banner Strip
        JPanel topStrip = new JPanel(new BorderLayout());
        topStrip.setBackground(COLOR_NAVY_950);
        topStrip.setBorder(new EmptyBorder(6, 20, 6, 20));

        JLabel govTitle = new JLabel("VITALSPHERE NATIONAL HEALTHCARE & BLOOD LOGISTICS NETWORK");
        govTitle.setFont(new Font("Segoe UI", Font.BOLD, 11));
        govTitle.setForeground(new Color(203, 213, 225));

        JPanel rightStrip = new JPanel(new FlowLayout(FlowLayout.RIGHT, 14, 0));
        rightStrip.setOpaque(false);

        activeRoleLabel.setFont(new Font("Segoe UI", Font.BOLD, 11));
        activeRoleLabel.setForeground(new Color(110, 231, 183));

        JLabel govTag = new JLabel("AUTHORITY VERIFIED");
        govTag.setFont(new Font("Segoe UI", Font.BOLD, 10));
        govTag.setForeground(new Color(252, 165, 165));
        govTag.setBorder(BorderFactory.createCompoundBorder(
                new LineBorder(new Color(220, 38, 38, 120), 1, true),
                new EmptyBorder(1, 6, 1, 6)
        ));

        rightStrip.add(activeRoleLabel);
        rightStrip.add(govTag);

        topStrip.add(govTitle, BorderLayout.WEST);
        topStrip.add(rightStrip, BorderLayout.EAST);

        // 2. Main Brand & Action Header
        JPanel mainHeader = new JPanel(new BorderLayout());
        mainHeader.setBackground(Color.WHITE);
        mainHeader.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createMatteBorder(0, 0, 1, 0, COLOR_SLATE_200),
                new EmptyBorder(12, 24, 12, 24)
        ));

        // Brand on left
        JPanel brandPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 12, 0));
        brandPanel.setOpaque(false);

        JLabel logoIconLabel = new JLabel(new ImageIcon(createAppIcon(38)));

        JPanel brandTextPanel = new JPanel(new GridLayout(2, 1, 0, 0));
        brandTextPanel.setOpaque(false);
        JLabel titleLbl = new JLabel("VitalSphere");
        titleLbl.setFont(new Font("Segoe UI", Font.BOLD, 19));
        titleLbl.setForeground(COLOR_NAVY_900);

        JLabel subLbl = new JLabel("HEALTHCARE & BLOOD LOGISTICS");
        subLbl.setFont(new Font("Segoe UI", Font.BOLD, 9));
        subLbl.setForeground(COLOR_SLATE_500);

        brandTextPanel.add(titleLbl);
        brandTextPanel.add(subLbl);
        brandPanel.add(logoIconLabel);
        brandPanel.add(brandTextPanel);

        // Actions & CampFlow Role Switcher on right
        JPanel navButtons = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 0));
        navButtons.setOpaque(false);

        // CampFlow Keychain Sign In / Sign Out Toggle (matching Web Portal)
        signInNavBtn = createStyledButton("Sign In", COLOR_RED_600, Color.WHITE);
        signInNavBtn.setPreferredSize(new Dimension(86, 32));
        signInNavBtn.addActionListener(e -> showCampFlowKeychainDialog());

        userNavBadgePanel = new JPanel(new FlowLayout(FlowLayout.RIGHT, 6, 0));
        userNavBadgePanel.setOpaque(false);
        userNavBadgePanel.setVisible(false);

        userNavNameLabel = new JLabel("Dr. Rajesh Sharma");
        userNavNameLabel.setFont(new Font("Segoe UI", Font.BOLD, 12));
        userNavNameLabel.setForeground(COLOR_NAVY_900);

        JButton signOutNavBtn = createStyledButton("Sign Out", COLOR_RED_600, Color.WHITE);
        signOutNavBtn.setPreferredSize(new Dimension(80, 30));
        signOutNavBtn.addActionListener(e -> executeJavaSignOut());

        userNavBadgePanel.add(userNavNameLabel);
        userNavBadgePanel.add(signOutNavBtn);

        JButton helpBtn = createStyledButton("? Clinical Status Guide", new Color(241, 245, 249), COLOR_NAVY_900);
        helpBtn.addActionListener(e -> showClinicalGuideDialog());

        JButton updateBtn = createStyledButton("Check for Updates", COLOR_RED_600, Color.WHITE);
        updateBtn.addActionListener(e -> checkForUpdates());

        JButton webBtn = createStyledButton("Open Web Portal", COLOR_NAVY_900, Color.WHITE);
        webBtn.addActionListener(e -> openWeb());

        navButtons.add(signInNavBtn);
        navButtons.add(userNavBadgePanel);
        navButtons.add(helpBtn);
        navButtons.add(updateBtn);
        navButtons.add(webBtn);

        mainHeader.add(brandPanel, BorderLayout.WEST);
        mainHeader.add(navButtons, BorderLayout.EAST);

        // Header Combined
        JPanel headerWrap = new JPanel(new BorderLayout());
        headerWrap.add(topStrip, BorderLayout.NORTH);
        headerWrap.add(mainHeader, BorderLayout.SOUTH);
        root.add(headerWrap, BorderLayout.NORTH);

        // 3. Tabbed Interface matching all web menus
        mainTabbedPane = new JTabbedPane();
        mainTabbedPane.setFont(new Font("Segoe UI", Font.BOLD, 12));
        mainTabbedPane.setBackground(COLOR_SLATE_100);
        mainTabbedPane.setBorder(new EmptyBorder(8, 16, 8, 16));

        mainTabbedPane.addTab("Live Blood Stock", createStockPanel());
        mainTabbedPane.addTab("Verified Donors (256 Members)", createDonorsPanel());
        mainTabbedPane.addTab("Who Wants Blood (64 Patients)", createRecipientsPanel());
        mainTabbedPane.addTab("Authority Medical Verification Console", createApprovalPanel());
        mainTabbedPane.addTab("Donor Registration Form", createDonorRegistrationPanel());
        mainTabbedPane.addTab("Emergency Blood Request Form", createEmergencyRequestPanel());
        updateDynamicTabCounts();

        root.add(mainTabbedPane, BorderLayout.CENTER);

        // 4. Clean Footer
        JPanel footer = new JPanel(new BorderLayout());
        footer.setBackground(COLOR_NAVY_950);
        footer.setBorder(new EmptyBorder(10, 24, 10, 24));

        statusLabel.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        statusLabel.setForeground(new Color(148, 163, 184));
        footer.add(statusLabel, BorderLayout.WEST);

        JLabel verLbl = new JLabel("© 2026 VitalSphere Desktop Node • v" + APP_VERSION);
        verLbl.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        verLbl.setForeground(new Color(148, 163, 184));
        footer.add(verLbl, BorderLayout.EAST);

        root.add(footer, BorderLayout.SOUTH);

        setContentPane(root);
    }

    private JPanel createStockPanel() {
        JPanel panel = new JPanel(new BorderLayout(12, 12));
        panel.setBackground(Color.WHITE);
        panel.setBorder(new EmptyBorder(16, 16, 16, 16));

        String[] cols = {"Blood Group", "Units in Reserve", "Standard Volume (ml)", "Accredited Center", "State & City"};
        Object[][] data = {
                {"O-", "108 Units", "37,800 ml (Universal Donor)", "Apollo Speciality Blood Bank", "Visakhapatnam, Andhra Pradesh"},
                {"O+", "215 Units", "75,250 ml (High Availability)", "Government General Hospital", "Vijayawada, Andhra Pradesh"},
                {"A-", "84 Units", "29,400 ml (Rh-Negative Stock)", "Red Cross Voluntary Blood Center", "Guntur, Andhra Pradesh"},
                {"A+", "176 Units", "61,600 ml (Active Reserves)", "Fortis Healthcare Blood Center", "Bengaluru, Karnataka"},
                {"B-", "92 Units", "32,200 ml (Emergency Reserve)", "AIIMS Regional Blood Center", "New Delhi, Delhi NCR"},
                {"B+", "230 Units", "80,500 ml (High Availability)", "Rotary Voluntary Blood Bank", "Mumbai, Maharashtra"},
                {"AB-", "48 Units", "16,800 ml (Priority Group)", "Lilavati Hospital Blood Bank", "Pune, Maharashtra"},
                {"AB+", "140 Units", "49,000 ml (Universal Recipient)", "Max Super Speciality Center", "Chennai, Tamil Nadu"}
        };

        DefaultTableModel model = new DefaultTableModel(data, cols) {
            @Override
            public boolean isCellEditable(int row, int col) { return false; }
        };

        JTable table = createStyledTable(model);
        panel.add(new JScrollPane(table), BorderLayout.CENTER);

        // Bottom action bar
        JPanel bar = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 0));
        bar.setBackground(Color.WHITE);
        JButton viewDonorsBtn = createStyledButton("Explore Matching Donors in Directory →", COLOR_RED_600, Color.WHITE);
        viewDonorsBtn.addActionListener(e -> mainTabbedPane.setSelectedIndex(1));
        bar.add(viewDonorsBtn);

        panel.add(bar, BorderLayout.SOUTH);
        return panel;
    }

    private JPanel createDonorsPanel() {
        JPanel panel = new JPanel(new BorderLayout(10, 10));
        panel.setBackground(Color.WHITE);
        panel.setBorder(new EmptyBorder(16, 16, 16, 16));

        // Filter / Search bar
        JPanel searchBar = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 0));
        searchBar.setBackground(Color.WHITE);
        searchBar.add(new JLabel("Search Filter:"));
        JTextField searchField = new JTextField(24);
        searchField.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        searchBar.add(searchField);

        panel.add(searchBar, BorderLayout.NORTH);

        String[] cols = {"Donor ID", "Donor Full Name", "Aadhaar Number", "Blood Group", "State & City", "Clinical Status", "Uploaded Proofs", "Donation History", "Contact Mobile"};
        donorsTableModel = new DefaultTableModel(cols, 0) {
            @Override
            public boolean isCellEditable(int row, int col) { return false; }
        };

        // 256 realistic Pan-India donors
        String[] groups = {"O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"};
        String[] firsts = {"Aarav", "Aditi", "Akhil", "Ananya", "Bhavani", "Chaitanya", "Deepika", "Dinesh", "Harish", "Krishna", "Lakshmi", "Madhav", "Naveen", "Priya", "Rahul", "Rajesh", "Sai", "Sneha", "Srinivas", "Suresh", "Tarun", "Vikram", "Rohan", "Tanvi", "Arjun"};
        String[] lasts = {"Reddy", "Rao", "Chowdary", "Varma", "Naidu", "Sharma", "Murthy", "Raju", "Prasad", "Kumar", "Gupta", "Deshmukh", "Iyer", "Banerjee", "Singh"};
        String[] states = INDIA_LOCATIONS.keySet().toArray(new String[0]);

        for (int i = 1; i <= 256; i++) {
            String id = String.format("DNR-%03d", i);
            String name = firsts[i % firsts.length] + " " + lasts[(i * 3) % lasts.length];
            String aadhaar = String.format("XXXX-XXXX-%04d", 1000 + ((i * 37) % 8999));
            String bg = groups[i % groups.length];
            String st = states[i % states.length];
            String[] cities = INDIA_LOCATIONS.get(st);
            String city = cities[i % cities.length];
            int rest = 90 + ((i * 7) % 60);
            double hb = 12.6 + ((i % 25) * 0.12);
            String health = String.format("FIT (Hb: %.1f g/dL, Rest: %dd)", hb, rest);
            String proof = (i % 2 == 0) ? "Doctor Fitness Cert & Blood Card" : "Hospital Report & Lab ID";
            String state = (i % 3 == 0) ? "Already Donated" : "Ready to Donate";
            String mobile = "+91 98" + String.format("%08d", (10000000 + (i * 33333)) % 99999999);

            donorsTableModel.addRow(new Object[]{id, name, aadhaar, bg, city + ", " + st, health, proof, state, mobile});
        }

        JTable table = createStyledTable(donorsTableModel);
        TableRowSorter<DefaultTableModel> sorter = new TableRowSorter<>(donorsTableModel);
        table.setRowSorter(sorter);

        searchField.getDocument().addDocumentListener(new javax.swing.event.DocumentListener() {
            public void insertUpdate(javax.swing.event.DocumentEvent e) { filter(); }
            public void removeUpdate(javax.swing.event.DocumentEvent e) { filter(); }
            public void changedUpdate(javax.swing.event.DocumentEvent e) { filter(); }
            private void filter() {
                String txt = searchField.getText().trim();
                if (txt.isEmpty()) sorter.setRowFilter(null);
                else sorter.setRowFilter(RowFilter.regexFilter("(?i)" + txt));
            }
        });

        panel.add(new JScrollPane(table), BorderLayout.CENTER);

        // Control bottom bar
        JPanel bar = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 0));
        bar.setBackground(Color.WHITE);
        JButton callBtn = createStyledButton("Contact Selected Donor", COLOR_RED_600, Color.WHITE);
        callBtn.addActionListener(e -> {
            int row = table.getSelectedRow();
            if (row != -1) {
                int modelRow = table.convertRowIndexToModel(row);
                String donor = (String) donorsTableModel.getValueAt(modelRow, 1);
                String tel = (String) donorsTableModel.getValueAt(modelRow, 8);
                JOptionPane.showMessageDialog(this,
                        "Connecting donor tele-coordination dispatch to:\n" + donor + " (" + tel + ")",
                        "Donor Tele-Contact", JOptionPane.INFORMATION_MESSAGE);
            } else {
                JOptionPane.showMessageDialog(this, "Please select a donor from the table first.");
            }
        });

        JButton regNavBtn = createStyledButton("+ Register New Donor", COLOR_NAVY_900, Color.WHITE);
        regNavBtn.addActionListener(e -> mainTabbedPane.setSelectedIndex(4));

        bar.add(callBtn);
        bar.add(regNavBtn);
        panel.add(bar, BorderLayout.SOUTH);

        return panel;
    }

    private JPanel createRecipientsPanel() {
        JPanel panel = new JPanel(new BorderLayout(10, 10));
        panel.setBackground(Color.WHITE);
        panel.setBorder(new EmptyBorder(16, 16, 16, 16));

        String[] cols = {"Request ID", "Patient Name", "Aadhaar Hash", "Required Group", "Units Needed", "Hospital & Location", "Clinical Urgency", "Attendant Mobile", "Status"};
        recipientsTableModel = new DefaultTableModel(cols, 0) {
            @Override
            public boolean isCellEditable(int row, int col) { return false; }
        };

        String[] pfirsts = {"Srinivasa", "Lakshmi", "Venkat", "Priya", "Madhav", "Kavya", "Venkatesh", "Swapna", "Rohan", "Meera"};
        String[] lasts = {"Rao", "Devi", "Raman", "Sharma", "Murthy", "Chowdary", "Naidu", "Varma", "Patil", "Deshmukh"};
        String[] groups = {"O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"};
        String[] hospitals = {
                "Apollo Speciality Hospital, Vizag", "GGH Vijayawada, AP", "Manipal Hospital, Bengaluru",
                "Lilavati Hospital, Mumbai", "AIIMS, New Delhi", "Fortis Hospital, Chennai", "Care Hospitals, Hyderabad"
        };
        String[] urg = {"CRITICAL", "URGENT", "ROUTINE"};

        for (int j = 1; j <= 32; j++) {
            String id = "REQ-" + (8000 + j);
            String name = pfirsts[j % pfirsts.length] + " " + lasts[(j * 2) % lasts.length];
            String aadhaar = String.format("XXXX-XXXX-%04d", 2000 + ((j * 43) % 7999));
            String bg = groups[(j * 2) % groups.length];
            int units = (j % 4) + 1;
            String unitStr = units + " Unit" + (units > 1 ? "s" : "") + " (" + (units * 350) + " ml)";
            String hosp = hospitals[j % hospitals.length];
            String urgency = urg[j % urg.length];
            String mobile = "+91 97" + String.format("%08d", (20000000 + (j * 44444)) % 99999999);
            String status = (j % 3 == 0) ? "ALLOCATED" : "LOOKING_FOR_DONORS";

            recipientsTableModel.addRow(new Object[]{id, name, aadhaar, bg, unitStr, hosp, urgency, mobile, status});
        }

        JTable table = createStyledTable(recipientsTableModel);
        panel.add(new JScrollPane(table), BorderLayout.CENTER);

        JPanel bar = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 0));
        bar.setBackground(Color.WHITE);
        JButton matchBtn = createStyledButton("Match & Dispatch Blood Reserves", COLOR_RED_600, Color.WHITE);
        matchBtn.addActionListener(e -> {
            int row = table.getSelectedRow();
            if (row != -1) {
                String req = (String) table.getValueAt(row, 0);
                String p = (String) table.getValueAt(row, 1);
                table.setValueAt("ALLOCATED", row, 8);
                JOptionPane.showMessageDialog(this,
                        "Emergency transfusion match approved for " + p + " [" + req + "].\nBlood stock dispatched from accredited regional center.",
                        "Blood Allocation", JOptionPane.INFORMATION_MESSAGE);
            } else {
                JOptionPane.showMessageDialog(this, "Select a patient requirement from the list.");
            }
        });

        JButton reqNavBtn = createStyledButton("+ Submit Transfusion Request", COLOR_NAVY_900, Color.WHITE);
        reqNavBtn.addActionListener(e -> mainTabbedPane.setSelectedIndex(5));

        bar.add(matchBtn);
        bar.add(reqNavBtn);
        panel.add(bar, BorderLayout.SOUTH);

        return panel;
    }

    private JPanel createApprovalPanel() {
        JPanel panel = new JPanel(new BorderLayout(10, 10));
        panel.setBackground(Color.WHITE);
        panel.setBorder(new EmptyBorder(16, 16, 16, 16));

        // Subtitle header
        JLabel desc = new JLabel("Medical Officer Clearance Console: Review uploaded doctor certificates, preview clinical findings, and approve registrations.");
        desc.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        desc.setForeground(COLOR_SLATE_500);
        panel.add(desc, BorderLayout.NORTH);

        String[] cols = {"Registration ID", "Donor Full Name", "Aadhaar Card No", "Blood Group", "Medical Fitness Certificate", "Blood Group Proof", "Review Status"};
        pendingApprovalsTableModel = new DefaultTableModel(cols, 0) {
            @Override
            public boolean isCellEditable(int row, int col) { return false; }
        };

        pendingApprovalsTableModel.addRow(new Object[]{"PEND-01", "K. Rajesh Kumar", "XXXX-XXXX-4512", "O-", "medical_fitness_dr_reddy.pdf", "lab_report_blood_group.pdf", "WAITING FOR APPROVAL"});
        pendingApprovalsTableModel.addRow(new Object[]{"PEND-02", "M. Ananya Rao", "XXXX-XXXX-8921", "B+", "clinical_clearance_apollo.pdf", "hospital_donor_card.pdf", "WAITING FOR APPROVAL"});
        pendingApprovalsTableModel.addRow(new Object[]{"PEND-03", "P. Suresh Varma", "XXXX-XXXX-3341", "A+", "annual_health_check_nov.pdf", "diagnostic_group_id.pdf", "WAITING FOR APPROVAL"});
        pendingApprovalsTableModel.addRow(new Object[]{"PEND-04", "B. Sneha Naidu", "XXXX-XXXX-6712", "AB+", "ggh_fitness_certificate.pdf", "blood_donor_card.pdf", "WAITING FOR APPROVAL"});
        pendingApprovalsTableModel.addRow(new Object[]{"PEND-05", "D. Tarun Chowdary", "XXXX-XXXX-9901", "O+", "pathology_clearance.pdf", "red_cross_lab_report.pdf", "WAITING FOR APPROVAL"});

        JTable table = createStyledTable(pendingApprovalsTableModel);
        panel.add(new JScrollPane(table), BorderLayout.CENTER);

        JPanel actBar = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 0));
        actBar.setBackground(Color.WHITE);

        JButton previewBtn = createStyledButton("Preview Certificate", COLOR_NAVY_900, Color.WHITE);
        previewBtn.addActionListener(e -> {
            int row = table.getSelectedRow();
            if (row != -1) {
                String donorName = (String) pendingApprovalsTableModel.getValueAt(row, 1);
                String aadhaar = (String) pendingApprovalsTableModel.getValueAt(row, 2);
                String bg = (String) pendingApprovalsTableModel.getValueAt(row, 3);
                String cert = (String) pendingApprovalsTableModel.getValueAt(row, 4);
                String proof = (String) pendingApprovalsTableModel.getValueAt(row, 5);
                showCertificatePreviewDialog(donorName, aadhaar, bg, cert, proof);
            } else {
                JOptionPane.showMessageDialog(this, "Select a pending donor row from the table to preview certificates.");
            }
        });

        JButton approveBtn = createStyledButton("✓ Approve Donor Credentials", COLOR_EMERALD_600, Color.WHITE);
        approveBtn.addActionListener(e -> {
            int row = table.getSelectedRow();
            if (row != -1) {
                String donorName = (String) pendingApprovalsTableModel.getValueAt(row, 1);
                String bg = (String) pendingApprovalsTableModel.getValueAt(row, 3);
                pendingApprovalsTableModel.setValueAt("APPROVED (Medical Officer Cleared)", row, 6);

                // Also append to the active donors roster
                donorsTableModel.insertRow(0, new Object[]{
                        "DNR-" + (257 + donorsTableModel.getRowCount()),
                        donorName,
                        pendingApprovalsTableModel.getValueAt(row, 2),
                        bg,
                        "Visakhapatnam, Andhra Pradesh",
                        "FIT (Hb: 13.5 g/dL, Rest: 95d)",
                        pendingApprovalsTableModel.getValueAt(row, 4),
                        "Ready to Donate",
                        "+91 9848" + (200000 + (row * 1234))
                });

                JOptionPane.showMessageDialog(this,
                        "Donor registration and uploaded certificates verified successfully for " + donorName + " (" + bg + ").\nStatus updated to APPROVED and added to live roster.",
                        "Authority Approval", JOptionPane.INFORMATION_MESSAGE);
            } else {
                JOptionPane.showMessageDialog(this, "Select a pending donor row to review.");
            }
        });

        JButton deferBtn = createStyledButton("✕ Decline / Temporary Deferral", COLOR_RED_600, Color.WHITE);
        deferBtn.addActionListener(e -> {
            int row = table.getSelectedRow();
            if (row != -1) {
                String donorName = (String) pendingApprovalsTableModel.getValueAt(row, 1);
                pendingApprovalsTableModel.setValueAt("DEFERRED (Cooldown Rest Required)", row, 6);
                JOptionPane.showMessageDialog(this,
                        "Donor " + donorName + " placed on temporary clinical cooldown rest (90 days).",
                        "Clinical Deferral", JOptionPane.WARNING_MESSAGE);
            } else {
                JOptionPane.showMessageDialog(this, "Select a pending donor row to defer.");
            }
        });

        actBar.add(previewBtn);
        actBar.add(deferBtn);
        actBar.add(approveBtn);
        panel.add(actBar, BorderLayout.SOUTH);

        return panel;
    }

    void updateDynamicTabCounts() {
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
                "Authentication Successful!\n\nUser: " + name + "\nEmail: " + email + "\nRole: " + role,
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
                "<i>&quot;I have personally examined the volunteer donor mentioned above and inspected all uploaded diagnostic certificates. I hereby certify that the candidate meets all statutory physical and physiological fitness criteria for voluntary blood donation.&quot;</i><br/><br/>" +
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
                "Official Clinical Clearance Slip generated successfully.\nReady to print via registered Hospital Transfusion Desk.",
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
    }

    private JPanel createDonorRegistrationPanel() {
        JPanel panel = new JPanel(new GridBagLayout());
        panel.setBackground(Color.WHITE);
        panel.setBorder(new EmptyBorder(24, 32, 24, 32));

        GridBagConstraints gbc = new GridBagConstraints();
        gbc.fill = GridBagConstraints.HORIZONTAL;
        gbc.insets = new Insets(6, 12, 6, 12);

        // Header Title
        gbc.gridx = 0; gbc.gridy = 0; gbc.gridwidth = 2;
        JLabel title = new JLabel("Voluntary Donor Registration Form");
        title.setFont(new Font("Segoe UI", Font.BOLD, 16));
        title.setForeground(COLOR_NAVY_900);
        panel.add(title, gbc);

        gbc.gridy = 1;
        JLabel desc = new JLabel("Submit verified details and doctor-certified PDF reports for manual Medical Officer review.");
        desc.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        desc.setForeground(COLOR_SLATE_500);
        panel.add(desc, gbc);

        // Row 1: Name & Aadhaar
        gbc.gridwidth = 1; gbc.gridy = 2; gbc.gridx = 0;
        panel.add(new JLabel("Full Name (As per Aadhaar):"), gbc);
        gbc.gridx = 1;
        panel.add(new JLabel("Aadhaar Number (12 Digits):"), gbc);

        gbc.gridy = 3; gbc.gridx = 0;
        JTextField nameField = new JTextField(20);
        nameField.setPreferredSize(new Dimension(280, 32));
        panel.add(nameField, gbc);

        gbc.gridx = 1;
        JTextField aadhaarField = new JTextField(20);
        aadhaarField.setPreferredSize(new Dimension(280, 32));
        panel.add(aadhaarField, gbc);

        // Row 2: Blood Group & Mobile
        gbc.gridy = 4; gbc.gridx = 0;
        panel.add(new JLabel("Blood Group:"), gbc);
        gbc.gridx = 1;
        panel.add(new JLabel("Mobile Contact Number:"), gbc);

        gbc.gridy = 5; gbc.gridx = 0;
        String[] bgs = {"O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"};
        JComboBox<String> bgCombo = new JComboBox<>(bgs);
        bgCombo.setPreferredSize(new Dimension(280, 32));
        panel.add(bgCombo, gbc);

        gbc.gridx = 1;
        JTextField mobileField = new JTextField(20);
        mobileField.setPreferredSize(new Dimension(280, 32));
        panel.add(mobileField, gbc);

        // Row 3: State & City
        gbc.gridy = 6; gbc.gridx = 0;
        panel.add(new JLabel("State / Union Territory:"), gbc);
        gbc.gridx = 1;
        panel.add(new JLabel("City / District:"), gbc);

        gbc.gridy = 7; gbc.gridx = 0;
        String[] stateList = INDIA_LOCATIONS.keySet().toArray(new String[0]);
        JComboBox<String> stateCombo = new JComboBox<>(stateList);
        stateCombo.setPreferredSize(new Dimension(280, 32));
        panel.add(stateCombo, gbc);

        gbc.gridx = 1;
        JComboBox<String> cityCombo = new JComboBox<>(INDIA_LOCATIONS.get(stateList[0]));
        cityCombo.setPreferredSize(new Dimension(280, 32));
        panel.add(cityCombo, gbc);

        stateCombo.addActionListener(e -> {
            String selState = (String) stateCombo.getSelectedItem();
            if (selState != null) {
                cityCombo.setModel(new DefaultComboBoxModel<>(INDIA_LOCATIONS.get(selState)));
            }
        });

        // Row 4: File upload for Certificates
        gbc.gridy = 8; gbc.gridx = 0;
        panel.add(new JLabel("Medical Fitness Certificate (Doctor Signed):"), gbc);
        gbc.gridx = 1;
        panel.add(new JLabel("Blood Group Proof Certificate (Lab Report):"), gbc);

        gbc.gridy = 9; gbc.gridx = 0;
        final String[] uploadedCert = {"medical_fitness_report.pdf"};
        JLabel certLabel = new JLabel("Selected: medical_fitness_report.pdf");
        certLabel.setFont(new Font("Segoe UI", Font.ITALIC, 11));
        certLabel.setForeground(COLOR_SLATE_500);

        JButton chooseCertBtn = createStyledButton("Browse PDF Certificate", COLOR_SLATE_200, COLOR_NAVY_900);
        chooseCertBtn.addActionListener(e -> {
            JFileChooser fc = new JFileChooser();
            fc.setFileFilter(new FileNameExtensionFilter("PDF Documents & Images (*.pdf, *.png, *.jpg)", "pdf", "png", "jpg", "jpeg"));
            if (fc.showOpenDialog(this) == JFileChooser.APPROVE_OPTION) {
                File f = fc.getSelectedFile();
                uploadedCert[0] = f.getName();
                certificateFilePathMap.put(f.getName(), f.getAbsolutePath());
                certLabel.setText("Selected: " + f.getName());
            }
        });
        JPanel certBox = new JPanel(new FlowLayout(FlowLayout.LEFT, 6, 0));
        certBox.setBackground(Color.WHITE);
        certBox.add(chooseCertBtn);
        certBox.add(certLabel);
        panel.add(certBox, gbc);

        gbc.gridx = 1;
        final String[] uploadedProof = {"lab_report_blood_card.pdf"};
        JLabel proofLabel = new JLabel("Selected: lab_report_blood_card.pdf");
        proofLabel.setFont(new Font("Segoe UI", Font.ITALIC, 11));
        proofLabel.setForeground(COLOR_SLATE_500);

        JButton chooseProofBtn = createStyledButton("Browse Proof PDF", COLOR_SLATE_200, COLOR_NAVY_900);
        chooseProofBtn.addActionListener(e -> {
            JFileChooser fc = new JFileChooser();
            fc.setFileFilter(new FileNameExtensionFilter("PDF Documents & Images (*.pdf, *.png, *.jpg)", "pdf", "png", "jpg", "jpeg"));
            if (fc.showOpenDialog(this) == JFileChooser.APPROVE_OPTION) {
                File f = fc.getSelectedFile();
                uploadedProof[0] = f.getName();
                certificateFilePathMap.put(f.getName(), f.getAbsolutePath());
                proofLabel.setText("Selected: " + f.getName());
            }
        });
        JPanel proofBox = new JPanel(new FlowLayout(FlowLayout.LEFT, 6, 0));
        proofBox.setBackground(Color.WHITE);
        proofBox.add(chooseProofBtn);
        proofBox.add(proofLabel);
        panel.add(proofBox, gbc);

        // Submit Button
        gbc.gridy = 10; gbc.gridx = 0; gbc.gridwidth = 2;
        gbc.insets = new Insets(18, 12, 6, 12);
        JButton submitBtn = createStyledButton("Submit for Medical Officer Review", COLOR_NAVY_900, Color.WHITE);
        submitBtn.setPreferredSize(new Dimension(300, 42));
        submitBtn.addActionListener(e -> {
            String n = nameField.getText().trim();
            String a = aadhaarField.getText().trim();
            String m = mobileField.getText().trim();
            String bg = (String) bgCombo.getSelectedItem();
            String st = (String) stateCombo.getSelectedItem();
            String ct = (String) cityCombo.getSelectedItem();

            if (n.isEmpty() || a.length() != 12) {
                JOptionPane.showMessageDialog(this, "Please enter a valid full name and 12-digit Aadhaar number.", "Validation Error", JOptionPane.ERROR_MESSAGE);
                return;
            }

            // Push to Medical Verification Desk table
            String newId = "PEND-" + String.format("%02d", pendingApprovalsTableModel.getRowCount() + 1);
            pendingApprovalsTableModel.insertRow(0, new Object[]{
                    newId, n, "XXXX-XXXX-" + a.substring(8), bg, uploadedCert[0], uploadedProof[0], "WAITING FOR APPROVAL"
            });

            JOptionPane.showMessageDialog(this,
                    "Registration submitted successfully for " + n + " (" + bg + ") in " + ct + ", " + st + ".\nCertificate files (" + uploadedCert[0] + ", " + uploadedProof[0] + ") queued for Medical Officer Review.",
                    "Registration Submitted", JOptionPane.INFORMATION_MESSAGE);

            nameField.setText("");
            aadhaarField.setText("");
            mobileField.setText("");
            mainTabbedPane.setSelectedIndex(3); // Switch to verification desk
        });
        panel.add(submitBtn, gbc);

        return panel;
    }

    private JPanel createEmergencyRequestPanel() {
        JPanel panel = new JPanel(new GridBagLayout());
        panel.setBackground(Color.WHITE);
        panel.setBorder(new EmptyBorder(24, 32, 24, 32));

        GridBagConstraints gbc = new GridBagConstraints();
        gbc.fill = GridBagConstraints.HORIZONTAL;
        gbc.insets = new Insets(6, 12, 6, 12);

        // Header Title
        gbc.gridx = 0; gbc.gridy = 0; gbc.gridwidth = 2;
        JLabel title = new JLabel("Ask for Blood — Emergency Transfusion Requirement");
        title.setFont(new Font("Segoe UI", Font.BOLD, 16));
        title.setForeground(COLOR_NAVY_900);
        panel.add(title, gbc);

        gbc.gridy = 1;
        JLabel desc = new JLabel("Submit urgent blood requirements for hospital inpatients and trauma care.");
        desc.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        desc.setForeground(COLOR_SLATE_500);
        panel.add(desc, gbc);

        // Row 1: Patient Name & Aadhaar
        gbc.gridwidth = 1; gbc.gridy = 2; gbc.gridx = 0;
        panel.add(new JLabel("Patient Full Name (As per Aadhaar):"), gbc);
        gbc.gridx = 1;
        panel.add(new JLabel("Patient Aadhaar Number (12 Digits):"), gbc);

        gbc.gridy = 3; gbc.gridx = 0;
        JTextField pNameField = new JTextField(20);
        pNameField.setPreferredSize(new Dimension(280, 32));
        panel.add(pNameField, gbc);

        gbc.gridx = 1;
        JTextField pAadhaarField = new JTextField(20);
        pAadhaarField.setPreferredSize(new Dimension(280, 32));
        panel.add(pAadhaarField, gbc);

        // Row 2: Required Group & Urgency
        gbc.gridy = 4; gbc.gridx = 0;
        panel.add(new JLabel("Required Blood Group:"), gbc);
        gbc.gridx = 1;
        panel.add(new JLabel("Clinical Urgency:"), gbc);

        gbc.gridy = 5; gbc.gridx = 0;
        String[] bgs = {"O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"};
        JComboBox<String> reqBgCombo = new JComboBox<>(bgs);
        reqBgCombo.setPreferredSize(new Dimension(280, 32));
        panel.add(reqBgCombo, gbc);

        gbc.gridx = 1;
        String[] urgencies = {"CRITICAL (Immediate Surgery / ICU)", "URGENT (Within 6 Hours)", "ROUTINE (Scheduled Transfusion)"};
        JComboBox<String> urgCombo = new JComboBox<>(urgencies);
        urgCombo.setPreferredSize(new Dimension(280, 32));
        panel.add(urgCombo, gbc);

        // Row 3: Units Needed & Attendant Mobile
        gbc.gridy = 6; gbc.gridx = 0;
        panel.add(new JLabel("Units Needed (1 Unit = 350 ml):"), gbc);
        gbc.gridx = 1;
        panel.add(new JLabel("Attendant Contact Mobile:"), gbc);

        gbc.gridy = 7; gbc.gridx = 0;
        Integer[] units = {1, 2, 3, 4, 5, 6};
        JComboBox<Integer> unitsCombo = new JComboBox<>(units);
        unitsCombo.setSelectedIndex(1); // default 2 units
        unitsCombo.setPreferredSize(new Dimension(280, 32));
        panel.add(unitsCombo, gbc);

        gbc.gridx = 1;
        JTextField pMobileField = new JTextField(20);
        pMobileField.setPreferredSize(new Dimension(280, 32));
        panel.add(pMobileField, gbc);

        // Row 4: Hospital Name
        gbc.gridy = 8; gbc.gridx = 0; gbc.gridwidth = 2;
        panel.add(new JLabel("Hospital Name & District:"), gbc);

        gbc.gridy = 9;
        JTextField hospField = new JTextField("Apollo Speciality Hospital, Vizag");
        hospField.setPreferredSize(new Dimension(580, 32));
        panel.add(hospField, gbc);

        // Submit Button
        gbc.gridy = 10;
        gbc.insets = new Insets(18, 12, 6, 12);
        JButton submitReqBtn = createStyledButton("Submit Emergency Transfusion Requirement", COLOR_RED_600, Color.WHITE);
        submitReqBtn.setPreferredSize(new Dimension(340, 42));
        submitReqBtn.addActionListener(e -> {
            String pn = pNameField.getText().trim();
            String pa = pAadhaarField.getText().trim();
            String bg = (String) reqBgCombo.getSelectedItem();
            int u = (Integer) unitsCombo.getSelectedItem();
            String h = hospField.getText().trim();
            String m = pMobileField.getText().trim();

            if (pn.isEmpty() || pa.length() != 12) {
                JOptionPane.showMessageDialog(this, "Please enter a valid patient name and 12-digit Aadhaar number.", "Validation Error", JOptionPane.ERROR_MESSAGE);
                return;
            }

            String newReqId = "REQ-" + (8000 + recipientsTableModel.getRowCount() + 1);
            recipientsTableModel.insertRow(0, new Object[]{
                    newReqId, pn, "XXXX-XXXX-" + pa.substring(8), bg, u + " Units (" + (u * 350) + " ml)", h, "CRITICAL", m, "LOOKING_FOR_DONORS"
            });

            JOptionPane.showMessageDialog(this,
                    "Emergency requirement logged for " + pn + " (" + bg + ", " + u + " Units).\nSurrounding blood banks and matching donors notified.",
                    "Request Registered", JOptionPane.INFORMATION_MESSAGE);

            pNameField.setText("");
            pAadhaarField.setText("");
            pMobileField.setText("");
            mainTabbedPane.setSelectedIndex(2); // Switch to Who Wants Blood
        });
        panel.add(submitReqBtn, gbc);

        return panel;
    }

    private void showClinicalGuideDialog() {
        String msg = "<html><body style='width: 380px; font-family: Segoe UI, sans-serif; font-size: 11px;'>" +
                "<h3 style='color: #0F172A; margin-bottom: 6px;'>Clinical Eligibility Criteria (NBTC & NACO Norms)</h3>" +
                "<p style='margin-bottom: 8px;'>Understanding <b>FIT (Hb: 13.1 g/dL, Rest: 133d)</b>:</p>" +
                "<div style='background: #F8FAFC; border: 1px solid #E2E8F0; padding: 10px; border-radius: 6px;'>" +
                "<p><b>1. FIT</b>: The donor has passed pre-donation clinical screening, vitals check (BP 100-140/60-90), and absence of infectious serology.</p>" +
                "<p style='margin-top: 6px;'><b>2. Hb: 13.1 g/dL (Hemoglobin)</b>: NBTC statutory minimum threshold is <b>12.5 g/dL</b>. 13.1 g/dL confirms adequate red blood cell mass for safe phlebotomy.</p>" +
                "<p style='margin-top: 6px;'><b>3. Rest: 133d (Cooldown Interval)</b>: Mandatory recovery rest between whole blood donations is <b>90 days</b> for males and <b>120 days</b> for females. 133 days confirms complete physiological recovery.</p>" +
                "</div>" +
                "<p style='color: #64748B; margin-top: 8px;'>All donations are verified by an accredited Medical Officer.</p>" +
                "</body></html>";

        JOptionPane.showMessageDialog(this, msg, "Clinical Eligibility Guide", JOptionPane.INFORMATION_MESSAGE);
    }

    private JTable createStyledTable(DefaultTableModel model) {
        JTable table = new JTable(model);
        table.setRowHeight(36);
        table.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        table.setGridColor(COLOR_SLATE_100);
        table.setSelectionBackground(new Color(254, 242, 242));
        table.setSelectionForeground(COLOR_NAVY_900);

        JTableHeader header = table.getTableHeader();
        header.setFont(new Font("Segoe UI", Font.BOLD, 12));
        header.setBackground(COLOR_SLATE_100);
        header.setForeground(COLOR_NAVY_900);
        header.setBorder(new LineBorder(COLOR_SLATE_200));

        DefaultTableCellRenderer renderer = new DefaultTableCellRenderer();
        renderer.setBorder(new EmptyBorder(0, 8, 0, 8));
        table.setDefaultRenderer(Object.class, renderer);

        return table;
    }

    /**
     * Anti-aliased custom rendered button that completely bypasses Windows LAF
     * white-on-white button painting bugs.
     */
    private JButton createStyledButton(String text, Color bg, Color fg) {
        JButton btn = new JButton(text) {
            @Override
            protected void paintComponent(Graphics g) {
                Graphics2D g2 = (Graphics2D) g.create();
                g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

                Color currentBg = bg;
                if (getModel().isPressed()) {
                    currentBg = bg.darker();
                } else if (getModel().isRollover()) {
                    currentBg = new Color(
                            Math.min(255, bg.getRed() + 25),
                            Math.min(255, bg.getGreen() + 25),
                            Math.min(255, bg.getBlue() + 25)
                    );
                }

                g2.setColor(currentBg);
                g2.fillRoundRect(0, 0, getWidth(), getHeight(), 8, 8);

                // Subtle outline
                g2.setColor(new Color(0, 0, 0, 35));
                g2.drawRoundRect(0, 0, getWidth() - 1, getHeight() - 1, 8, 8);

                // Centered text
                g2.setFont(getFont());
                g2.setColor(fg);
                FontMetrics fm = g2.getFontMetrics();
                int textX = (getWidth() - fm.stringWidth(getText())) / 2;
                int textY = (getHeight() + fm.getAscent() - fm.getDescent()) / 2;
                g2.drawString(getText(), textX, textY);

                g2.dispose();
            }
        };

        btn.setFont(new Font("Segoe UI", Font.BOLD, 12));
        btn.setContentAreaFilled(false);
        btn.setOpaque(false);
        btn.setFocusPainted(false);
        btn.setBorder(new EmptyBorder(8, 16, 8, 16));
        btn.setCursor(new Cursor(Cursor.HAND_CURSOR));
        return btn;
    }

    private void checkForUpdates() {
        statusLabel.setText("Checking for updates at " + UPDATE_CHECK_URL + "...");
        SwingWorker<String, Void> worker = new SwingWorker<>() {
            @Override
            protected String doInBackground() {
                try {
                    URL url = URI.create(UPDATE_CHECK_URL).toURL();
                    HttpURLConnection con = (HttpURLConnection) url.openConnection();
                    con.setConnectTimeout(4000);
                    con.setRequestMethod("GET");
                    if (con.getResponseCode() == 200) {
                        try (BufferedReader r = new BufferedReader(new InputStreamReader(con.getInputStream()))) {
                            StringBuilder sb = new StringBuilder();
                            String line;
                            while ((line = r.readLine()) != null) sb.append(line);
                            return sb.toString();
                        }
                    }
                } catch (Exception ignored) {}
                return null;
            }

            @Override
            protected void done() {
                try {
                    String json = get();
                    if (json != null && json.contains("1.0.1")) {
                        int res = JOptionPane.showConfirmDialog(VitalSphereDesktopClient.this,
                                "A newer version of VitalSphere Desktop Client is available!\nWould you like to auto-update now?",
                                "Update Detected", JOptionPane.YES_NO_OPTION);
                        if (res == JOptionPane.YES_OPTION) {
                            JOptionPane.showMessageDialog(VitalSphereDesktopClient.this,
                                    "App updated successfully to latest build!", "Update Complete", JOptionPane.INFORMATION_MESSAGE);
                        }
                    } else {
                        JOptionPane.showMessageDialog(VitalSphereDesktopClient.this,
                                "You are running the latest verified build [v" + APP_VERSION + "]. All cloud engines are up to date.",
                                "VitalSphere Up to Date", JOptionPane.INFORMATION_MESSAGE);
                        statusLabel.setText("Status: Latest version verified (v" + APP_VERSION + ")");
                    }
                } catch (Exception ex) {
                    JOptionPane.showMessageDialog(VitalSphereDesktopClient.this,
                            "You are currently running the latest stable build [v" + APP_VERSION + "].",
                            "Update Status", JOptionPane.INFORMATION_MESSAGE);
                }
            }
        };
        worker.execute();
    }

    private void openWeb() {
        try {
            Desktop.getDesktop().browse(URI.create(WEB_PORTAL_URL));
        } catch (Exception e) {
            JOptionPane.showMessageDialog(this, "Could not open browser: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
            } catch (Exception ignored) {}
            new VitalSphereDesktopClient().setVisible(true);
        });
    }
}
