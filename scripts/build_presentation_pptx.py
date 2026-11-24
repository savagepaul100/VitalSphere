import os
import io
from PIL import Image
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

print("Building VitalSphere White & Red Angular Presentation (.pptx)...")

output_dir = os.path.abspath("Report and PPT")
os.makedirs(output_dir, exist_ok=True)
pptx_path = os.path.join(output_dir, "VitalSphere_Presentation.pptx")

prs = pptx.Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# STRICT WHITE & RED THEME PALETTE
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_BG_LIGHT = RGBColor(248, 250, 252) # Crisp subtle slate-50
COLOR_RED_PRIMARY = RGBColor(220, 38, 38) # Crimson Red #DC2626
COLOR_RED_DARK = RGBColor(185, 28, 28) # Deep Red #B91C1C
COLOR_RED_LIGHT = RGBColor(254, 242, 242) # Red 50 tint
COLOR_NAVY_DARK = RGBColor(10, 17, 32) # Deep Slate #0A1120
COLOR_TEXT_MAIN = RGBColor(15, 23, 42) # Slate 900
COLOR_TEXT_MUTED = RGBColor(71, 85, 105) # Slate 600
COLOR_BORDER = RGBColor(226, 232, 240) # Slate 200 border
COLOR_EMERALD = RGBColor(5, 150, 105)

srm_logo_path = r"target\srm_logo.png"

def get_clean_image_stream(path):
    try:
        im = Image.open(path)
        buf = io.BytesIO()
        im.save(buf, format='PNG')
        buf.seek(0)
        return buf
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return None

blank_layout = prs.slide_layouts[6]

def set_slide_background(slide):
    # Pure White background with top red accent line
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLOR_WHITE
    bg.line.fill.background()

    # Red top accent strip (Angular, 0 radius)
    strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    strip.fill.solid()
    strip.fill.fore_color.rgb = COLOR_RED_PRIMARY
    strip.line.fill.background()
    return bg

def add_slide_header(slide, title, category="CSE 213 • ADVANCED JAVA PROGRAMMING"):
    # Category tag
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(9.5), Inches(0.28))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    p_c.text = category.upper()
    p_c.font.size = Pt(9.5)
    p_c.font.bold = True
    p_c.font.color.rgb = COLOR_RED_PRIMARY

    # Main Slide Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.62), Inches(9.5), Inches(0.65))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title
    p_t.font.size = Pt(21)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_NAVY_DARK

    # Subtle horizontal dividing rule
    rule = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.3), Inches(11.733), Inches(0.02))
    rule.fill.solid()
    rule.fill.fore_color.rgb = COLOR_BORDER
    rule.line.fill.background()

    # SRM Logo top right
    if os.path.exists(srm_logo_path):
        stream = get_clean_image_stream(srm_logo_path)
        if stream:
            slide.shapes.add_picture(stream, Inches(11.8), Inches(0.35), width=Inches(0.75))

def create_angular_card(slide, left, top, width, height, bg_color=COLOR_WHITE, border_color=COLOR_BORDER):
    # Strictly RECTANGLE with 0 corner radius (NO ROUNDED CORNERS)
    card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
    else:
        card.line.fill.background()
    return card

# ==============================================================================
# SLIDE 1: TITLE SLIDE (WHITE & RED ANGULAR THEME)
# ==============================================================================
s1 = prs.slides.add_slide(blank_layout)
set_slide_background(s1)

# Left Red Accent Banner (Angular Rectangle)
left_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.4), Inches(7.5))
left_bar.fill.solid()
left_bar.fill.fore_color.rgb = COLOR_RED_PRIMARY
left_bar.line.fill.background()

# SRM AP Logo Center-Top
if os.path.exists(srm_logo_path):
    stream = get_clean_image_stream(srm_logo_path)
    if stream:
        s1.shapes.add_picture(stream, Inches(1.0), Inches(0.8), width=Inches(1.2))

# Sub-header badge
b_badge = create_angular_card(s1, Inches(2.4), Inches(0.85), Inches(5.8), Inches(0.38), bg_color=COLOR_RED_LIGHT, border_color=COLOR_RED_PRIMARY)
b_tf = b_badge.text_frame
b_tf.margin_left = Inches(0.15)
b_p = b_tf.paragraphs[0]
b_p.text = "SRM UNIVERSITY – AP • DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING"
b_p.font.size = Pt(8.5)
b_p.font.bold = True
b_p.font.color.rgb = COLOR_RED_PRIMARY

# Main Project Title
t_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(11.5), Inches(1.5))
tf = t_box.text_frame
p0 = tf.paragraphs[0]
p0.text = "VitalSphere"
p0.font.size = Pt(44)
p0.font.bold = True
p0.font.color.rgb = COLOR_RED_PRIMARY

p1 = tf.add_paragraph()
p1.text = "National Healthcare & Cloud-Synchronized Blood Logistics Platform"
p1.font.size = Pt(20)
p1.font.bold = True
p1.font.color.rgb = COLOR_NAVY_DARK

p2 = tf.add_paragraph()
p2.text = "CSE 213: Advanced Java Programming • B.Tech III Semester (CSE AI ML F) • Academic Year: 2026 – 2027"
p2.font.size = Pt(11)
p2.font.color.rgb = COLOR_TEXT_MUTED

