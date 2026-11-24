import os
import io
from PIL import Image
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

print("Building VitalSphere Professional Presentation (.pptx)...")

output_dir = os.path.abspath("Report and PPT")
os.makedirs(output_dir, exist_ok=True)
pptx_path = os.path.join(output_dir, "VitalSphere_Presentation.pptx")

prs = pptx.Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color Palette
COLOR_NAVY_950 = RGBColor(10, 17, 32)
COLOR_NAVY_900 = RGBColor(15, 23, 42)
COLOR_RED_600 = RGBColor(220, 38, 38)
COLOR_SLATE_400 = RGBColor(148, 163, 184)
COLOR_SLATE_500 = RGBColor(100, 116, 139)
COLOR_SLATE_700 = RGBColor(51, 65, 85)
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_EMERALD_600 = RGBColor(5, 150, 105)
COLOR_CARD_BG = RGBColor(24, 34, 53)

srm_logo_path = r"C:\Users\PAUL\Documents\Projects\Nexus-Arena\srm_logo.png"

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

blank_slide_layout = prs.slide_layouts[6]

def set_slide_background(slide, color):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    return bg

def add_header(slide, title, category="VITALSPHERE HEALTHCARE & BLOOD LOGISTICS PLATFORM"):
    # Header strip
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(10), Inches(0.3))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    p_c.text = category.upper()
    p_c.font.size = Pt(10)
    p_c.font.bold = True
    p_c.font.color.rgb = COLOR_RED_600

    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(10), Inches(0.7))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_WHITE

    # SRM Logo top-right
    if os.path.exists(srm_logo_path):
        s_stream = get_clean_image_stream(srm_logo_path)
        if s_stream:
            slide.shapes.add_picture(s_stream, Inches(11.8), Inches(0.4), width=Inches(0.85))

# ------------------------------------------------------------------------------
# SLIDE 1: TITLE SLIDE
# ------------------------------------------------------------------------------
s1 = prs.slides.add_slide(blank_slide_layout)
set_slide_background(s1, COLOR_NAVY_950)

# SRM AP Logo center-top
if os.path.exists(srm_logo_path):
    s_stream = get_clean_image_stream(srm_logo_path)
    if s_stream:
        s1.shapes.add_picture(s_stream, Inches(6.05), Inches(0.7), width=Inches(1.25))

t1_box = s1.shapes.add_textbox(Inches(1.0), Inches(2.1), Inches(11.333), Inches(2.0))
tf1 = t1_box.text_frame
tf1.word_wrap = True
p1_sub = tf1.paragraphs[0]
p1_sub.text = "CSE 213 — ADVANCED JAVA PROGRAMMING • III SEMESTER B.TECH CSE AI ML F"
p1_sub.alignment = PP_ALIGN.CENTER
p1_sub.font.size = Pt(11)
p1_sub.font.bold = True
p1_sub.font.color.rgb = COLOR_RED_600

p1_title = tf1.add_paragraph()
p1_title.text = "VITALSPHERE"
p1_title.alignment = PP_ALIGN.CENTER
p1_title.font.size = Pt(36)
p1_title.font.bold = True
p1_title.font.color.rgb = COLOR_WHITE

p1_desc = tf1.add_paragraph()
p1_desc.text = "National Healthcare & Cloud-Synchronized Blood Logistics Coordination Platform"
p1_desc.alignment = PP_ALIGN.CENTER
p1_desc.font.size = Pt(16)
p1_desc.font.color.rgb = COLOR_SLATE_400

# Meta table at bottom
meta_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(4.5), Inches(10.333), Inches(2.2))
meta_card.fill.solid()
meta_card.fill.fore_color.rgb = COLOR_CARD_BG
meta_card.line.color.rgb = COLOR_RED_600

mtf = meta_card.text_frame
mtf.word_wrap = True
p_team = mtf.paragraphs[0]
p_team.text = "PROJECT TEAM MEMBERS (SRM UNIVERSITY – AP):"
p_team.font.bold = True
p_team.font.size = Pt(12)
p_team.font.color.rgb = COLOR_RED_600

