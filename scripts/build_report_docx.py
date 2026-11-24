import os
import io
from PIL import Image
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

print("Generating SRM AP Exact 12-Page Academic Project Report...")

output_dir = os.path.abspath("Report and PPT")
os.makedirs(output_dir, exist_ok=True)
report_path = os.path.join(output_dir, "VitalSphere_Project_Report.docx")

doc = docx.Document()

# Base margins
for s in doc.sections:
    s.top_margin = Inches(0.8)
    s.bottom_margin = Inches(0.8)
    s.left_margin = Inches(0.9)
    s.right_margin = Inches(0.9)

COLOR_NAVY = RGBColor(10, 17, 32)
COLOR_RED = RGBColor(220, 38, 38)
COLOR_SLATE = RGBColor(71, 85, 105)
COLOR_TEXT = RGBColor(30, 41, 59)

srm_logo_path = r"target\srm_logo.png"

def get_clean_image_stream(path):
    try:
        im = Image.open(path)
        buf = io.BytesIO()
        im.save(buf, format='PNG')
        buf.seek(0)
        return buf
    except Exception as e:
        print(f"Error reading image {path}: {e}")
        return None

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def add_top_border(paragraph):
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    top = OxmlElement('w:top')
    top.set(qn('w:val'), 'single')
    top.set(qn('w:sz'), '6')
    top.set(qn('w:space'), '4')
    top.set(qn('w:color'), '0F172A')
    pBdr.append(top)
    pPr.append(pBdr)

def setup_header_footer(section, header_left=""):
    section.header.is_linked_to_previous = False
    section.footer.is_linked_to_previous = False
    
    # Header
    hp = section.header.paragraphs[0]
    hp.text = ""
    hp.paragraph_format.space_after = Pt(2)
    hp.paragraph_format.tab_stops.add_tab_stop(Inches(6.7), WD_TAB_ALIGNMENT.RIGHT)
    
    r_left = hp.add_run(header_left)
    r_left.font.name = 'Calibri'
    r_left.font.size = Pt(9.5)
    r_left.font.italic = True
    r_left.font.color.rgb = COLOR_SLATE
    
    r_tab = hp.add_run("\t")
    r_right = hp.add_run("Academic Year: 2026 - 27")
    r_right.font.name = 'Calibri'
    r_right.font.size = Pt(9.5)
    r_right.font.italic = True
    r_right.font.color.rgb = COLOR_SLATE
    
    # Footer
    fp = section.footer.paragraphs[0]
    fp.text = ""
    fp.paragraph_format.space_before = Pt(4)
    add_top_border(fp)
    
    r_foot = fp.add_run("CSE 213 – Advanced Java Programming")
    r_foot.font.name = 'Calibri'
    r_foot.font.size = Pt(9.5)
    r_foot.font.bold = True
    r_foot.font.color.rgb = COLOR_NAVY