# Angular Team Card (Left)
create_angular_card(s1, Inches(1.0), Inches(3.6), Inches(5.6), Inches(3.2), bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER)
# Accent top bar for card
top_strip_left = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(3.6), Inches(5.6), Inches(0.08))
top_strip_left.fill.solid()
top_strip_left.fill.fore_color.rgb = COLOR_RED_PRIMARY
top_strip_left.line.fill.background()

box_team = s1.shapes.add_textbox(Inches(1.2), Inches(3.8), Inches(5.2), Inches(2.8))
tf_tm = box_team.text_frame
p = tf_tm.paragraphs[0]
p.text = "PROJECT AUTHORS & RESPONSIBILITIES"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = COLOR_RED_PRIMARY

members = [
    ("1. P. Abhishek Paul (AP25110071316)", "Lead Architect, Cloud Synchronization & Data Models"),
    ("2. K. Nithien (AP25110070134)", "Desktop Client Engineering & Custom Swing GUI"),
    ("3. Shaik Hasnain (AP25110070228)", "Backend Concurrency & Clinical Verification Pipeline")
]
for m_title, m_role in members:
    pm = tf_tm.add_paragraph()
    pm.text = m_title
    pm.font.size = Pt(10.5)
    pm.font.bold = True
    pm.font.color.rgb = COLOR_NAVY_DARK
    pr = tf_tm.add_paragraph()
    pr.text = "    " + m_role
    pr.font.size = Pt(9)
    pr.font.color.rgb = COLOR_TEXT_MUTED

# Angular Faculty Card (Right)
create_angular_card(s1, Inches(7.0), Inches(3.6), Inches(5.3), Inches(3.2), bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER)
top_strip_right = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.0), Inches(3.6), Inches(5.3), Inches(0.08))
top_strip_right.fill.solid()
top_strip_right.fill.fore_color.rgb = COLOR_NAVY_DARK
top_strip_right.line.fill.background()

box_fac = s1.shapes.add_textbox(Inches(7.2), Inches(3.8), Inches(4.9), Inches(2.8))
tf_fac = box_fac.text_frame
pf = tf_fac.paragraphs[0]
pf.text = "FACULTY SUPERVISION & INSTITUTION"
pf.font.size = Pt(11)
pf.font.bold = True
pf.font.color.rgb = COLOR_NAVY_DARK

fac_details = [
    ("Faculty Guide:", "Dr. Srikanth Lukka"),
    ("Designation:", "Assistant Professor"),
    ("Department:", "Department of Computer Science & Engineering"),
    ("School:", "School of Engineering and Sciences"),
    ("University:", "SRM UNIVERSITY – AP, ANDHRA PRADESH"),
    ("Campus:", "Neerukonda, Mangalagiri Mandal, Guntur – 522 240")
]
for k, v in fac_details:
    pkv = tf_fac.add_paragraph()
    pkv.text = f"{k} {v}"
    pkv.font.size = Pt(9.5)
    if k in ["Faculty Guide:", "University:"]:
        pkv.font.bold = True
        pkv.font.color.rgb = COLOR_NAVY_DARK
    else:
        pkv.font.color.rgb = COLOR_TEXT_MUTED

# ==============================================================================
# SLIDE 2: EXECUTIVE OVERVIEW & PROBLEM STATEMENT
# ==============================================================================
s2 = prs.slides.add_slide(blank_layout)
set_slide_background(s2)
add_slide_header(s2, "Executive Overview: The Blood Supply Deficit in India", "PROBLEM STATEMENT & CLINICAL MOTIVATION")

# 3 Metric Cards Across Top (Angular)
metrics = [
    ("1.2M+ Units", "Annual National Blood Shortage", "India suffers from an acute deficit of voluntary units, severely impacting emergency trauma care.", COLOR_RED_PRIMARY),
    ("60 Minutes", "The 'Golden Hour' Window", "Trauma and obstetric cases require immediate component transfusion before irreversible hemorrhagic shock.", COLOR_NAVY_DARK),
    ("Zero Visibility", "Fragmented Logistics Silos", "Blood banks track inventories on local spreadsheets with zero real-time inter-hospital synchronization.", COLOR_RED_DARK)
]

for i, (val, title, desc, color) in enumerate(metrics):
    card = create_angular_card(s2, Inches(0.8 + i * 4.0), Inches(1.6), Inches(3.7), Inches(2.2), bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER)
    # colored top bar
    bar = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8 + i * 4.0), Inches(1.6), Inches(3.7), Inches(0.06))
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()

    tb = s2.shapes.add_textbox(Inches(1.0 + i * 4.0), Inches(1.8), Inches(3.3), Inches(1.8))
    tf = tb.text_frame
    p_v = tf.paragraphs[0]
    p_v.text = val
    p_v.font.size = Pt(26)
    p_v.font.bold = True
    p_v.font.color.rgb = color

    p_t = tf.add_paragraph()
    p_t.text = title
    p_t.font.size = Pt(11)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_NAVY_DARK

    p_d = tf.add_paragraph()
    p_d.text = desc
    p_d.font.size = Pt(9)
    p_d.font.color.rgb = COLOR_TEXT_MUTED