p_members = mtf.add_paragraph()
p_members.text = "• P. Abhishek Paul (AP25110071316) — Team Lead & Cloud Architect\n• K. Nithien (AP25110070134) — Desktop Client & Swing UI Developer\n• Shaik Hasnain (AP25110070228) — Backend Logic & Verification Lead"
p_members.font.size = Pt(11.5)
p_members.font.color.rgb = COLOR_WHITE

p_fac = mtf.add_paragraph()
p_fac.text = "FACULTY GUIDE: Dr. Srikanth Lukka, Assistant Professor, Department of CSE"
p_fac.font.bold = True
p_fac.font.size = Pt(11.5)
p_fac.font.color.rgb = RGBColor(56, 189, 248)

# ------------------------------------------------------------------------------
# SLIDE 2: PROBLEM STATEMENT & MOTIVATION
# ------------------------------------------------------------------------------
s2 = prs.slides.add_slide(blank_slide_layout)
set_slide_background(s2, COLOR_NAVY_950)
add_header(s2, "The Critical Problem: Life-Threatening Blood Coordination Delays")

cards_data_s2 = [
    ("Fragmented Stock Silos", "Blood banks maintain disconnected, manual records. Patients spend hours calling hospitals blindly during emergency trauma surgeries, wasting vital minutes.", COLOR_RED_600),
    ("Unverified Donor Lists", "Informal social media lists register citizen volunteers without medical clearance. Over 35% are rejected on-site due to low Hb (<12.5) or inadequate cooldown rest (<90 days).", COLOR_RED_600),
    ("Requisition Proof Deficit", "Emergency blood calls often lack authentic hospital proof. This leads to chaotic rumors and panic without physician-verified transfusion requisition slips.", COLOR_RED_600),
    ("High-Latency Coordination", "Finding a donor is only half the battle. Coordination fails due to broken forms, outdated phone numbers, login blockers, and lack of real-time attendant alerts.", COLOR_RED_600)
]

for idx, (title, desc, col) in enumerate(cards_data_s2):
    x = Inches(0.8 + (idx * 2.95))
    card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.8), Inches(2.8), Inches(4.8))
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_CARD_BG
    card.line.color.rgb = col
    
    tf = card.text_frame
    tf.word_wrap = True
    p_num = tf.paragraphs[0]
    p_num.text = f"0{idx+1}"
    p_num.font.bold = True
    p_num.font.size = Pt(28)
    p_num.font.color.rgb = col
    
    p_t = tf.add_paragraph()
    p_t.text = title
    p_t.font.bold = True
    p_t.font.size = Pt(14)
    p_t.font.color.rgb = COLOR_WHITE
    
    p_d = tf.add_paragraph()
    p_d.text = desc
    p_d.font.size = Pt(11)
    p_d.font.color.rgb = COLOR_SLATE_400

# ------------------------------------------------------------------------------
# SLIDE 3: THE VITALSPHERE SOLUTION
# ------------------------------------------------------------------------------
s3 = prs.slides.add_slide(blank_slide_layout)
set_slide_background(s3, COLOR_NAVY_950)
add_header(s3, "The VitalSphere Solution: Dual-Platform Coordination Network")

s3_features = [
    ("Native Java Desktop Client", "Engineered in Java 21 Swing/AWT. Full Medical Officer Clearance Console, Keychain login, and direct OS-level Desktop file inspection for statutory certificates."),
    ("Cloud-Edge Web Portal", "Dual PC and mobile experience with real-time stock matrix, zero-stale cache-control headers, and floating pill navigation. 100% accessible anywhere without installation."),
    ("Statutory Pre-Screening", "Enforces National Blood Transfusion Council (NBTC) clinical standards: Hb >= 12.5 g/dL and Rest >= 90 days. Every voluntary donor is certified by a Medical Officer."),
    ("Instant Attendant Dispatch", "1-Click 'Donate' action triggers immediate real-time tele-notification to the patient's family, hospital desk, and live Notification Center without login barriers.")
]