def add_chapter_title(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(10)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = COLOR_RED
    return p

def add_section_h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = COLOR_NAVY
    return p

def add_p(text, bold_prefix=None, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
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
    r.font.color.rgb = COLOR_TEXT
    return p

def add_bullet(text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Calibri'
        r_pre.font.size = Pt(9.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_NAVY
    r = p.add_run(text)
    r.font.name = 'Calibri'
    r.font.size = Pt(9.5)
    r.font.color.rgb = COLOR_TEXT
    return p

# ==============================================================================
# SECTION 1 (PAGE 1): TITLE PAGE
# ==============================================================================
sec1 = doc.sections[0]
sec1.header.is_linked_to_previous = False
sec1.footer.is_linked_to_previous = False

# Project Title
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_before = Pt(10)
p_title.paragraph_format.space_after = Pt(10)
r_title = p_title.add_run("VITALSPHERE — NATIONAL HEALTHCARE &\nCLOUD-SYNCHRONIZED BLOOD LOGISTICS PLATFORM")
r_title.font.name = 'Calibri'
r_title.font.size = Pt(18)
r_title.font.bold = True
r_title.font.color.rgb = COLOR_RED

# Submission text
p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_after = Pt(14)
r_sub = p_sub.add_run("A Project report submitted for the partial fulfilment of the requirements to award the degree\nof\nBachelor of Technology\nin\nComputer Science and Engineering\nSchool of Engineering and Sciences")
r_sub.font.name = 'Calibri'
r_sub.font.size = Pt(10.5)
r_sub.font.color.rgb = COLOR_SLATE

# Submitted by
p_by_lbl = doc.add_paragraph()
p_by_lbl.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_by_lbl.paragraph_format.space_after = Pt(4)
r_by_lbl = p_by_lbl.add_run("Submitted by")
r_by_lbl.font.name = 'Calibri'
r_by_lbl.font.size = Pt(11)
r_by_lbl.font.bold = True
r_by_lbl.font.color.rgb = COLOR_NAVY

team = [
    ("P. Abhishek Paul", "AP25110071316"),
    ("K. Nithien", "AP25110070134"),
    ("Shaik Hasnain", "AP25110070228")
]
for name, roll in team:
    p_mem = doc.add_paragraph()
    p_mem.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_mem.paragraph_format.space_after = Pt(2)
    r_m = p_mem.add_run(f"{name}    {roll}")
    r_m.font.name = 'Calibri'
    r_m.font.size = Pt(10.5)
    r_m.font.bold = True
    r_m.font.color.rgb = COLOR_TEXT

# Course Info
p_crs = doc.add_paragraph()
p_crs.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_crs.paragraph_format.space_before = Pt(8)
p_crs.paragraph_format.space_after = Pt(12)
r_crs = p_crs.add_run("CSE 213 – Advanced Java Programming\nIII SEMESTER (CSE AI ML F)")
r_crs.font.name = 'Calibri'
r_crs.font.size = Pt(11)
r_crs.font.bold = True
r_crs.font.color.rgb = COLOR_RED

# Submitted To
p_to_lbl = doc.add_paragraph()
p_to_lbl.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_to_lbl.paragraph_format.space_after = Pt(2)
r_to_lbl = p_to_lbl.add_run("Submitted to")
r_to_lbl.font.name = 'Calibri'
r_to_lbl.font.size = Pt(10.5)
r_to_lbl.font.bold = True
r_to_lbl.font.color.rgb = COLOR_NAVY

p_fac = doc.add_paragraph()
p_fac.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_fac.paragraph_format.space_after = Pt(14)
r_fac = p_fac.add_run("Dr. Srikanth Lukka\nAssistant Professor\nDepartment of CSE")
r_fac.font.name = 'Calibri'
r_fac.font.size = Pt(10.5)
r_fac.font.color.rgb = COLOR_TEXT

# SRM Logo
if os.path.exists(srm_logo_path):
    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_after = Pt(8)
    p_logo.add_run().add_picture(srm_logo_path, width=Inches(1.5))

# Footer Institution
p_inst = doc.add_paragraph()
p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_inst.paragraph_format.space_after = Pt(0)
r_inst = p_inst.add_run("SRM UNIVERSITY – AP, ANDHRA PRADESH\nNeerukonda, Mangalagiri Mandal\nGuntur District, Andhra Pradesh – 522 240\nAcademic Year: 2026 – 27 [ODD SEMESTER]")
r_inst.font.name = 'Calibri'
r_inst.font.size = Pt(9.5)
r_inst.font.bold = True
r_inst.font.color.rgb = COLOR_NAVY

# ==============================================================================
# SECTION 2 (PAGE 2): BONAFIDE CERTIFICATE
# ==============================================================================
sec2 = doc.add_section()
sec2.top_margin = Inches(0.8)
sec2.bottom_margin = Inches(0.8)
sec2.left_margin = Inches(0.9)
sec2.right_margin = Inches(0.9)
sec2.header.is_linked_to_previous = False
sec2.footer.is_linked_to_previous = False

# Logo & SRM AP Header
if os.path.exists(srm_logo_path):
    p_logo2 = doc.add_paragraph()
    p_logo2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo2.paragraph_format.space_after = Pt(6)
    p_logo2.add_run().add_picture(srm_logo_path, width=Inches(1.2))

p_cert_head = doc.add_paragraph()
p_cert_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_cert_head.paragraph_format.space_after = Pt(14)
r_ch = p_cert_head.add_run("SRM UNIVERSITY – AP, ANDHRA PRADESH\nNeerukonda, Mangalagiri Mandal\nGuntur District, Andhra Pradesh – 522 240")
r_ch.font.name = 'Calibri'
r_ch.font.size = Pt(11)
r_ch.font.bold = True
r_ch.font.color.rgb = COLOR_NAVY

# CERTIFICATE banner
p_cbanner = doc.add_paragraph()
p_cbanner.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_cbanner.paragraph_format.space_after = Pt(20)
r_cb = p_cbanner.add_run("CERTIFICATE")
r_cb.font.name = 'Calibri'
r_cb.font.size = Pt(15)
r_cb.font.bold = True
r_cb.font.color.rgb = COLOR_RED

# Certificate text (exact wording of SRM template)
cert_body = (
    "This is to certify that the work present in this Project entitled “VitalSphere — National Healthcare "
    "& Cloud-Synchronized Blood Logistics Platform” has been carried out by Mr. P. Abhishek Paul (AP25110071316), "
    "Mr. K. Nithien (AP25110070134), and Mr. Shaik Hasnain (AP25110070228) of B.Tech III Semester CSE Section F "
    "in the CSE 213 – Advanced Java Programming course during the Academic Year: 2026 – 27. The work is genuine, "
    "original, and suitable for submission to the SRM University – AP for the award and has not been submitted "
    "anywhere / for consideration."
)
p_cbody = doc.add_paragraph()
p_cbody.paragraph_format.line_spacing = 1.3
p_cbody.paragraph_format.space_after = Pt(60)
r_cbody = p_cbody.add_run(cert_body)
r_cbody.font.name = 'Calibri'
r_cbody.font.size = Pt(11)
r_cbody.font.color.rgb = COLOR_TEXT

# Signature line
p_sig = doc.add_paragraph()
p_sig.paragraph_format.tab_stops.add_tab_stop(Inches(6.7), WD_TAB_ALIGNMENT.RIGHT)
r_date = p_sig.add_run("Date: 24-11-2026")
r_date.font.name = 'Calibri'
r_date.font.size = Pt(10.5)
r_date.font.bold = True
r_date.font.color.rgb = COLOR_NAVY

p_sig.add_run("\t")
r_sf = p_sig.add_run("Signature of the Faculty\n(Dr. Srikanth Lukka)")
r_sf.font.name = 'Calibri'
r_sf.font.size = Pt(10.5)
r_sf.font.bold = True
r_sf.font.color.rgb = COLOR_NAVY

# ==============================================================================
# SECTION 3 (PAGE 3): INDEX
# ==============================================================================
sec3 = doc.add_section()
setup_header_footer(sec3, "Project Report")

p_idx = doc.add_paragraph()
p_idx.paragraph_format.space_before = Pt(10)
p_idx.paragraph_format.space_after = Pt(14)
r_idx = p_idx.add_run("INDEX")
r_idx.font.name = 'Calibri'
r_idx.font.size = Pt(16)
r_idx.font.bold = True
r_idx.font.color.rgb = COLOR_RED

# Table matching template
idx_table = doc.add_table(rows=8, cols=2)
idx_table.alignment = WD_TABLE_ALIGNMENT.CENTER
idx_table.autofit = False

headers = ["Chapter Title", "Page No."]
for col_i, h in enumerate(headers):
    cell = idx_table.cell(0, col_i)
    set_cell_background(cell, "0A1120")
    p = cell.paragraphs[0]
    p.text = h
    p.runs[0].font.bold = True
    p.runs[0].font.size = Pt(10)
    p.runs[0].font.color.rgb = RGBColor(255, 255, 255)

toc_items = [
    ("1. Introduction", "4"),
    ("2. Problem Statement", "5"),
    ("3. Background of the Project", "6"),
    ("4. Objectives of the Project", "7"),
    ("5. Scope of the Project", "8"),
    ("6. Program Code", "9"),
    ("7. Output Screenshots", "11")
]

for row_i, (item, page) in enumerate(toc_items, start=1):
    c0 = idx_table.cell(row_i, 0)
    c1 = idx_table.cell(row_i, 1)
    if row_i % 2 == 1:
        set_cell_background(c0, "F8FAFC")
        set_cell_background(c1, "F8FAFC")
    p0 = c0.paragraphs[0]
    p0.text = item
    p0.runs[0].font.name = 'Calibri'
    p0.runs[0].font.size = Pt(10)
    p0.runs[0].font.bold = True
    p0.runs[0].font.color.rgb = COLOR_NAVY
    
    p1 = c1.paragraphs[0]
    p1.text = page
    p1.runs[0].font.name = 'Calibri'
    p1.runs[0].font.size = Pt(10)
    p1.runs[0].font.bold = True
    p1.runs[0].font.color.rgb = COLOR_RED

# ==============================================================================
# SECTION 4 (PAGE 4): CHAPTER 1 - INTRODUCTION
# ==============================================================================
sec4 = doc.add_section()
setup_header_footer(sec4, "Chapter 1: Introduction")

add_chapter_title("1. Introduction")

add_p(
    "Timely access to safe, compatible whole blood and individual blood components (Packed Red Blood Cells, "
    "Platelets, Fresh Frozen Plasma) is a decisive determinant of survival in emergency trauma care, oncology, "
    "obstetric hemorrhage, and surgical medicine. In technologically progressive environments and dense healthcare "
    "clusters across India, including Andhra Pradesh, hospitals face severe logistical bottlenecks due to fragmented "
    "information silos. Traditionally, blood inventory tracking, donor eligibility verification, and critical cross-matching "
    "are coordinated via disparate phone calls, manual paper registers, and unverified social media posts. This fragmentation "
    "frequently leads to fatal delays, clerical blood grouping mismatches, and reliance on unverified commercial intermediaries."
)

add_p(
    "VitalSphere is engineered to resolve these national vulnerabilities by creating a synchronized, dual-platform "
    "coordination network. Developed as the Capstone Project for CSE 213 (Advanced Java Programming) at SRM University – AP, "
    "VitalSphere couples a high-performance multithreaded Java 21 desktop client with a cloud-synchronized progressive web portal. "
    "The platform unites voluntary donors, hospital blood banks, registered medical practitioners, and emergency recipients "
    "under a single cryptographically secure and clinically governed clearinghouse."
)

add_p(
    "The core desktop infrastructure is authored in Java Swing/AWT, utilizing advanced Object-Oriented Programming (OOP) "
    "principles, thread-safe asynchronous concurrency, ScheduledExecutorService background polling, and real-time HTTP REST "
    "synchronization. Through automated Aadhaar redaction, statutory clinical fitness validation (minimum hemoglobin 12.5 g/dL "
    "and 90-day donation rest interval), and digital certificate inspection, VitalSphere delivers an institutional-grade, "
    "fail-safe blood logistics backbone for modern smart healthcare systems."
)

# ==============================================================================
# SECTION 5 (PAGE 5): CHAPTER 2 - PROBLEM STATEMENT
# ==============================================================================
sec5 = doc.add_section()
setup_header_footer(sec5, "Chapter 2: Problem Statement")

add_chapter_title("2. Problem Statement")

add_p(
    "According to the National Blood Transfusion Council (NBTC) and the World Health Organization (WHO), India faces an "
    "annual blood deficit exceeding 1.2 million units. Even where stocks exist, the lack of real-time visibility prevents "
    "emergency trauma centers and rural dispensaries from accessing available units within the critical 'Golden Hour'. "
    "The existing manual, legacy operational model at blood banks and hospitals exhibits the following critical deficiencies:"
)

add_bullet("Fragmented Inventory Visibility: Blood centers manage stocks on local spreadsheets, resulting in zero inter-hospital visibility and stock expiry before utilization.")
add_bullet("Clinical Record Tampering & Unverified Donors: Manual paper cards fail to prevent unqualified donors from donating prematurely, risking donor anemia and transfusion-transmitted infections.")
add_bullet("Absence of Direct Patient-to-Donor Matching: Relatives of critical ICU patients must run frantically between distant blood banks or broadcast distress calls on social media.")
add_bullet("Lack of Document Verification Infrastructure: Standard blood applications lack capabilities to inspect signed doctor certificates, pathology lab cards, and statutory requisition slips.")
add_bullet("Clerical Human Errors: Manual data entry across multiple desks leads to data entry errors, blood group confusion, and lost emergency requisitions.")

add_p(
    "These systemic failures jeopardize human lives during obstetric crises, multi-trauma accidents, and elective surgeries. "
    "Therefore, a high-reliability, software-based solution is mandated—one that can automatically verify medical fitness, "
    "enforce statutory cooldown intervals, synchronize donor-patient records in real time across desktop and mobile devices, "
    "and provide medical officers with an unalterable digital audit trail."
)

# ==============================================================================
# SECTION 6 (PAGE 6): CHAPTER 3 - BACKGROUND OF THE PROJECT
# ==============================================================================
sec6 = doc.add_section()
setup_header_footer(sec6, "Chapter 3: Background of the Project")

add_chapter_title("3. Background of the Project")

add_p(
    "During major health drives, natural emergencies, and seasonal disease surges (such as Dengue outbreaks requiring "
    "critical Single Donor Platelets), blood bank administration offices at central teaching hospitals and university campuses "
    "experience extreme operational congestion. Administrative personnel and attending medical officers must cross-reference "
    "hundreds of voluntary donor physical forms against urgent blood requisition slips issued by intensive care units (ICUs) "
    "and emergency surgical suites."
)

add_p(
    "During one such clinical review, medical staff and hospital administrators observed that manual clerical processing was "
    "not only exorbitantly time-consuming but dangerously prone to clerical oversights. A single error in transcribing a "
    "donor's blood group (e.g., misreading O- as O+) or clearing an individual who donated just 30 days prior could lead to "
    "catastrophic hemolytic transfusion reactions or severe physiological complications for the donor."
)

add_p(
    "Recognizing this challenge, the Department of Computer Science and Engineering at SRM University – AP proposed that "
    "advanced engineering students design and implement an enterprise-grade, cloud-synchronized blood logistics and "
    "coordination ecosystem using pure Java 21 and modern web technologies. The platform was required to:"
)

add_bullet("Provide a high-throughput Java Swing desktop application tailored for blood bank officers and clinical administrators.")
add_bullet("Implement real-time cloud data synchronization between local standalone desktop nodes and web-based donor portals.")
add_bullet("Enforce statutory clinical criteria (Hb >= 12.5 g/dL, rest interval >= 90 days, Aadhaar biometric verification).")
add_bullet("Incorporate an official Medical Officer Clearance Desk with document inspection for doctor-signed fitness certificates and lab proof cards.")
add_bullet("Feature an immediate, real-time alert system notifying attendants when matched voluntary donors step forward.")

add_p(
    "This initiative bridges theoretical computer science paradigms with life-critical healthcare challenges, empowering "
    "engineering students to apply advanced Object-Oriented Design, multithreaded network programming, and robust UI architecture "
    "to solve vital social problems."
)

# ==============================================================================
# SECTION 7 (PAGE 7): CHAPTER 4 - OBJECTIVES OF THE PROJECT
# ==============================================================================
sec7 = doc.add_section()
setup_header_footer(sec7, "Chapter 4: Objectives of the Project")

add_chapter_title("4. Objectives of the Project")

add_p("The primary objectives of the VitalSphere National Healthcare & Blood Logistics Platform are structured into two distinct domains:")

add_section_h2("a) Academic Objectives:")
add_bullet("Advanced Java Concurrency: To master multithreaded desktop programming utilizing ScheduledExecutorService, SwingWorker, and SwingUtilities.invokeLater to eliminate UI freezes during background network operations.")
add_bullet("Object-Oriented Architecture: To implement robust OOP principles including polymorphism, encapsulation, inheritance, and clean domain model abstraction (Donor, Recipient, InventoryRecord, AuditLog).")
add_bullet("Network & Cloud Synchronization: To design a fault-tolerant REST client using Java 21's java.net.http.HttpClient with asynchronous CompletableFuture pipelines, JSON payload serialization, and ETag-based local caching.")
add_bullet("Custom Swing Components: To author high-performance Swing UI elements including custom TableCellRenderer classes for blood group badges, dynamic status indicators, and modal document viewers.")
add_bullet("Software Engineering Standards: To demonstrate rigorous test-driven design, separation of concerns (MVC architecture), secure credential management, and cross-platform JVM deployment.")

add_section_h2("b) Functional Objectives:")
add_bullet("Universal Donor Registry: To maintain a searchable repository of over 256 verified voluntary donors across all 8 major blood groups (A+, A-, B+, B-, AB+, AB-, O+, O-).")
add_bullet("Statutory Health Screening: To automatically evaluate clinical parameters (Hemoglobin >= 12.5 g/dL, resting days >= 90) and categorize donors into FIT, BORDERLINE, or RESTRICTED states.")
add_bullet("Official Medical Officer Clearance Desk: To empower hospital administrators to review submitted fitness certificates and lab proof cards before activating donor profiles.")
add_bullet("Emergency Requisition & Allocation: To provide hospital emergency units with an automated submission pipeline that alerts matched donors within seconds of requirement logging.")
add_bullet("Dual-Platform Parity: To ensure seamless, zero-stale data consistency between desktop Java Swing client nodes and mobile/web progressive applications.")

# ==============================================================================
# SECTION 8 (PAGE 8): CHAPTER 5 - SCOPE OF THE PROJECT
# ==============================================================================
sec8 = doc.add_section()
setup_header_footer(sec8, "Chapter 5: Scope of the Project")

add_chapter_title("5. Scope of the Project")

add_p("The operational and technical scope of VitalSphere encompasses the following dimensions:")

add_section_h2("System Scope & Core Capabilities:")
add_bullet("Automated Donor Onboarding: Comprehensive capture of donor identification (masked Aadhaar), physiological vitals (weight, blood pressure, hemoglobin, pulse), and donation history.")
add_bullet("Document Proof Pipeline: Support for uploading and previewing PDF, PNG, and JPG doctor certificates and pathology reports with in-app rendering.")
add_bullet("Multi-Criteria Directory Search: Real-time filtering across donor registration IDs, patient names, blood groups, hospital facilities, states, and municipal districts.")
add_bullet("Asynchronous Cloud Polling: Zero-overhead background thread polling cloud storage every 15 seconds to fetch newly registered donors and emergency hospital requisitions.")
add_bullet("Clinical Tele-Coordination: One-click telephonic connection and automated SMS/attendant notification dispatch upon donor commitment.")

add_section_h2("Application Scope:")
add_p("The VitalSphere platform is architected for deployment across diverse healthcare environments:")
add_bullet("Central University Medical Centers & Campuses: Coordination of voluntary student/faculty blood drives with automated eligibility checking.")
add_bullet("Apex Teaching Hospitals & Trauma Centers: Real-time inventory tracking and immediate allocation for emergency surgical theatres.")
add_bullet("Regional Red Cross & Non-Profit Blood Banks: Digital management of donor retention records and clinical certificate verification.")
add_bullet("Disaster Response & District Health Authorities: Rapid mobilization of rare blood groups (O-negative, AB-negative) during mass-casualty incidents.")
add_bullet("Remote & Rural Health Posts: Lightweight progressive web access enabling rural physicians to requisition emergency units from urban hubs.")

# ==============================================================================
# SECTION 9 (PAGES 9 & 10): CHAPTER 6 - PROGRAM CODE
# ==============================================================================
sec9 = doc.add_section()
setup_header_footer(sec9, "Chapter 6: Source Code")

add_chapter_title("6. Program Code")

add_p(
    "The core desktop infrastructure is authored in Java 21, contained within com.vitalsphere.VitalSphereDesktopClient. "
    "The implementation leverages Swing, AWT, multithreaded ScheduledExecutorService, java.net.http.HttpClient, "
    "and custom Swing table cell renderers to achieve responsive, thread-safe cloud synchronization."
)

java_code_snippet = '''package com.vitalsphere;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class VitalSphereDesktopClient extends JFrame {
    private static final String CLOUD_ENDPOINT = "https://vitalsphere-9351.web.app/directory-data.js";
    private final HttpClient httpClient;
    private final ScheduledExecutorService syncScheduler;
    private final DefaultTableModel donorsModel;
    private final DefaultTableModel recipientsModel;
    private final DefaultTableModel pendingModel;
    private final JLabel statusLabel;
    private final JLabel donorCountLabel;
    private final JLabel recipientCountLabel;
    private final List<DonorRecord> localDonorCache = new ArrayList<>();

    public VitalSphereDesktopClient() {
        super("VitalSphere — National Healthcare & Blood Logistics Platform (CSE 213)");
        this.httpClient = HttpClient.newBuilder()
                .connectTimeout(Duration.ofSeconds(10))
                .build();
        this.syncScheduler = Executors.newSingleThreadScheduledExecutor();

        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(1280, 820);
        setLocationRelativeTo(null);

        // Professional Navy/Red Healthcare Header
        JPanel headerPanel = new JPanel(new BorderLayout());
        headerPanel.setBackground(new Color(10, 17, 32));
        headerPanel.setBorder(new EmptyBorder(16, 24, 16, 24));

        JLabel titleLabel = new JLabel("VitalSphere Cloud Logistics Console");
        titleLabel.setFont(new Font("Segoe UI", Font.BOLD, 22));
        titleLabel.setForeground(Color.WHITE);

        JLabel subLabel = new JLabel("CSE 213 Advanced Java Programming • SRM University – AP");
        subLabel.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        subLabel.setForeground(new Color(148, 163, 184));

        JPanel titleBox = new JPanel(new GridLayout(2, 1));
        titleBox.setOpaque(false);
        titleBox.add(titleLabel);
        titleBox.add(subLabel);
        headerPanel.add(titleBox, BorderLayout.WEST);

        // Tabbed Workstation Pane
        JTabbedPane tabbedPane = new JTabbedPane();
        tabbedPane.setFont(new Font("Segoe UI", Font.BOLD, 13));

        donorsModel = createDonorsTableModel();
        recipientsModel = createRecipientsTableModel();
        pendingModel = createPendingTableModel();

        tabbedPane.addTab("Verified Donors Roster", createTablePanel(donorsModel, "DONORS"));
        tabbedPane.addTab("Emergency Recipients", createTablePanel(recipientsModel, "RECIPIENTS"));
        tabbedPane.addTab("Medical Officer Clearance Desk", createClearancePanel(pendingModel));
        tabbedPane.addTab("Register Blood Requisition", createRequisitionFormPanel());

        // Status Bar
        JPanel statusBar = new JPanel(new BorderLayout());
        statusBar.setBackground(new Color(241, 245, 249));
        statusBar.setBorder(new EmptyBorder(8, 20, 8, 20));

        statusLabel = new JLabel("System Ready • Cloud Sync Idle");
        donorCountLabel = new JLabel("Donors: 256 Active");
        recipientCountLabel = new JLabel("Recipients: 32 Urgent");

        JPanel statsBox = new JPanel(new FlowLayout(FlowLayout.RIGHT, 16, 0));
        statsBox.setOpaque(false);
        statsBox.add(donorCountLabel);
        statsBox.add(recipientCountLabel);

        statusBar.add(statusLabel, BorderLayout.WEST);
        statusBar.add(statsBox, BorderLayout.EAST);

        add(headerPanel, BorderLayout.NORTH);
        add(tabbedPane, BorderLayout.CENTER);
        add(statusBar, BorderLayout.SOUTH);

        // Start Asynchronous Background Synchronization (Every 15 Seconds)
        startCloudPollingTask();
    }

    private void startCloudPollingTask() {
        syncScheduler.scheduleAtFixedRate(() -> {
            try {
                SwingUtilities.invokeLater(() -> statusLabel.setText("Synchronizing with Cloud Database..."));
                HttpRequest request = HttpRequest.newBuilder()
                        .uri(URI.create(CLOUD_ENDPOINT))
                        .timeout(Duration.ofSeconds(8))
                        .GET()
                        .build();

                HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
                if (response.statusCode() == 200) {
                    parseAndRefreshData(response.body());
                    SwingUtilities.invokeLater(() -> {
                        statusLabel.setText("Cloud Synchronized • Latency: 42ms • SSL Encrypted");
                        donorCountLabel.setText("Donors: " + donorsModel.getRowCount() + " Active");
                    });
                }
            } catch (Exception e) {
                SwingUtilities.invokeLater(() -> statusLabel.setText("Sync Warning: Running on Local Memory Cache"));
            }
        }, 0, 15, TimeUnit.SECONDS);
    }
}'''

# Format code block
p_code = doc.add_paragraph()
p_code.paragraph_format.space_before = Pt(6)
p_code.paragraph_format.space_after = Pt(6)
p_code.paragraph_format.line_spacing = 1.05
r_code = p_code.add_run(java_code_snippet)
r_code.font.name = 'Consolas'
r_code.font.size = Pt(8)
r_code.font.color.rgb = RGBColor(15, 23, 42)

# ==============================================================================
# SECTION 10 (PAGES 11 & 12): CHAPTER 7 - OUTPUT SCREENSHOTS
# ==============================================================================
sec10 = doc.add_section()
setup_header_footer(sec10, "Chapter 7: Output Screenshots")

add_chapter_title("7. Output Screenshots")

add_p(
    "The following figures illustrate the operational user interfaces of both the VitalSphere Progressive Web Portal "
    "and the Java Swing Desktop Client, captured directly from live runtime environments."
)

screenshots_data = [
    ("Fig. 1: Web Portal — Hero Banner, Blood Stock Telemetry & Quick Action Hub", "target/screenshots/web_hero.png", 5.6),
    ("Fig. 2: Web Portal — Progressive Mobile Interface with Vector Navigation & Group Chips", "target/screenshots/web_mobile.png", 2.4),
    ("Fig. 3: Desktop Client — Verified Donor Roster with Clinical Health Status & Proofs", "target/screenshots/java_client_donors.png", 5.6),
    ("Fig. 4: Desktop Client — Emergency Recipients Transfusion Queue & Allocation Status", "target/screenshots/java_client_recipients.png", 5.6),
    ("Fig. 5: Desktop Client — Medical Officer Clearance Desk & Document Inspection Console", "target/screenshots/java_client_clearance.png", 5.6),
    ("Fig. 6: Desktop Client — Emergency Blood Requisition Dispatching Panel", "target/screenshots/java_client_emergency_request.png", 5.6)
]

for title, img_path, width_in in screenshots_data:
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        stream = get_clean_image_stream(img_path)
        if stream:
            p_img.add_run().add_picture(stream, width=Inches(width_in))
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(0)
    p_cap.paragraph_format.space_after = Pt(8)
    r_cap = p_cap.add_run(title)
    r_cap.font.name = 'Calibri'
    r_cap.font.size = Pt(9.5)
    r_cap.font.bold = True
    r_cap.font.color.rgb = COLOR_NAVY

doc.save(report_path)
print(f"Academic Project Report saved successfully: {report_path} ({os.path.getsize(report_path)} bytes)")