# 2 Columns for Existing Limitations vs VitalSphere Solution (Angular)
c_left = create_angular_card(s2, Inches(0.8), Inches(4.1), Inches(5.7), Inches(2.9), bg_color=COLOR_WHITE, border_color=COLOR_RED_PRIMARY)
tb_l = s2.shapes.add_textbox(Inches(1.0), Inches(4.2), Inches(5.3), Inches(2.6))
tf_l = tb_l.text_frame
p_lh = tf_l.paragraphs[0]
p_lh.text = "CURRENT SYSTEM FLAWS (LEGACY PROCESS)"
p_lh.font.size = Pt(11)
p_lh.font.bold = True
p_lh.font.color.rgb = COLOR_RED_PRIMARY

flaws = [
    "Unverified volunteer registrations with no medical documentation",
    "Premature donations bypassing the statutory 90-day cooldown interval",
    "Relatives forced to make frantic manual phone calls and social media pleas",
    "Zero digital audit trail for medical fitness or pathology proof documents"
]
for f in flaws:
    p = tf_l.add_paragraph()
    p.text = "• " + f
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_MAIN

c_right = create_angular_card(s2, Inches(6.8), Inches(4.1), Inches(5.7), Inches(2.9), bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER)
tb_r = s2.shapes.add_textbox(Inches(7.0), Inches(4.2), Inches(5.3), Inches(2.6))
tf_r = tb_r.text_frame
p_rh = tf_r.paragraphs[0]
p_rh.text = "THE VITALSPHERE SOLUTION"
p_rh.font.size = Pt(11)
p_rh.font.bold = True
p_rh.font.color.rgb = COLOR_NAVY_DARK

sol = [
    "Synchronized Java 21 desktop client + cloud-connected progressive web portal",
    "Automated physiological screening: Hb >= 12.5 g/dL and resting days >= 90",
    "Mandatory digital inspection of doctor-signed certificates and lab proofs",
    "Instant telephonic & notification dispatch matching voluntary donors in seconds"
]
for s in sol:
    p = tf_r.add_paragraph()
    p.text = "✓ " + s
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK

# ==============================================================================
# SLIDE 3: SYSTEM TOPOLOGY & ARCHITECTURE ILLUSTRATION
# ==============================================================================
s3 = prs.slides.add_slide(blank_layout)
set_slide_background(s3)
add_slide_header(s3, "System Topology: Synchronized Dual-Platform Ecosystem", "SYSTEM ARCHITECTURE & CLOUD DATA PIPELINE")

# Angular Diagram Boxes
nodes = [
    ("WEB CLIENT & MOBILE PWA", "HTML5 • Modern Vanilla JS • CSS3", "Public registration, stock telemetry & emergency blood requests", Inches(0.8), Inches(1.8), COLOR_RED_PRIMARY),
    ("FIREBASE CLOUD INFRASTRUCTURE", "Firestore • Cloud Storage • CDN", "Encrypted document archive, REST endpoints & ETag caching", Inches(4.9), Inches(1.8), COLOR_NAVY_DARK),
    ("JAVA 21 DESKTOP APPLICATION", "Java Swing • AWT • Concurrency", "Medical officer clearance desk, donor roster & local cache", Inches(9.0), Inches(1.8), COLOR_RED_DARK)
]

for title, tech, desc, left, top, color in nodes:
    card = create_angular_card(s3, left, top, Inches(3.5), Inches(2.3), bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER)
    bar = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(3.5), Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()

    tb = s3.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), Inches(3.1), Inches(1.8))
    tf = tb.text_frame
    p_t = tf.paragraphs[0]
    p_t.text = title
    p_t.font.size = Pt(11)
    p_t.font.bold = True
    p_t.font.color.rgb = color

    p_tc = tf.add_paragraph()
    p_tc.text = tech
    p_tc.font.size = Pt(8.5)
    p_tc.font.bold = True
    p_tc.font.color.rgb = COLOR_NAVY_DARK

    p_d = tf.add_paragraph()
    p_d.text = desc
    p_d.font.size = Pt(9)
    p_d.font.color.rgb = COLOR_TEXT_MUTED

# Architecture Connection Flow Details
flow_card = create_angular_card(s3, Inches(0.8), Inches(4.5), Inches(11.733), Inches(2.4), bg_color=COLOR_WHITE, border_color=COLOR_BORDER)
tb_fl = s3.shapes.add_textbox(Inches(1.0), Inches(4.6), Inches(11.3), Inches(2.1))
tf_fl = tb_fl.text_frame
p_fh = tf_fl.paragraphs[0]
p_fh.text = "DATA SYNCHRONIZATION & CONCURRENCY ARCHITECTURE"
p_fh.font.size = Pt(11)
p_fh.font.bold = True
p_fh.font.color.rgb = COLOR_RED_PRIMARY

points = [
    "Bi-directional Synchronization: Web submissions immediately propagate to cloud endpoints, ingested by Java client via ScheduledExecutorService polling.",
    "Non-Blocking Concurrency: Background HTTP GET requests run on dedicated daemon threads, preventing Java Swing Event Dispatch Thread (EDT) starvation.",
    "Aadhaar Privacy Redaction: Government identity numbers are masked on client ingestion (XXXX-XXXX-1234) ensuring complete statutory compliance.",
    "Local Fail-Safe Cache: If network disconnection occurs, the Java Swing client serves cached records from local JVM memory with zero interruption."
]
for pt in points:
    p = tf_fl.add_paragraph()
    p.text = "→ " + pt
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_MAIN