for idx, (ftitle, fdesc) in enumerate(s3_features):
    y = Inches(1.8 + (idx * 1.25))
    row_card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.733), Inches(1.1))
    row_card.fill.solid()
    row_card.fill.fore_color.rgb = COLOR_CARD_BG
    row_card.line.color.rgb = COLOR_SLATE_700
    
    rtf = row_card.text_frame
    rtf.word_wrap = True
    rp1 = rtf.paragraphs[0]
    rp1.text = ftitle.upper()
    rp1.font.bold = True
    rp1.font.size = Pt(12)
    rp1.font.color.rgb = COLOR_RED_600
    
    rp2 = rtf.add_paragraph()
    rp2.text = fdesc
    rp2.font.size = Pt(10.5)
    rp2.font.color.rgb = COLOR_WHITE

# ------------------------------------------------------------------------------
# SLIDE 4: SYSTEM ARCHITECTURE & DATA FLOW
# ------------------------------------------------------------------------------
s4 = prs.slides.add_slide(blank_slide_layout)
set_slide_background(s4, COLOR_NAVY_950)
add_header(s4, "System Architecture: Distributed, Resilient Multi-Client Topology")

arch_boxes = [
    ("NATIVE DESKTOP CLIENT\n(Java 21 / Swing / AWT)", "• Standalone executable JAR\n• Event Dispatch Thread (EDT)\n• Anti-aliased 2D rendering\n• Local resilient fallback cache\n• OS Desktop API file viewer", Inches(0.8)),
    ("CLOUD BACKEND & EDGE CDN\n(Google Firebase / REST)", "• Global edge CDN distribution\n• REST version validator\n• No-cache revalidation headers\n• Static asset delivery engine\n• Zero-latency JSON payloads", Inches(4.8)),
    ("RESPONSIVE WEB PORTAL\n(Desktop & Mobile Clients)", "• Responsive dual HTML5/CSS\n• Self-contained fallback generators\n• Pan-India State/District logic\n• Real-time Notification Center\n• Floating pill mobile dock", Inches(8.8))
]

for btitle, bdesc, bx in arch_boxes:
    bshape = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, Inches(1.8), Inches(3.7), Inches(4.8))
    bshape.fill.solid()
    bshape.fill.fore_color.rgb = COLOR_CARD_BG
    bshape.line.color.rgb = RGBColor(56, 189, 248)
    
    btf = bshape.text_frame
    btf.word_wrap = True
    bp1 = btf.paragraphs[0]
    bp1.text = btitle
    bp1.font.bold = True
    bp1.font.size = Pt(13)
    bp1.font.color.rgb = RGBColor(56, 189, 248)
    
    bp2 = btf.add_paragraph()
    bp2.text = bdesc
    bp2.font.size = Pt(11)
    bp2.font.color.rgb = COLOR_WHITE

# ------------------------------------------------------------------------------
# SLIDE 5: CORE JAVA CONCEPTS IMPLEMENTED (OOP)
# ------------------------------------------------------------------------------
s5 = prs.slides.add_slide(blank_slide_layout)
set_slide_background(s5, COLOR_NAVY_950)
add_header(s5, "Core Java Programming Concepts (Mapping to CSE 213 Curriculum)")

oop_concepts = [
    ("Inheritance", "VitalSphereDesktopClient extends javax.swing.JFrame, orchestrating child panels, custom layout managers, and modal JDialogs in an OOP hierarchy.", "JFrame & JDialog Containment"),
    ("Encapsulation", "Clinical vitals (Hb levels, rest days, certificate paths) are encapsulated within private data structures and managed through DefaultTableModel interfaces.", "Private State & Table Models"),
    ("Polymorphism", "Buttons and action listeners implement dynamic behavior through overloaded factories (createStyledButton), computing hover, pressed, and focus paint styles dynamically.", "Factory Methods & State Tints"),
    ("Abstraction", "Complex OS document interactions are abstracted behind unified openDocumentFileOrDisplay() calls, decoupling platform specifics from GUI controllers.", "Unified System File Bridges")
]

