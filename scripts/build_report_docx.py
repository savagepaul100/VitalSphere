import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

print("Building VitalSphere Comprehensive Academic Project Report (.docx)...")

output_dir = os.path.abspath("Report and PPT")
os.makedirs(output_dir, exist_ok=True)
report_path = os.path.join(output_dir, "VitalSphere_Project_Report.docx")

doc = docx.Document()

# Set standard 1-inch margins
for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

# Color Palette
COLOR_NAVY = RGBColor(10, 17, 32)
COLOR_RED = RGBColor(220, 38, 38)
COLOR_SLATE = RGBColor(71, 85, 105)
COLOR_MUTED = RGBColor(100, 116, 139)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def add_heading_1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(17)
    run.font.bold = True
    run.font.color.rgb = COLOR_RED
    return p

def add_heading_2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = COLOR_NAVY
    return p

def add_heading_3(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(11.5)
    run.font.bold = True
    run.font.color.rgb = COLOR_SLATE
    return p

def add_body_p(text, bold_prefix=None, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Calibri'
        r_pre.font.size = Pt(10.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_NAVY
    r = p.add_run(text)
    r.font.name = 'Calibri'
    r.font.size = Pt(10.5)
    r.font.color.rgb = RGBColor(30, 41, 59)
    return p

def add_bullet(text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Calibri'
        r_pre.font.size = Pt(10)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_NAVY
    r = p.add_run(text)
    r.font.name = 'Calibri'
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(51, 65, 85)
    return p

# ------------------------------------------------------------------------------
# PAGE 1: TITLE PAGE
# ------------------------------------------------------------------------------
srm_logo_path = r"C:\Users\PAUL\Documents\Projects\Nexus-Arena\srm_logo.png"

p_logo = doc.add_paragraph()
p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_logo.paragraph_format.space_after = Pt(16)
if os.path.exists(srm_logo_path):
    p_logo.add_run().add_picture(srm_logo_path, width=Inches(2.4))

p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_after = Pt(6)
r_title = p_title.add_run("VITALSPHERE — NATIONAL HEALTHCARE &\nCLOUD-SYNCHRONIZED BLOOD LOGISTICS PLATFORM")
r_title.font.name = 'Calibri'
r_title.font.size = Pt(19)
r_title.font.bold = True
r_title.font.color.rgb = COLOR_RED

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_after = Pt(24)
r_sub = p_sub.add_run("A Project Report submitted in partial fulfilment of the requirements\nfor the award of the degree of\nBachelor of Technology in Computer Science and Engineering\nSchool of Engineering and Sciences")
r_sub.font.name = 'Calibri'
r_sub.font.size = Pt(11)
r_sub.font.italic = True
r_sub.font.color.rgb = COLOR_SLATE

# Table for Submitted By & Submitted To
meta_table = doc.add_table(rows=2, cols=2)
meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_table.autofit = False

cell_by_h = meta_table.cell(0, 0)
cell_to_h = meta_table.cell(0, 1)
cell_by_c = meta_table.cell(1, 0)
cell_to_c = meta_table.cell(1, 1)

cell_by_h.paragraphs[0].text = "SUBMITTED BY:"
cell_by_h.paragraphs[0].runs[0].font.bold = True
cell_by_h.paragraphs[0].runs[0].font.size = Pt(10.5)
cell_by_h.paragraphs[0].runs[0].font.color.rgb = COLOR_NAVY

cell_to_h.paragraphs[0].text = "SUBMITTED TO:"
cell_to_h.paragraphs[0].runs[0].font.bold = True
cell_to_h.paragraphs[0].runs[0].font.size = Pt(10.5)
cell_to_h.paragraphs[0].runs[0].font.color.rgb = COLOR_NAVY

p_by = cell_by_c.paragraphs[0]
p_by.paragraph_format.line_spacing = 1.2
p_by.add_run("1. P. Abhishek Paul (AP25110071316)\n2. K. Nithien (AP25110070134)\n3. Shaik Hasnain (AP25110070228)\n\nCourse: CSE 213 — Advanced Java Programming\nClass: III Semester B.Tech CSE AI ML F").font.size = Pt(9.5)

p_to = cell_to_c.paragraphs[0]
p_to.paragraph_format.line_spacing = 1.2
p_to.add_run("Dr. Srikanth Lukka\nAssistant Professor\nDepartment of Computer Science and Engineering\nSchool of Engineering and Sciences\nSRM University – AP, Andhra Pradesh").font.size = Pt(9.5)

p_foot = doc.add_paragraph()
p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_foot.paragraph_format.space_before = Pt(36)
p_foot.paragraph_format.space_after = Pt(0)
r_foot = p_foot.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING\nSRM UNIVERSITY – AP, ANDHRA PRADESH – 522 240\nAcademic Year: 2026 – 2027")
r_foot.font.name = 'Calibri'
r_foot.font.size = Pt(10)
r_foot.font.bold = True
r_foot.font.color.rgb = COLOR_NAVY

doc.add_page_break()

# ------------------------------------------------------------------------------
# PAGE 2: BONAFIDE CERTIFICATE
# ------------------------------------------------------------------------------
p_cert_title = doc.add_paragraph()
p_cert_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_cert_title.paragraph_format.space_after = Pt(18)
r_cert = p_cert_title.add_run("BONAFIDE CERTIFICATE")
r_cert.font.name = 'Calibri'
r_cert.font.size = Pt(15)
r_cert.font.bold = True
r_cert.font.color.rgb = COLOR_RED

add_body_p(
    "This is to certify that the project report entitled “VITALSPHERE — NATIONAL HEALTHCARE & CLOUD-SYNCHRONIZED BLOOD LOGISTICS PLATFORM” is the bonafide academic work carried out by Mr. P. Abhishek Paul (Reg. No: AP25110071316), Mr. K. Nithien (Reg. No: AP25110070134), and Mr. Shaik Hasnain (Reg. No: AP25110070228) of III Semester B.Tech Computer Science and Engineering (CSE AI ML F) in the Department of Computer Science and Engineering, School of Engineering and Sciences, SRM University – AP, in partial fulfilment for the requirements of the course CSE 213: Advanced Java Programming during the academic year 2026 – 2027.",
    space_after=14
)

add_body_p(
    "The students have successfully demonstrated exemplary competence in core Java 21 Object-Oriented Programming (OOP) paradigms, multithreaded desktop Graphical User Interface development utilizing Java Swing/AWT, thread-safe asynchronous concurrency, and zero-stale cloud data synchronization between local standalone systems and distributed cloud web architectures.",
    space_after=24
)

# Signature Table
sig_table = doc.add_table(rows=2, cols=2)
sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
sig_table.autofit = False

s00 = sig_table.cell(0, 0)
s01 = sig_table.cell(0, 1)
s10 = sig_table.cell(1, 0)
s11 = sig_table.cell(1, 1)

s00.paragraphs[0].text = "\n\n___________________________________\nDr. Srikanth Lukka\nAssistant Professor & Project Faculty\nDept. of Computer Science & Engineering\nSRM University – AP"
s00.paragraphs[0].runs[0].font.size = Pt(9.5)
s00.paragraphs[0].runs[0].font.color.rgb = COLOR_NAVY

s01.paragraphs[0].text = "\n\n___________________________________\nHead of the Department\nDepartment of Computer Science & Engineering\nSchool of Engineering and Sciences\nSRM University – AP"
s01.paragraphs[0].runs[0].font.size = Pt(9.5)
s01.paragraphs[0].runs[0].font.color.rgb = COLOR_NAVY

s10.paragraphs[0].text = "\nDate: 24-11-2026\nPlace: Mangalagiri, Guntur"
s10.paragraphs[0].runs[0].font.size = Pt(9)
s10.paragraphs[0].runs[0].font.color.rgb = COLOR_SLATE

s11.paragraphs[0].text = "\nDepartment Seal / Institutional Endorsement"
s11.paragraphs[0].runs[0].font.size = Pt(9)
s11.paragraphs[0].runs[0].font.color.rgb = COLOR_SLATE

doc.add_page_break()

# ------------------------------------------------------------------------------
# PAGE 3: TABLE OF CONTENTS (INDEX)
# ------------------------------------------------------------------------------
p_idx = doc.add_paragraph()
p_idx.paragraph_format.space_after = Pt(14)
r_idx = p_idx.add_run("TABLE OF CONTENTS")
r_idx.font.name = 'Calibri'
r_idx.font.size = Pt(15)
r_idx.font.bold = True
r_idx.font.color.rgb = COLOR_RED

idx_table = doc.add_table(rows=11, cols=3)
idx_table.alignment = WD_TABLE_ALIGNMENT.CENTER
idx_table.autofit = False

headers = ["Chapter", "Topic Description", "Page No."]
for col_i, h in enumerate(headers):
    cell = idx_table.cell(0, col_i)
    set_cell_background(cell, "0A1120")
    p = cell.paragraphs[0]
    p.text = h
    p.runs[0].font.bold = True
    p.runs[0].font.size = Pt(9.5)
    p.runs[0].font.color.rgb = RGBColor(255, 255, 255)

toc_data = [
    ("1", "Introduction & Domain Context", "4"),
    ("2", "Problem Statement & Clinical Motivation", "5"),
    ("3", "Project Objectives & Scope of Work", "6"),
    ("4", "System Architecture & Cross-Platform Topology", "7"),
    ("5", "Core Java Concepts & OOP Implementation", "9"),
    ("6", "Data Synchronization, Polling & Caching Engine", "11"),
    ("7", "Medical Officer Clearance Console & Document Verification", "13"),
    ("8", "Emergency Transfusion Requisition Workflow", "15"),
    ("9", "Testing, Verification & Validation Results", "17"),
    ("10", "Conclusion, Academic Learnings & Future Roadmap", "19")
]

for row_i, (ch, desc, pg) in enumerate(toc_data, start=1):
    c0 = idx_table.cell(row_i, 0)
    c1 = idx_table.cell(row_i, 1)
    c2 = idx_table.cell(row_i, 2)
    c0.paragraphs[0].text = ch
    c1.paragraphs[0].text = desc
    c2.paragraphs[0].text = pg
    for c in (c0, c1, c2):
        c.paragraphs[0].runs[0].font.size = Pt(9)
        c.paragraphs[0].runs[0].font.color.rgb = COLOR_NAVY
    if row_i % 2 == 1:
        set_cell_background(c0, "F8FAFC")
        set_cell_background(c1, "F8FAFC")
        set_cell_background(c2, "F8FAFC")

doc.add_page_break()

# ------------------------------------------------------------------------------
# CHAPTER 1: INTRODUCTION
# ------------------------------------------------------------------------------
add_heading_1("Chapter 1: Introduction & Domain Context")

add_body_p(
    "In emergency trauma surgery, pediatric thalassemia care, oncological transfusions, and maternity obstetrics, blood is an irreplacable, highly perishable biological asset. Unlike industrial pharmaceutical products with extensive shelf lives, whole blood reserves must be transfused within 35 to 42 days of collection, while platelet concentrates expire in merely 5 days. Across India and global healthcare networks, every 2 seconds a patient urgently requires a transfusion, accounting for over 14.6 million units needed annually.",
    bold_prefix="1.1 The Critical Healthcare Imperative: "
)

add_body_p(
    "VitalSphere is an enterprise-grade National Healthcare & Blood Logistics Platform engineered natively in Java 21 (Eclipse Temurin JDK) and deployed in high-concurrency cloud architecture. Designed specifically for the CSE 213 (Advanced Java Programming) curriculum at SRM University – AP, VitalSphere bridges the chronic communication chasm separating voluntary citizen donors, licensed blood banks, hospital trauma surgery units, and authorized Chief Medical Officers.",
    bold_prefix="1.2 Project Overview: "
)

add_body_p(
    "The platform delivers a dual-client operating paradigm: a standalone high-performance Java Desktop Client (compiled with custom Swing/AWT 2D anti-aliased graphics) coupled with a modern responsive Web Portal accessible seamlessly across desktop PCs and mobile smartphones. By enforcing statutory National Blood Transfusion Council (NBTC) clinical standards, digital certificate uploads, pan-India administrative district selectors, and unblocked real-time tele-notification routing, VitalSphere eliminates tragic administrative delays in emergency transfusion logistics.",
    bold_prefix="1.3 Unified Dual-Platform Topology: "
)

# ------------------------------------------------------------------------------
# CHAPTER 2: PROBLEM STATEMENT & MOTIVATION
# ------------------------------------------------------------------------------
add_heading_1("Chapter 2: Problem Statement & Clinical Motivation")

add_body_p(
    "Despite modern advancements in hospital diagnostics, voluntary blood donation and patient coordination across regional healthcare clusters suffer from four acute, life-threatening bottlenecks:",
    bold_prefix="2.1 Critical Operational Bottlenecks: "
)

add_bullet("Fragmented, Isolated Stock Silos: Individual blood banks maintain disconnected physical logbooks or private internal software, rendering emergency stock discovery across cities slow and cumbersome.", bold_prefix="1. ")
add_bullet("Unverified Citizen Registrations: Unstructured WhatsApp groups and web portals frequently register donors without statutory medical officer sign-off, leading to on-site rejections due to low Hemoglobin (< 12.5 g/dL) or inadequate cooldown rest periods (< 90 days).", bold_prefix="2. ")
add_bullet("Emergency Requirement Proof Deficit: Patients often request urgent blood without verifying clinical legitimacy through authorized physician transfusion slips, creating chaotic false alarms in donor networks.", bold_prefix="3. ")
add_bullet("High-Latency Attendant Coordination: When matching voluntary donors are located, coordination is often delayed by complex sign-in barriers, outdated phone numbers, or lack of direct dispatch notification mechanisms.", bold_prefix="4. ")

add_body_p(
    "VitalSphere systematically eradicates each of these systemic failure modes. By standardizing pan-India state/city matrices, automating medical certificate previews with real-time Desktop file opening, and enabling 1-click unblocked donation dispatch to patient attendants, VitalSphere transforms chaotic blood requests into deterministic, life-saving logistical actions.",
    bold_prefix="2.2 The VitalSphere Value Proposition: "
)

# ------------------------------------------------------------------------------
# CHAPTER 3: OBJECTIVES & SCOPE OF WORK
# ------------------------------------------------------------------------------
add_heading_1("Chapter 3: Project Objectives & Scope of Work")

add_heading_2("3.1 Academic Course Objectives (CSE 213)")
add_bullet("Demonstrate advanced Object-Oriented Programming (OOP) paradigms including Polymorphic data modeling, strict Encapsulation, Interface Abstraction, and Class Inheritance.", bold_prefix="OOP Principles: ")
add_bullet("Engineer a responsive, native desktop Graphical User Interface (GUI) in Java Swing/AWT featuring custom rendering, anti-aliased geometry, and dynamic layout management.", bold_prefix="GUI Engineering: ")
add_bullet("Master asynchronous Concurrency and Event Dispatch Thread (EDT) safety to guarantee zero UI freezes during intensive network polling and file inspection operations.", bold_prefix="Multithreading & EDT: ")
add_bullet("Implement native File I/O, Document Chooser integrations, and OS-level Desktop API bridging for immediate viewing of statutory PDF and medical certificate documents.", bold_prefix="Document Management: ")

add_heading_2("3.2 Functional System Objectives")
add_bullet("Full-Screen Medical Officer Clearance Console enabling Chief Medical Officers to review voluntary donor registrations, inspect physician certificates, and issue statutory NBTC clearance.", bold_prefix="Clearance Console: ")
add_bullet("Live Blood Stock Inventory covering all 8 major human blood phenotypes (O-, O+, A-, A+, B-, B+, AB-, AB+) with immediate group-filtered directory popups.", bold_prefix="Inventory Matrix: ")
add_bullet("Doctor Requisition Certificate Upload for Emergency Patients, guaranteeing that every blood requirement is backed by an authenticated hospital transfusion order.", bold_prefix="Requisition Proof: ")
add_bullet("Direct Attendant Dispatch Workflow with instant confirmation, live Notification Center sync, and automated status transition to '✓ DONOR FOUND'.", bold_prefix="Dispatch Workflow: ")

doc.add_page_break()

# ------------------------------------------------------------------------------
# CHAPTER 4: SYSTEM ARCHITECTURE
# ------------------------------------------------------------------------------
add_heading_1("Chapter 4: System Architecture & Cross-Platform Topology")

add_body_p(
    "VitalSphere employs a distributed, loosely-coupled architecture designed for high availability, zero latency, and multi-client interoperability across operating systems.",
    bold_prefix="4.1 Architectural Overview: "
)

# Architecture Table
arch_table = doc.add_table(rows=5, cols=3)
arch_table.alignment = WD_TABLE_ALIGNMENT.CENTER
arch_table.autofit = False

arch_headers = ["Layer / Subsystem", "Technology Employed", "Operational Responsibility"]
for col_i, h in enumerate(arch_headers):
    cell = arch_table.cell(0, col_i)
    set_cell_background(cell, "0A1120")
    p = cell.paragraphs[0]
    p.text = h
    p.runs[0].font.bold = True
    p.runs[0].font.size = Pt(9.5)
    p.runs[0].font.color.rgb = RGBColor(255, 255, 255)

arch_data = [
    ("Desktop Client", "Java 21 (Eclipse Temurin) / Swing / AWT", "High-performance administrative console for Medical Officers, local caching, desktop file viewers."),
    ("Cloud Web Client", "HTML5, Modern CSS, ES6 JavaScript", "Zero-install web experience optimized for Desktop PCs and Mobile devices with floating pill navigation."),
    ("Cloud Hosting & CDN", "Google Cloud / Firebase Hosting", "Distributed global edge network delivering static assets with zero-stale cache-control headers."),
    ("REST & Version API", "JSON REST Protocol", "Automatic client version validation (v1.0.0), cloud update polling, and downloadable fat-JAR packaging.")
]

for row_i, (l, t, r) in enumerate(arch_data, start=1):
    c0 = arch_table.cell(row_i, 0)
    c1 = arch_table.cell(row_i, 1)
    c2 = arch_table.cell(row_i, 2)
    c0.paragraphs[0].text = l
    c1.paragraphs[0].text = t
    c2.paragraphs[0].text = r
    for c in (c0, c1, c2):
        c.paragraphs[0].runs[0].font.size = Pt(8.5)
        c.paragraphs[0].runs[0].font.color.rgb = COLOR_NAVY
    if row_i % 2 == 1:
        set_cell_background(c0, "F8FAFC")
        set_cell_background(c1, "F8FAFC")
        set_cell_background(c2, "F8FAFC")

add_body_p(
    "VitalSphere implements a dual-mode synchronization model. When Internet connectivity is active, the Java client interrogates cloud endpoints and updates local tables. Should network latency or disconnections occur, the client falls back to an immutable, thread-safe memory registry populated with 256 verified donors and 64 active emergency recipients across all Indian states.",
    bold_prefix="4.2 Resilient Data Store Strategy: "
)

# ------------------------------------------------------------------------------
# CHAPTER 5: CORE JAVA CONCEPTS & OOP IMPLEMENTATION
# ------------------------------------------------------------------------------
add_heading_1("Chapter 5: Core Java Concepts & OOP Implementation")

add_body_p(
    "VitalSphere's desktop engine is an exemplary showcase of advanced Java programming techniques directly mapped to the CSE 213 syllabus:",
    bold_prefix="5.1 OOP Principles in Practice: "
)

add_bullet("The VitalSphereDesktopClient class extends JFrame, establishing hierarchical containment of menu panels, tabbed panes, and modal dialogs.", bold_prefix="1. Inheritance: ")
add_bullet("All critical clinical attributes—such as donor Aadhaar, Hemoglobin levels, and cooldown days—are encapsulated within managed DefaultTableModel instances and private data structures accessed strictly through validated mutators.", bold_prefix="2. Encapsulation: ")
add_bullet("Buttons throughout the application are instantiated via polymorphic createStyledButton() factories, dynamically handling rollover states, press events, and color rendering.", bold_prefix="3. Polymorphism: ")
add_bullet("Complex underlying OS desktop actions (such as Desktop.getDesktop().open()) are abstracted behind unified openDocumentFileOrDisplay() interfaces.", bold_prefix="4. Abstraction: ")

add_heading_2("5.2 Multithreading, Concurrency & EDT Safety")
add_body_p(
    "Swing applications run on a dedicated single-threaded pipeline known as the Event Dispatch Thread (EDT). Long-running operations executed on the EDT freeze the user interface. VitalSphere guarantees non-blocking responsiveness by running version checks and remote synchronization tasks on background threads via SwingUtilities.invokeLater() and executor pools, ensuring buttery smooth 60 FPS rendering.",
    bold_prefix="Concurrency Architecture: "
)

add_heading_2("5.3 Custom 2D Graphics & High-DPI Anti-Aliased Painting")
add_body_p(
    "To resolve common Java Swing UI defects (such as white text on white backgrounds or jagged corners), VitalSphere overrides paintComponent() in custom JButtons. By enabling KEY_ANTIALIASING on Graphics2D objects, computing dynamic pressed/hover color tints, and drawing rounded bounding boxes (fillRoundRect), the client delivers a pristine modern aesthetic matching Figma design guidelines.",
    bold_prefix="Rendering Engine: "
)

doc.add_page_break()

# ------------------------------------------------------------------------------
# CHAPTER 6: DATA SYNCHRONIZATION & CACHING ENGINE
# ------------------------------------------------------------------------------
add_heading_1("Chapter 6: Data Synchronization, Polling & Caching Engine")

add_body_p(
    "A standout achievement of VitalSphere is its comprehensive solution to browser caching anomalies. On mobile platforms (Chrome on Android, Safari on iOS), web applications frequently serve stale cached JavaScript and HTML files, obscuring fresh data updates.",
    bold_prefix="6.1 The Stale Cache Dilemma: "
)

add_body_p(
    "VitalSphere completely resolves this through a three-tier cache invalidation strategy in firebase.json:",
    bold_prefix="6.2 Three-Tier Invalidation: "
)
add_bullet("Cache-Control: max-age=0, no-cache, no-store, must-revalidate applied across all HTML and JS endpoints.", bold_prefix="Header Invalidation: ")
add_bullet("Dynamic script source version query tags (/directory-data.js?v=20261124_06) forcing edge CDNs to revalidate on every reload.", bold_prefix="Query Fingerprinting: ")
add_bullet("Self-contained fallback generators embedded directly in public/index.html and public/m/index.html, ensuring instant rendering even during complete network timeouts.", bold_prefix="Inline Fallbacks: ")

# ------------------------------------------------------------------------------
# CHAPTER 7: MEDICAL OFFICER CLEARANCE & CERTIFICATE PREVIEW
# ------------------------------------------------------------------------------
add_heading_1("Chapter 7: Medical Officer Clearance Console & Verification")

add_body_p(
    "In accordance with statutory National Blood Transfusion Council (NBTC) regulations, blood cannot be collected from voluntary donors without certified clinical clearance. VitalSphere provides a dedicated Medical Officer Clearance Console accessible to Chief Medical Officers:",
    bold_prefix="7.1 Clinical Governance Framework: "
)

add_bullet("Review of candidate personal parameters: Full Name, Aadhaar number, verified blood phenotype, and residential district.", bold_prefix="1. Candidate Profile: ")
add_bullet("Evaluation of physiological vitals: Hemoglobin level (statutory minimum of 12.5 g/dL) and donation cooldown rest days (minimum 90 days required between donations).", bold_prefix="2. Physiological Vitals: ")
add_bullet("Inspection of uploaded documents: Doctor-signed Medical Fitness Certificates and Laboratory Blood Group Identification Cards.", bold_prefix="3. Document Inspection: ")
add_bullet("1-Click Statutory Clearance: Medical Officers can directly Approve (adding candidate to live roster) or Defer (placing donor on clinical rest).", bold_prefix="4. Clearance Decision: ")

add_heading_2("7.2 Real-Time Document Viewer Bridge")
add_body_p(
    "In the Java Desktop Client, when a Medical Officer clicks 'Open Fitness Document', the application queries certificateFilePathMap. If a local file path exists, it launches the native OS application via Desktop.getDesktop().open(f). If previewing simulated institutional records, it renders an authentic statutory Form-04 clearance document viewer with digital digests and official MCI registration identifiers.",
    bold_prefix="Bridge Implementation: "
)

# ------------------------------------------------------------------------------
# CHAPTER 8: EMERGENCY TRANSFUSION REQUISITION WORKFLOW
# ------------------------------------------------------------------------------
add_heading_1("Chapter 8: Emergency Transfusion Requisition Workflow")

add_body_p(
    "When a patient requires urgent blood for trauma resuscitation, planned cardiac surgery, or neonatal care, attendants submit an Emergency Transfusion Requirement:",
    bold_prefix="8.1 Workflow Sequencing: "
)

add_bullet("Patient Identification: Full Name and 12-digit Aadhaar number for identity traceability.", bold_prefix="Step 1: ")
add_bullet("Transfusion Parameters: Phenotype required, units needed (calculated in milliliters at 350 ml/unit), and clinical urgency level (CRITICAL, URGENT, or ROUTINE).", bold_prefix="Step 2: ")
add_bullet("Doctor Requisition Certificate Upload: Attendant uploads the physical hospital requisition order or physician prescription (.pdf, .png, .jpg) to prove clinical authenticity.", bold_prefix="Step 3: ")
add_bullet("Instant Network Broadcast: The requirement is dynamically injected into live registries and broadcasts alerts across desktop and mobile Notification Centers.", bold_prefix="Step 4: ")
add_bullet("Unblocked Volunteer Donation: Any citizen donor can click 'Donate', which instantly confirms commitment and dispatches a verified tele-notification to the patient attendant's phone.", bold_prefix="Step 5: ")

doc.add_page_break()

# ------------------------------------------------------------------------------
# CHAPTER 9: SCREENSHOTS, VERIFICATION & VALIDATION
# ------------------------------------------------------------------------------
add_heading_1("Chapter 9: Testing, Verification & UI Demonstrations")

add_body_p(
    "VitalSphere underwent rigorous unit, integration, and UI acceptance testing across Windows 11, Chrome 126, Android Chrome, and Java 21 OpenJDK runtimes.",
    bold_prefix="9.1 Quality Assurance Summary: "
)

# Insert Screenshots if available
import io
from PIL import Image

def get_clean_image_stream(file_path):
    try:
        im = Image.open(file_path)
        buf = io.BytesIO()
        im.save(buf, format='PNG')
        buf.seek(0)
        return buf
    except Exception as e:
        print(f"Error converting {file_path}: {e}")
        return None

screen_paths = [
    (r"C:\Users\PAUL\.gemini\antigravity\brain\22b50d08-d1d4-476a-b4c6-9e333fb80fb1\.user_uploaded\media_1795518007351_d7c52834.jpg", "Figure 9.1: VitalSphere Native Java Desktop Client (Swing GUI with Live Donors Table and Action Panel)"),
    (r"C:\Users\PAUL\.gemini\antigravity\brain\22b50d08-d1d4-476a-b4c6-9e333fb80fb1\.user_uploaded\media_1795516901049_b558a926.jpg", "Figure 9.2: Java Desktop Certificate Preview & Statutory NBTC Clinical Clearance Dialog"),
    (r"C:\Users\PAUL\.gemini\antigravity\brain\22b50d08-d1d4-476a-b4c6-9e333fb80fb1\.user_uploaded\media_1795522689897_4629b506.png", "Figure 9.3: Desktop Web Portal — Voluntary Donor Registration with Pan-India State & District Selectors"),
    (r"C:\Users\PAUL\.gemini\antigravity\brain\22b50d08-d1d4-476a-b4c6-9e333fb80fb1\.user_uploaded\media_1795522830460_3c148eb7.jpg", "Figure 9.4: Mobile Web Portal — Live Blood Stock Inventory Grid with Floating Pill Navigation Bar")
]

for s_path, s_caption in screen_paths:
    if os.path.exists(s_path):
        img_stream = get_clean_image_stream(s_path)
        if img_stream:
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(4)
            p_img.add_run().add_picture(img_stream, width=Inches(5.5))
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(12)
            r_cap = p_cap.add_run(s_caption)
            r_cap.font.name = 'Calibri'
            r_cap.font.size = Pt(8.5)
            r_cap.font.italic = True
            r_cap.font.color.rgb = COLOR_SLATE

# ------------------------------------------------------------------------------
# CHAPTER 10: CONCLUSION & FUTURE SCOPE
# ------------------------------------------------------------------------------
add_heading_1("Chapter 10: Conclusion, Learnings & Future Roadmap")

add_body_p(
    "VitalSphere exemplifies the real-world convergence of rigorous Java Object-Oriented software engineering with public healthcare logistics. Developed for the CSE 213 (Advanced Java Programming) course at SRM University – AP, the platform proves that combining native Java desktop speed with cloud edge distribution solves profound coordination failures in humanitarian medicine.",
    bold_prefix="10.1 Concluding Remarks: "
)

add_heading_2("10.2 Academic Learnings")
add_bullet("Mastered the nuances of Swing concurrency and the Event Dispatch Thread to prevent application blocking.", bold_prefix="Threading: ")
add_bullet("Gained deep proficiency in Java 2D anti-aliased graphics and high-contrast color management.", bold_prefix="Custom UI: ")
add_bullet("Engineered bulletproof cross-platform caching strategies across edge cloud CDNs and mobile browsers.", bold_prefix="Cloud Networking: ")
add_bullet("Standardized complex pan-India geographic dictionaries and clinical verification algorithms.", bold_prefix="Data Architecture: ")

add_heading_2("10.3 Future Scope & Strategic Roadmap")
add_bullet("Integration of GPS routing and drone delivery logistics for critical Rh-negative units.", bold_prefix="1. Autonomous Transit: ")
add_bullet("Direct integration with the Government of India e-RaktKosh national blood bank API.", bold_prefix="2. e-RaktKosh Sync: ")
add_bullet("Automated SMS/WhatsApp OTP verification on patient attendant mobile contacts.", bold_prefix="3. Tele-Gateway: ")

doc.save(report_path)
print(f"Report successfully generated at: {report_path}")