# ==============================================================================
# SLIDE 4: WEB PLATFORM INTERFACE & LIVE TELEMETRY
# ==============================================================================
s4 = prs.slides.add_slide(blank_layout)
set_slide_background(s4)
add_slide_header(s4, "Web Platform: Public Portal & Real-Time Stock Telemetry", "WEB APPLICATION ARCHITECTURE")

# Embed Screenshot of Web Hero
if os.path.exists("target/screenshots/web_hero.png"):
    stream = get_clean_image_stream("target/screenshots/web_hero.png")
    if stream:
        s4.shapes.add_picture(stream, Inches(0.8), Inches(1.6), width=Inches(7.2))
        # Angular frame
        frame = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.6), Inches(7.2), Inches(4.6))
        frame.fill.background()
        frame.line.color.rgb = COLOR_BORDER
        frame.line.width = Pt(1.5)

# Right Side Card with Feature Analysis
create_angular_card(s4, Inches(8.3), Inches(1.6), Inches(4.2), Inches(5.3), bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER)
top_bar = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.3), Inches(1.6), Inches(4.2), Inches(0.08))
top_bar.fill.solid()
top_bar.fill.fore_color.rgb = COLOR_RED_PRIMARY
top_bar.line.fill.background()

tb_wf = s4.shapes.add_textbox(Inches(8.5), Inches(1.8), Inches(3.8), Inches(4.9))
tf_wf = tb_wf.text_frame
p_wh = tf_wf.paragraphs[0]
p_wh.text = "WEB CAPABILITIES & FEATURES"
p_wh.font.size = Pt(11)
p_wh.font.bold = True
p_wh.font.color.rgb = COLOR_RED_PRIMARY

w_feats = [
    ("Live Stock Counter:", "Real-time visualization of units available across all 8 blood groups (A+, B+, O-, etc.)."),
    ("Universal Search:", "Instant filtering across state, district, hospital, and blood group parameters."),
    ("Donor Portal:", "Self-service onboarding with document upload for doctor-signed fitness certificates."),
    ("Zero-Jank Scrolling:", "Dynamic sticky header offset navigation preventing overlap bugs."),
    ("Cloud Sync Status:", "Visual badge confirming connection with national transfusion clearinghouse.")
]
for k, v in w_feats:
    p = tf_wf.add_paragraph()
    p.text = k
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    pv = tf_wf.add_paragraph()
    pv.text = v
    pv.font.size = Pt(8.5)
    pv.font.color.rgb = COLOR_TEXT_MUTED

# ==============================================================================
# SLIDE 5: MOBILE PROGRESSIVE EXPERIENCE & EMERGENCY WORKFLOW
# ==============================================================================
s5 = prs.slides.add_slide(blank_layout)
set_slide_background(s5)
add_slide_header(s5, "Mobile PWA: On-the-Go Emergency Coordination", "PROGRESSIVE MOBILE INTERFACE")

# Embed Mobile Screenshot
if os.path.exists("target/screenshots/web_mobile.png"):
    stream = get_clean_image_stream("target/screenshots/web_mobile.png")
    if stream:
        s5.shapes.add_picture(stream, Inches(0.8), Inches(1.6), width=Inches(2.6))
        frame = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.6), Inches(2.6), Inches(5.3))
        frame.fill.background()
        frame.line.color.rgb = COLOR_BORDER
        frame.line.width = Pt(1.5)

# Middle Card: Emergency Request Flow
create_angular_card(s5, Inches(3.7), Inches(1.6), Inches(4.5), Inches(5.3), bg_color=COLOR_WHITE, border_color=COLOR_BORDER)
tb_mf = s5.shapes.add_textbox(Inches(3.9), Inches(1.8), Inches(4.1), Inches(4.9))
tf_mf = tb_mf.text_frame
p_mh = tf_mf.paragraphs[0]
p_mh.text = "MOBILE DESIGN HIGHLIGHTS"
p_mh.font.size = Pt(11)
p_mh.font.bold = True
p_mh.font.color.rgb = COLOR_RED_PRIMARY

m_pts = [
    ("Floating Pill Navigation:", "Ergonomic bottom navigation bar with crisp SVG vector icons (no emojis)."),
    ("Fullscreen Group Directory:", "Tapping any blood group chip opens a focused modal with donor tele-coordination."),
    ("Touch-Optimized Tele-Call:", "Direct dialer links (tel:+91...) connecting attendants with donors in one tap."),
    ("In-App Notification Hub:", "Emergency request alert banners with direct drill-down routing.")
]
for k, v in m_pts:
    p = tf_mf.add_paragraph()
    p.text = k
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    pv = tf_mf.add_paragraph()
    pv.text = v
    pv.font.size = Pt(8.5)
    pv.font.color.rgb = COLOR_TEXT_MUTED

# Right Card: Form & Document Upload Screenshot or Details
if os.path.exists("target/screenshots/web_emergency_req.png"):
    stream_req = get_clean_image_stream("target/screenshots/web_emergency_req.png")
    if stream_req:
        s5.shapes.add_picture(stream_req, Inches(8.5), Inches(1.6), width=Inches(4.0))
        frame = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.5), Inches(1.6), Inches(4.0), Inches(5.3))
        frame.fill.background()
        frame.line.color.rgb = COLOR_BORDER
        frame.line.width = Pt(1.5)