for idx, (title, desc, tag) in enumerate(oop_concepts):
    col = idx % 2
    row = idx // 2
    x = Inches(0.8 + (col * 5.95))
    y = Inches(1.8 + (row * 2.5))
    
    box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.7), Inches(2.2))
    box.fill.solid()
    box.fill.fore_color.rgb = COLOR_CARD_BG
    box.line.color.rgb = COLOR_RED_600
    
    btf = box.text_frame
    btf.word_wrap = True
    bp1 = btf.paragraphs[0]
    bp1.text = f"{title.upper()} — {tag}"
    bp1.font.bold = True
    bp1.font.size = Pt(12)
    bp1.font.color.rgb = COLOR_RED_600
    
    bp2 = btf.add_paragraph()
    bp2.text = desc
    bp2.font.size = Pt(10.5)
    bp2.font.color.rgb = COLOR_WHITE

# ------------------------------------------------------------------------------
# SLIDE 6: MULTITHREADING, CONCURRENCY & GRAPHICS 2D
# ------------------------------------------------------------------------------
s6 = prs.slides.add_slide(blank_slide_layout)
set_slide_background(s6, COLOR_NAVY_950)
add_header(s6, "Multithreading, Concurrency & Custom Java 2D Graphics")

concurrency_items = [
    ("Event Dispatch Thread (EDT) Safety", "All UI rendering, table updates, and dialog transitions strictly adhere to Swing's single-threaded EDT pipeline. Long-running version checks and remote polling execute on background threads via SwingUtilities.invokeLater(), preventing UI freezes."),
    ("Custom Anti-Aliased Graphics2D Engine", "Eliminates white-on-white text bugs and jagged edges by overriding paintComponent(). Activates RenderingHints.KEY_ANTIALIASING, calculates mathematically blended color shades on mouse hover, and renders smooth rounded rectangles."),
    ("Resilient Fallback Memory Cache", "Thread-safe local registries (Map<String, String>) store file paths, 256 pre-cleared donors, and 64 emergency recipients. The client maintains complete operational functionality even when offline."),
    ("Desktop API OS-Bridge Integration", "Integrates java.awt.Desktop to trigger native operating system handlers, allowing Medical Officers to open and inspect authentic PDF and image certificates in their preferred local document viewer.")
]

for idx, (ctitle, cdesc) in enumerate(concurrency_items):
    y = Inches(1.8 + (idx * 1.25))
    cbox = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.733), Inches(1.1))
    cbox.fill.solid()
    cbox.fill.fore_color.rgb = COLOR_CARD_BG
    cbox.line.color.rgb = RGBColor(56, 189, 248)
    
    ctf = cbox.text_frame
    ctf.word_wrap = True
    cp1 = ctf.paragraphs[0]
    cp1.text = ctitle.upper()
    cp1.font.bold = True
    cp1.font.size = Pt(12)
    cp1.font.color.rgb = RGBColor(56, 189, 248)
    
    cp2 = ctf.add_paragraph()
    cp2.text = cdesc
    cp2.font.size = Pt(10.5)
    cp2.font.color.rgb = COLOR_WHITE

# ------------------------------------------------------------------------------
# SLIDE 7: DATA FETCHING, POLLING & CACHING
# ------------------------------------------------------------------------------
s7 = prs.slides.add_slide(blank_slide_layout)
set_slide_background(s7, COLOR_NAVY_950)
add_header(s7, "Data Ingestion, Dynamic Matrices & Zero-Stale Caching")

s7_columns = [
    ("Pan-India Geographic Matrix", "• Structured state-to-district dictionaries covering all 28 states and territories.\n• Dynamic cascading dropdowns (donorState -> donorCity).\n• Real-time validation without hardcoded Andhra Pradesh restrictions.", Inches(0.8)),
    ("Zero-Stale Cloud Invalidation", "• Firebase Hosting Cache-Control:\n  max-age=0, no-cache, no-store, must-revalidate.\n• Script fingerprint query versions.\n• Eradicates Android/iOS stale caching bugs.", Inches(4.8)),
    ("Resilient Fallback Generators", "• Self-contained synchronous generator initializes 256 donors and 64 recipients inline.\n• Immune to network dropouts or CDN lag.\n• Instant filtering across all 8 blood groups.", Inches(8.8))
]

for h_t, h_d, h_x in s7_columns:
    col_card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, h_x, Inches(1.8), Inches(3.7), Inches(4.8))
    col_card.fill.solid()
    col_card.fill.fore_color.rgb = COLOR_CARD_BG
    col_card.line.color.rgb = COLOR_RED_600
    
    ctf = col_card.text_frame
    ctf.word_wrap = True
    cp1 = ctf.paragraphs[0]
    cp1.text = h_t.upper()
    cp1.font.bold = True
    cp1.font.size = Pt(13)
    cp1.font.color.rgb = COLOR_RED_600
    
    cp2 = ctf.add_paragraph()
    cp2.text = h_d
    cp2.font.size = Pt(11)
    cp2.font.color.rgb = COLOR_WHITE

# ------------------------------------------------------------------------------
# SLIDE 8: MEDICAL OFFICER CLEARANCE CONSOLE
# ------------------------------------------------------------------------------
s8 = prs.slides.add_slide(blank_slide_layout)
set_slide_background(s8, COLOR_NAVY_950)
add_header(s8, "Medical Officer Clearance Console: Statutory Clinical Verification")

clearance_steps = [
    ("1. Candidate Vitals Inspection", "Review applicant's Full Name, Aadhaar identifier, blood group, and contact information."),
    ("2. Statutory Criteria Validation", "Checks Hemoglobin level (statutory minimum of 12.5 g/dL) and rest period (minimum 90 days required between donations)."),
    ("3. Document Preview & Audit", "Inspects uploaded Doctor-signed Fitness Certificates and official Laboratory Blood Group Cards directly."),
    ("4. Statutory Decision (Approve/Defer)", "Approve: Candidate enters active donor pool. Defer: Temporarily placed on 90-day cooldown rest.")
]

for idx, (stitle, sdesc) in enumerate(clearance_steps):
    x = Inches(0.8 + (idx * 2.95))
    step_card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.8), Inches(2.8), Inches(4.8))
    step_card.fill.solid()
    step_card.fill.fore_color.rgb = COLOR_CARD_BG
    step_card.line.color.rgb = COLOR_EMERALD_600
    
    stf = step_card.text_frame
    stf.word_wrap = True
    sp1 = stf.paragraphs[0]
    sp1.text = stitle
    sp1.font.bold = True
    sp1.font.size = Pt(13)
    sp1.font.color.rgb = COLOR_EMERALD_600
    
    sp2 = stf.add_paragraph()
    sp2.text = sdesc
    sp2.font.size = Pt(11)
    sp2.font.color.rgb = COLOR_WHITE

# ------------------------------------------------------------------------------
# SLIDE 9: SCREENSHOTS: DESKTOP JAVA CLIENT
# ------------------------------------------------------------------------------
s9 = prs.slides.add_slide(blank_slide_layout)
set_slide_background(s9, COLOR_NAVY_950)
add_header(s9, "Live Showcase: Native Desktop Java Client Application")

desktop_img_1 = r"C:/Users/PAUL/.gemini/antigravity/brain/22b50d08-d1d4-476a-b4c6-9e333fb80fb1/.user_uploaded/media_1795518007351_d7c52834.jpg"
desktop_img_2 = r"C:/Users/PAUL/.gemini/antigravity/brain/22b50d08-d1d4-476a-b4c6-9e333fb80fb1/.user_uploaded/media_1795516901049_b558a926.jpg"