# ==============================================================================
# SLIDE 6: DESKTOP CLIENT — VERIFIED DONOR ROSTER
# ==============================================================================
s6 = prs.slides.add_slide(blank_layout)
set_slide_background(s6)
add_slide_header(s6, "Desktop Client: Verified Donor Roster & Health Status", "JAVA SWING DESKTOP ARCHITECTURE")

if os.path.exists("target/screenshots/java_client_donors.png"):
    stream = get_clean_image_stream("target/screenshots/java_client_donors.png")
    if stream:
        s6.shapes.add_picture(stream, Inches(0.8), Inches(1.6), width=Inches(7.8))
        frame = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.6), Inches(7.8), Inches(5.0))
        frame.fill.background()
        frame.line.color.rgb = COLOR_BORDER
        frame.line.width = Pt(1.5)

# Technical Card
create_angular_card(s6, Inches(8.9), Inches(1.6), Inches(3.6), Inches(5.0), bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER)
tb_sc = s6.shapes.add_textbox(Inches(9.1), Inches(1.8), Inches(3.2), Inches(4.6))
tf_sc = tb_sc.text_frame
p_sh = tf_sc.paragraphs[0]
p_sh.text = "SWING IMPLEMENTATION"
p_sh.font.size = Pt(11)
p_sh.font.bold = True
p_sh.font.color.rgb = COLOR_RED_PRIMARY

s_pts = [
    ("JTable & DefaultTableModel:", "High-throughput tabular grid displaying 256+ verified records with sub-millisecond scrolling."),
    ("Custom Cell Renderer:", "Extends DefaultTableCellRenderer to paint color-coded blood group tags and health badges."),
    ("Aadhaar Data Masking:", "Redacts sensitive identity numbers to ensure patient privacy compliance."),
    ("Dynamic Filter Pipeline:", "Regex-based row filtering matching names, cities, or blood groups on keystroke.")
]
for k, v in s_pts:
    p = tf_sc.add_paragraph()
    p.text = k
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    pv = tf_sc.add_paragraph()
    pv.text = v
    pv.font.size = Pt(8.5)
    pv.font.color.rgb = COLOR_TEXT_MUTED

# ==============================================================================
# SLIDE 7: DESKTOP CLIENT — EMERGENCY RECIPIENTS & ALLOCATION
# ==============================================================================
s7 = prs.slides.add_slide(blank_layout)
set_slide_background(s7)
add_slide_header(s7, "Desktop Client: Emergency Recipients & Transfusion Queue", "CRITICAL PATIENT ALLOCATION")

if os.path.exists("target/screenshots/java_client_recipients.png"):
    stream = get_clean_image_stream("target/screenshots/java_client_recipients.png")
    if stream:
        s7.shapes.add_picture(stream, Inches(0.8), Inches(1.6), width=Inches(7.8))
        frame = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.6), Inches(7.8), Inches(5.0))
        frame.fill.background()
        frame.line.color.rgb = COLOR_BORDER
        frame.line.width = Pt(1.5)

create_angular_card(s7, Inches(8.9), Inches(1.6), Inches(3.6), Inches(5.0), bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER)
tb_rc = s7.shapes.add_textbox(Inches(9.1), Inches(1.8), Inches(3.2), Inches(4.6))
tf_rc = tb_rc.text_frame
p_rh = tf_rc.paragraphs[0]
p_rh.text = "ALLOCATION LOGIC"
p_rh.font.size = Pt(11)
p_rh.font.bold = True
p_rh.font.color.rgb = COLOR_NAVY_DARK

r_pts = [
    ("Urgency Prioritization:", "Critical ICU and surgical cases flagged with high-visibility badges for immediate triage."),
    ("Component Calculation:", "Translates requested units into millilitre volume requirements (350 ml/unit standard PRBC)."),
    ("Direct Donor Pairing:", "Attendants can trigger instant donor alerts directly from the desktop workstation."),
    ("Real-Time Status:", "Switches states dynamically from LOOKING_FOR_DONORS to ALLOCATED upon commitment.")
]
for k, v in r_pts:
    p = tf_rc.add_paragraph()
    p.text = k
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    pv = tf_rc.add_paragraph()
    pv.text = v
    pv.font.size = Pt(8.5)
    pv.font.color.rgb = COLOR_TEXT_MUTED

# ==============================================================================
# SLIDE 8: MEDICAL OFFICER CLEARANCE DESK & DOCUMENT INSPECTION
# ==============================================================================
s8 = prs.slides.add_slide(blank_layout)
set_slide_background(s8)
add_slide_header(s8, "Medical Officer Clearance Desk: Statutory Document Verification", "CLINICAL AUDIT & COMPLIANCE")

if os.path.exists("target/screenshots/java_client_clearance.png"):
    stream = get_clean_image_stream("target/screenshots/java_client_clearance.png")
    if stream:
        s8.shapes.add_picture(stream, Inches(0.8), Inches(1.6), width=Inches(7.8))
        frame = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.6), Inches(7.8), Inches(5.0))
        frame.fill.background()
        frame.line.color.rgb = COLOR_BORDER
        frame.line.width = Pt(1.5)