if os.path.exists(desktop_img_1):
    stream1 = get_clean_image_stream(desktop_img_1)
    if stream1:
        s9.shapes.add_picture(stream1, Inches(0.8), Inches(1.8), width=Inches(5.6))
        c1 = s9.shapes.add_textbox(Inches(0.8), Inches(5.8), Inches(5.6), Inches(0.6))
        c1.text_frame.paragraphs[0].text = "Swing Main Console: Live Donor Table & Action Controls"
        c1.text_frame.paragraphs[0].font.size = Pt(11)
        c1.text_frame.paragraphs[0].font.color.rgb = COLOR_SLATE_400

if os.path.exists(desktop_img_2):
    stream2 = get_clean_image_stream(desktop_img_2)
    if stream2:
        s9.shapes.add_picture(stream2, Inches(6.8), Inches(1.8), width=Inches(5.7))
        c2 = s9.shapes.add_textbox(Inches(6.8), Inches(6.0), Inches(5.7), Inches(0.6))
        c2.text_frame.paragraphs[0].text = "Certificate Preview Dialog: Statutory Form-04 & Local File Launcher"
        c2.text_frame.paragraphs[0].font.size = Pt(11)
        c2.text_frame.paragraphs[0].font.color.rgb = COLOR_SLATE_400

# ------------------------------------------------------------------------------
# SLIDE 10: SCREENSHOTS: DESKTOP & MOBILE WEB PORTAL
# ------------------------------------------------------------------------------
s10 = prs.slides.add_slide(blank_slide_layout)
set_slide_background(s10, COLOR_NAVY_950)
add_header(s10, "Live Showcase: Responsive Desktop & Mobile Web Portals")

web_img_1 = r"C:/Users/PAUL/.gemini/antigravity/brain/22b50d08-d1d4-476a-b4c6-9e333fb80fb1/.user_uploaded/media_1795522689897_4629b506.png"
web_img_2 = r"C:/Users/PAUL/.gemini/antigravity/brain/22b50d08-d1d4-476a-b4c6-9e333fb80fb1/.user_uploaded/media_1795522830460_3c148eb7.jpg"

if os.path.exists(web_img_1):
    stream_w1 = get_clean_image_stream(web_img_1)
    if stream_w1:
        s10.shapes.add_picture(stream_w1, Inches(0.8), Inches(1.8), width=Inches(6.0))
        cw1 = s10.shapes.add_textbox(Inches(0.8), Inches(6.4), Inches(6.0), Inches(0.5))
        cw1.text_frame.paragraphs[0].text = "Desktop Registration: Dynamic Pan-India State & District Selectors"
        cw1.text_frame.paragraphs[0].font.size = Pt(11)
        cw1.text_frame.paragraphs[0].font.color.rgb = COLOR_SLATE_400

if os.path.exists(web_img_2):
    stream_w2 = get_clean_image_stream(web_img_2)
    if stream_w2:
        s10.shapes.add_picture(stream_w2, Inches(7.5), Inches(1.8), width=Inches(5.0))
        cw2 = s10.shapes.add_textbox(Inches(7.5), Inches(6.4), Inches(5.0), Inches(0.5))
        cw2.text_frame.paragraphs[0].text = "Mobile Portal: Live Stock Grid & Modern Floating Pill Bottom Bar"
        cw2.text_frame.paragraphs[0].font.size = Pt(11)
        cw2.text_frame.paragraphs[0].font.color.rgb = COLOR_SLATE_400

# ------------------------------------------------------------------------------
# SLIDE 11: EMERGENCY TRANSFUSION & ATTENDANT DISPATCH
# ------------------------------------------------------------------------------
s11 = prs.slides.add_slide(blank_slide_layout)
set_slide_background(s11, COLOR_NAVY_950)
add_header(s11, "Emergency Transfusion Requisition & 1-Click Donor Dispatch")

workflow_cards = [
    ("Hospital Transfusion Order", "Attendant submits patient Aadhaar, blood group, units needed, and uploads Doctor's Requisition Certificate (.pdf / .png / .jpg)."),
    ("Instant Network Broadcast", "Requirement is injected into live registries and broadcasts alerts across Desktop & Mobile Notification Centers with click-to-preview routing."),
    ("1-Click Donor Commitment", "Any citizen donor can click 'Donate' on the patient card. The system marks status as '✓ DONOR FOUND' and verifies donor credentials."),
    ("Real-Time Attendant Alert", "Dispatches immediate confirmation to the attendant's phone and hospital desk, establishing direct line communication to save a life.")
]

for idx, (wtitle, wdesc) in enumerate(workflow_cards):
    y = Inches(1.8 + (idx * 1.25))
    wcard = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.733), Inches(1.1))
    wcard.fill.solid()
    wcard.fill.fore_color.rgb = COLOR_CARD_BG
    wcard.line.color.rgb = COLOR_RED_600
    
    wtf = wcard.text_frame
    wtf.word_wrap = True
    wp1 = wtf.paragraphs[0]
    wp1.text = f"STEP {idx+1}: {wtitle.upper()}"
    wp1.font.bold = True
    wp1.font.size = Pt(12)
    wp1.font.color.rgb = COLOR_RED_600
    
    wp2 = wtf.add_paragraph()
    wp2.text = wdesc
    wp2.font.size = Pt(10.5)
    wp2.font.color.rgb = COLOR_WHITE

# ------------------------------------------------------------------------------
# SLIDE 12: TEAM MEMBERS & ROLES
# ------------------------------------------------------------------------------
s12 = prs.slides.add_slide(blank_slide_layout)
set_slide_background(s12, COLOR_NAVY_950)
add_header(s12, "Team Contributions & Engineering Responsibilities")

team_cards = [
    ("P. Abhishek Paul", "AP25110071316", "Lead Architect & Cloud Systems",
     "• Engineered the dual-platform system topology and Firebase edge deployment.\n• Solved mobile browser caching via multi-tier Cache-Control headers.\n• Implemented unblocked Donate tele-dispatch and real-time Notification Center.\n• Designed pan-India dynamic state/district lookup matrices."),
    ("K. Nithien", "AP25110070134", "Desktop Client & Swing UI Developer",
     "• Engineered the standalone Java 21 Swing/AWT desktop application.\n• Built custom anti-aliased Graphics2D button renderer preventing color bugs.\n• Developed CampFlow Keychain 1-click credential selector and sign-in toggle.\n• Integrated Desktop API for opening authentic local certificate files."),
    ("Shaik Hasnain", "AP25110070228", "Data Logic & Verification Lead",
     "• Implemented statutory NBTC Medical Officer clearance console.\n• Built clinical parameters verification (Hb >= 12.5 g/dL, Rest >= 90 days).\n• Developed Doctor Transfusion Requisition Certificate upload pipeline.\n• Conducted unit testing, thread safety verification, and fat-JAR packaging.")
]

for idx, (mname, mroll, mrole, mresp) in enumerate(team_cards):
    x = Inches(0.8 + (idx * 3.95))
    tcard = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.8), Inches(3.75), Inches(4.8))
    tcard.fill.solid()
    tcard.fill.fore_color.rgb = COLOR_CARD_BG
    tcard.line.color.rgb = RGBColor(56, 189, 248)
    
    ttf = tcard.text_frame
    ttf.word_wrap = True
    tp1 = ttf.paragraphs[0]
    tp1.text = mname
    tp1.font.bold = True
    tp1.font.size = Pt(14)
    tp1.font.color.rgb = COLOR_WHITE
    
    tp2 = ttf.add_paragraph()
    tp2.text = f"{mroll}\n{mrole}"
    tp2.font.bold = True
    tp2.font.size = Pt(10.5)
    tp2.font.color.rgb = RGBColor(56, 189, 248)
    
    tp3 = ttf.add_paragraph()
    tp3.text = f"\n{mresp}"
    tp3.font.size = Pt(10)
    tp3.font.color.rgb = COLOR_SLATE_400