create_angular_card(s8, Inches(8.9), Inches(1.6), Inches(3.6), Inches(5.0), bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER)
tb_cl = s8.shapes.add_textbox(Inches(9.1), Inches(1.8), Inches(3.2), Inches(4.6))
tf_cl = tb_cl.text_frame
p_ch = tf_cl.paragraphs[0]
p_ch.text = "VERIFICATION PIPELINE"
p_ch.font.size = Pt(11)
p_ch.font.bold = True
p_ch.font.color.rgb = COLOR_RED_PRIMARY

c_pts = [
    ("Doctor Certificate Inspection:", "Allows clinical officers to review signed medical fitness reports (PDF / images)."),
    ("Pathology Lab Card Proof:", "Verifies blood group laboratory tests before activating volunteer status."),
    ("Manual Officer Approval:", "Two-tier verification ensuring no unqualified donor is enrolled into the public roster."),
    ("Audit Record Archival:", "Approved files are time-stamped and recorded with administrative officer credentials.")
]
for k, v in c_pts:
    p = tf_cl.add_paragraph()
    p.text = k
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    pv = tf_cl.add_paragraph()
    pv.text = v
    pv.font.size = Pt(8.5)
    pv.font.color.rgb = COLOR_TEXT_MUTED

# ==============================================================================
# SLIDE 9: CORE JAVA CONCEPTS & OOP DESIGN
# ==============================================================================
s9 = prs.slides.add_slide(blank_layout)
set_slide_background(s9)
add_slide_header(s9, "Technical Deep Dive: Core Java Concepts & OOP Implementation", "CSE 213 CURRICULAR ALIGNMENT")

concepts = [
    ("1. Object-Oriented Domain Models", "Encapsulation & Domain Modeling", "Immutable records and domain classes (DonorRecord, RecipientRecord, BloodStock) encapsulating physiological data with strict getters and validation.", COLOR_RED_PRIMARY),
    ("2. Java Swing & AWT Architecture", "GUI Components & Renderers", "Extensive use of JFrame, JTabbedPane, JTable, and custom DefaultTableCellRenderer implementations for color-coded badges and icons.", COLOR_NAVY_DARK),
    ("3. Asynchronous Concurrency", "ScheduledExecutorService & EDT", "Multithreaded background polling via ScheduledExecutorService. Zero UI freezes using SwingUtilities.invokeLater for safe GUI state updates.", COLOR_RED_PRIMARY),
    ("4. HTTP Networking & REST Client", "java.net.http.HttpClient (Java 21)", "Modern non-blocking HTTP client executing asynchronous GET/POST operations with duration timeouts and JSON serialization.", COLOR_NAVY_DARK)
]

for i, (num_title, sub, desc, color) in enumerate(concepts):
    col = i % 2
    row = i // 2
    left = Inches(0.8 + col * 6.0)
    top = Inches(1.6 + row * 2.7)

    card = create_angular_card(s9, left, top, Inches(5.7), Inches(2.4), bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER)
    bar = s9.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(5.7), Inches(0.06))
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()

    tb = s9.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), Inches(5.3), Inches(2.0))
    tf = tb.text_frame
    p_t = tf.paragraphs[0]
    p_t.text = num_title
    p_t.font.size = Pt(12)
    p_t.font.bold = True
    p_t.font.color.rgb = color

    p_s = tf.add_paragraph()
    p_s.text = sub
    p_s.font.size = Pt(9.5)
    p_s.font.bold = True
    p_s.font.color.rgb = COLOR_NAVY_DARK

    p_d = tf.add_paragraph()
    p_d.text = desc
    p_d.font.size = Pt(9)
    p_d.font.color.rgb = COLOR_TEXT_MUTED

# ==============================================================================
# SLIDE 10: MULTITHREADING, DATA FLOW & CACHING ENGINE
# ==============================================================================
s10 = prs.slides.add_slide(blank_layout)
set_slide_background(s10)
add_slide_header(s10, "Data Synchronization Engine: Polling, Caching & Fail-Safe State", "CONCURRENCY & DATA FLOW PIPELINE")

# Illustration Flow Cards (Horizontal Pipeline)
steps = [
    ("STEP 1", "Scheduled Trigger", "ScheduledExecutorService fires every 15s on daemon pool thread", COLOR_RED_PRIMARY),
    ("STEP 2", "HTTP REST Request", "java.net.http.HttpClient issues non-blocking GET to Cloud Endpoint", COLOR_NAVY_DARK),
    ("STEP 3", "JSON Ingestion", "Payload parsed into immutable Java domain records with Aadhaar masking", COLOR_RED_PRIMARY),
    ("STEP 4", "Swing EDT Dispatch", "SwingUtilities.invokeLater safely pushes table model row updates", COLOR_NAVY_DARK)
]

for i, (st, title, desc, color) in enumerate(steps):
    left = Inches(0.8 + i * 2.95)
    card = create_angular_card(s10, left, Inches(1.7), Inches(2.8), Inches(2.3), bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER)
    bar = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, Inches(1.7), Inches(2.8), Inches(0.06))
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()

    tb = s10.shapes.add_textbox(left + Inches(0.15), Inches(1.9), Inches(2.5), Inches(1.9))
    tf = tb.text_frame
    p_s = tf.paragraphs[0]
    p_s.text = st
    p_s.font.size = Pt(9)
    p_s.font.bold = True
    p_s.font.color.rgb = color

    p_t = tf.add_paragraph()
    p_t.text = title
    p_t.font.size = Pt(11)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_NAVY_DARK

    p_d = tf.add_paragraph()
    p_d.text = desc
    p_d.font.size = Pt(8.5)
    p_d.font.color.rgb = COLOR_TEXT_MUTED

# Detailed Architecture Table / Breakdown Below
create_angular_card(s10, Inches(0.8), Inches(4.3), Inches(11.733), Inches(2.6), bg_color=COLOR_WHITE, border_color=COLOR_BORDER)
tb_df = s10.shapes.add_textbox(Inches(1.0), Inches(4.4), Inches(11.3), Inches(2.3))
tf_df = tb_df.text_frame
p_dh = tf_df.paragraphs[0]
p_dh.text = "RESILIENCE & OFFLINE TOLERANCE GUARANTEES"
p_dh.font.size = Pt(11)
p_dh.font.bold = True
p_dh.font.color.rgb = COLOR_RED_PRIMARY

guarantees = [
    ("Zero Event Dispatch Thread (EDT) Lockup:", "By isolating network I/O to background executor workers, the Java desktop GUI maintains smooth 60 FPS scrolling and instantaneous response."),
    ("Local Memory Snapshot (Fail-Safe):", "If the cloud network experiences downtime, the client seamlessly falls back to the in-memory cache, keeping hospital operations uninterrupted."),
    ("Concurrency Race Condition Prevention:", "Data structures utilize synchronized blocks and CopyOnWriteArrayList structures during model mutation, eliminating ConcurrentModificationException.")
]
for k, v in guarantees:
    p = tf_df.add_paragraph()
    p.text = k
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    pv = tf_df.add_paragraph()
    pv.text = v
    pv.font.size = Pt(8.5)
    pv.font.color.rgb = COLOR_TEXT_MUTED

# ==============================================================================
# SLIDE 11: CLINICAL COMPLIANCE & AADHAAR PRIVACY WORKFLOW
# ==============================================================================
s11 = prs.slides.add_slide(blank_layout)
set_slide_background(s11)
add_slide_header(s11, "Clinical Governance & Statutory Compliance Pipeline", "STATUTORY BLOOD TRANSFUSION PROTOCOLS")

# 3 Pillars (Angular Cards)
pillars = [
    ("PHYSIOLOGICAL SCREENING", "Statutory Vital Parameters", [
        "Hemoglobin threshold: >= 12.5 g/dL (evaluated via micro-cuvette testing)",
        "Minimum donation cooldown: 90 days required between whole blood donations",
        "Body weight threshold: Minimum 45 kg required for adult 350 ml donation",
        "Blood pressure: Systolic 100-140 mmHg, Diastolic 60-90 mmHg"
    ], COLOR_RED_PRIMARY),
    ("AADHAAR PRIVACY & REDACTION", "Digital Personal Data Protection", [
        "Full 12-digit Aadhaar captured during registration for deduplication",
        "Automated client-side redaction masks leading 8 digits (XXXX-XXXX-1234)",
        "Unmasked identity strictly accessible only by licensed medical officers",
        "Prevents identity theft and protects donor personal security"
    ], COLOR_NAVY_DARK),
    ("STATUTORY DOCUMENT AUDIT", "NBTC / CDSCO Guidelines", [
        "Mandatory upload of Registered Physician Medical Fitness Certificate",
        "Official Blood Grouping Card from licensed Pathology Laboratory",
        "Hospital Blood Transfusion Requisition Order required for recipients",
        "Immutable audit log generated upon medical officer clearance"
    ], COLOR_RED_DARK)
]

for i, (title, sub, items, color) in enumerate(pillars):
    left = Inches(0.8 + i * 4.0)
    card = create_angular_card(s11, left, Inches(1.7), Inches(3.7), Inches(5.1), bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER)
    bar = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, Inches(1.7), Inches(3.7), Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()

    tb = s11.shapes.add_textbox(left + Inches(0.2), Inches(1.9), Inches(3.3), Inches(4.7))
    tf = tb.text_frame
    p_t = tf.paragraphs[0]
    p_t.text = title
    p_t.font.size = Pt(11)
    p_t.font.bold = True
    p_t.font.color.rgb = color

    p_s = tf.add_paragraph()
    p_s.text = sub
    p_s.font.size = Pt(9)
    p_s.font.bold = True
    p_s.font.color.rgb = COLOR_NAVY_DARK

    for item in items:
        p_i = tf.add_paragraph()
        p_i.text = "• " + item
        p_i.font.size = Pt(8.5)
        p_i.font.color.rgb = COLOR_TEXT_MAIN

# ==============================================================================
# SLIDE 12: CONCLUSION, LIVE LINKS & GITHUB REPOSITORY (LAST PAGE)
# ==============================================================================
s12 = prs.slides.add_slide(blank_layout)
set_slide_background(s12)
add_slide_header(s12, "Project Summary, Live Deployments & Institutional Links", "PROJECT CONCLUSION & CODE REPOSITORY")

# Left Column: Key Achievements
create_angular_card(s12, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2), bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER)
top_left = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.7), Inches(0.08))
top_left.fill.solid()
top_left.fill.fore_color.rgb = COLOR_RED_PRIMARY
top_left.line.fill.background()