# ------------------------------------------------------------------------------
# SLIDE 13: CONCLUSION & FUTURE ROADMAP
# ------------------------------------------------------------------------------
s13 = prs.slides.add_slide(blank_slide_layout)
set_slide_background(s13, COLOR_NAVY_950)
add_header(s13, "Conclusion & Future Roadmap")

s13_items = [
    ("Academic Excellence in Java 21", "Successfully implemented all CSE 213 advanced Java concepts: OOP inheritance, thread-safe memory models, custom 2D vector painting, and Event Dispatch Thread isolation."),
    ("Measurable Clinical Impact", "Replaces chaotic WhatsApp calls and paper slips with deterministic, certified, real-time blood logistics across hospital surgical units and voluntary citizen donors."),
    ("Zero-Emoji Clean Vector Standard", "Adheres to rigorous enterprise software standards: replaced all emojis with clean Unicode symbols (✓, ✕, •, →) and crisp scalable vector SVGs across Web and Java GUI."),
    ("Future Strategic Roadmap", "Planned integration with Government of India e-RaktKosh API, automated SMS/WhatsApp OTP dispatch gateway, and autonomous drone delivery routing for rare Rh-negative blood.")
]

for idx, (stitle, sdesc) in enumerate(s13_items):
    y = Inches(1.8 + (idx * 1.25))
    scard = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.733), Inches(1.1))
    scard.fill.solid()
    scard.fill.fore_color.rgb = COLOR_CARD_BG
    scard.line.color.rgb = COLOR_EMERALD_600
    
    stf = scard.text_frame
    stf.word_wrap = True
    sp1 = stf.paragraphs[0]
    sp1.text = stitle.upper()
    sp1.font.bold = True
    sp1.font.size = Pt(12)
    sp1.font.color.rgb = COLOR_EMERALD_600
    
    sp2 = stf.add_paragraph()
    sp2.text = sdesc
    sp2.font.size = Pt(10.5)
    sp2.font.color.rgb = COLOR_WHITE

# ------------------------------------------------------------------------------
# SLIDE 14: Q&A / VIVA VOCE
# ------------------------------------------------------------------------------
s14 = prs.slides.add_slide(blank_slide_layout)
set_slide_background(s14, COLOR_NAVY_950)

if os.path.exists(srm_logo_path):
    stream_end = get_clean_image_stream(srm_logo_path)
    if stream_end:
        s14.shapes.add_picture(stream_end, Inches(6.05), Inches(1.2), width=Inches(1.25))

q_box = s14.shapes.add_textbox(Inches(1.0), Inches(2.8), Inches(11.333), Inches(3.0))
qtf = q_box.text_frame
qtf.word_wrap = True

qp1 = qtf.paragraphs[0]
qp1.text = "THANK YOU!"
qp1.alignment = PP_ALIGN.CENTER
qp1.font.size = Pt(38)
qp1.font.bold = True
qp1.font.color.rgb = COLOR_RED_600

qp2 = qtf.add_paragraph()
qp2.text = "VitalSphere — National Healthcare & Cloud-Synchronized Blood Logistics Platform"
qp2.alignment = PP_ALIGN.CENTER
qp2.font.size = Pt(16)
qp2.font.color.rgb = COLOR_WHITE

qp3 = qtf.add_paragraph()
qp3.text = "\nQuestions & Technical Discussion (Viva Voce)"
qp3.alignment = PP_ALIGN.CENTER
qp3.font.size = Pt(14)
qp3.font.bold = True
qp3.font.color.rgb = RGBColor(56, 189, 248)

qp4 = qtf.add_paragraph()
qp4.text = "Department of Computer Science and Engineering • SRM University – AP"
qp4.alignment = PP_ALIGN.CENTER
qp4.font.size = Pt(11)
qp4.font.color.rgb = COLOR_SLATE_400

prs.save(pptx_path)
print(f"Presentation successfully generated at: {pptx_path}")