tb_ach = s12.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.3), Inches(4.8))
tf_ach = tb_ach.text_frame
p_ah = tf_ach.paragraphs[0]
p_ah.text = "SUMMARY OF ACCOMPLISHMENTS"
p_ah.font.size = Pt(12)
p_ah.font.bold = True
p_ah.font.color.rgb = COLOR_RED_PRIMARY

achievements = [
    ("Cross-Platform Parity:", "Successfully unified desktop Java Swing and cloud web technologies into one synchronized platform."),
    ("Life-Saving Impact:", "Reduces blood procurement latency from several hours down to sub-minute notifications."),
    ("Pure Java 21 Foundation:", "Exemplifies modern Java concurrency, custom table renderers, and robust OOP principles."),
    ("Clinical Rigor:", "Integrates doctor certificate review, pathology proof verification, and Aadhaar redaction.")
]
for k, v in achievements:
    p = tf_ach.add_paragraph()
    p.text = k
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY_DARK
    pv = tf_ach.add_paragraph()
    pv.text = v
    pv.font.size = Pt(9)
    pv.font.color.rgb = COLOR_TEXT_MUTED

# Right Column: Live Links (Strictly requested by User!)
create_angular_card(s12, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), bg_color=COLOR_WHITE, border_color=COLOR_RED_PRIMARY)
top_right = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.7), Inches(0.08))
top_right.fill.solid()
top_right.fill.fore_color.rgb = COLOR_NAVY_DARK
top_right.line.fill.background()

tb_lnk = s12.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.8))
tf_lnk = tb_lnk.text_frame
p_lh = tf_lnk.paragraphs[0]
p_lh.text = "LIVE DEPLOYMENT & CODE REPOSITORY"
p_lh.font.size = Pt(12)
p_lh.font.bold = True
p_lh.font.color.rgb = COLOR_NAVY_DARK

# 1. Web Portal Link Box (Angular)
c_web = create_angular_card(s12, Inches(7.0), Inches(2.3), Inches(5.3), Inches(1.3), bg_color=COLOR_RED_LIGHT, border_color=COLOR_RED_PRIMARY)
tb_w = s12.shapes.add_textbox(Inches(7.15), Inches(2.35), Inches(5.0), Inches(1.2))
tf_w = tb_w.text_frame
p_wt = tf_w.paragraphs[0]
p_wt.text = "PUBLIC CLOUD WEB PORTAL:"
p_wt.font.size = Pt(9)
p_wt.font.bold = True
p_wt.font.color.rgb = COLOR_RED_PRIMARY

p_wl = tf_w.add_paragraph()
p_wl.text = "https://vitalsphere-9351.web.app"
p_wl.font.size = Pt(13)
p_wl.font.bold = True
p_wl.font.color.rgb = COLOR_NAVY_DARK

p_wd = tf_w.add_paragraph()
p_wd.text = "Live production web deployment with mobile PWA interface"
p_wd.font.size = Pt(8.5)
p_wd.font.color.rgb = COLOR_TEXT_MUTED

# 2. GitHub Link Box (Angular)
c_git = create_angular_card(s12, Inches(7.0), Inches(3.8), Inches(5.3), Inches(1.3), bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER)
tb_g = s12.shapes.add_textbox(Inches(7.15), Inches(3.85), Inches(5.0), Inches(1.2))
tf_g = tb_g.text_frame
p_gt = tf_g.paragraphs[0]
p_gt.text = "GITHUB CODE REPOSITORY:"
p_gt.font.size = Pt(9)
p_gt.font.bold = True
p_gt.font.color.rgb = COLOR_NAVY_DARK

p_gl = tf_g.add_paragraph()
p_gl.text = "https://github.com/savagepaul100/VitalSphere"
p_gl.font.size = Pt(12)
p_gl.font.bold = True
p_gl.font.color.rgb = COLOR_RED_PRIMARY

p_gd = tf_g.add_paragraph()
p_gd.text = "Complete Java desktop source code, report docx, PPT, and web assets"
p_gd.font.size = Pt(8.5)
p_gd.font.color.rgb = COLOR_TEXT_MUTED

# 3. Academic Footer
tb_foot = s12.shapes.add_textbox(Inches(7.0), Inches(5.3), Inches(5.3), Inches(1.4))
tf_ft = tb_foot.text_frame
p_f1 = tf_ft.paragraphs[0]
p_f1.text = "Department of Computer Science and Engineering"
p_f1.font.size = Pt(10)
p_f1.font.bold = True
p_f1.font.color.rgb = COLOR_NAVY_DARK

p_f2 = tf_ft.add_paragraph()
p_f2.text = "School of Engineering and Sciences • SRM University – AP"
p_f2.font.size = Pt(9.5)
p_f2.font.color.rgb = COLOR_TEXT_MUTED

p_f3 = tf_ft.add_paragraph()
p_f3.text = "Faculty Guide: Dr. Srikanth Lukka, Assistant Professor"
p_f3.font.size = Pt(9.5)
p_f3.font.bold = True
p_f3.font.color.rgb = COLOR_RED_PRIMARY

prs.save(pptx_path)
print(f"Presentation saved successfully: {pptx_path} ({os.path.getsize(pptx_path)} bytes)")
