"""
Professional PDF Generator for Anna-Setu: Project Brief & Timeline.
Generates an executive PDF containing Part 1 (Project Brief & SDGs),
Part 2 (Dual-Track Architecture & Hardware BOM), and Part 3 (Project Timeline & Phased Roadmap).
Parts 4 & 5 (Tracker table & Best judgment disclosure) have been excluded as requested.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# Palette
PRIMARY_COLOR = colors.HexColor("#1B4D3E")     # Deep Forest Green
SECONDARY_COLOR = colors.HexColor("#0F62FE")   # IBM Blue
ACCENT_GREEN = colors.HexColor("#2E7D32")      # Success Green
TEXT_DARK = colors.HexColor("#212529")         # Dark Charcoal Body
TEXT_MUTED = colors.HexColor("#555555")        # Gray
BG_LIGHT_GREEN = colors.HexColor("#E8F5E9")    # Soft Mint Green
BG_CARD = colors.HexColor("#F8F9FA")           # Light Gray Card
BORDER_LIGHT = colors.HexColor("#E0E0E0")


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and draw total page numbers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(TEXT_MUTED)

        # Running Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(36, 812, "Anna-Setu: Project Brief & Phased Timeline • 1M1B / IBM SkillsBuild")
            self.drawRightString(559, 812, "Student: Pankhuri Govila")
            self.setStrokeColor(BORDER_LIGHT)
            self.setLineWidth(0.6)
            self.line(36, 806, 559, 806)

        # Running Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(559, 25, page_str)
        self.drawString(36, 25, "1M1B Virtual Internship • Mentor Review: paramjeet@onemoneb.org • In Collaboration with AICTE")
        self.setStrokeColor(BORDER_LIGHT)
        self.setLineWidth(0.6)
        self.line(36, 35, 559, 35)

        self.restoreState()


def build_pdf(filename="Anna_Setu_Project_Brief_Timeline_and_Tracker.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=42,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=PRIMARY_COLOR,
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=14,
        textColor=SECONDARY_COLOR,
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=PRIMARY_COLOR,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        "Heading2_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=SECONDARY_COLOR,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=TEXT_DARK,
        spaceAfter=4
    )

    table_header = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    table_cell = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=10,
        textColor=TEXT_DARK
    )

    table_cell_bold = ParagraphStyle(
        "TableCellBold",
        parent=table_cell,
        fontName="Helvetica-Bold"
    )

    table_cell_center = ParagraphStyle(
        "TableCellCenter",
        parent=table_cell,
        alignment=1
    )

    story = []

    # -------------------------------------------------------------------------
    # HEADER & META CARD
    # -------------------------------------------------------------------------
    story.append(Paragraph("ANNA-SETU: PROJECT BRIEF & PHASED TIMELINE", title_style))
    story.append(Paragraph("1M1B AI for Sustainability Virtual Internship • In Collaboration with IBM SkillsBuild & AICTE", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY_COLOR, spaceAfter=8))

    meta_table_data = [
        [
            Paragraph("<b>Intern / Author:</b> Pankhuri Govila", body_style),
            Paragraph("<b>Program:</b> 1M1B AI for Sustainability Virtual Internship", body_style),
            Paragraph("<b>1M1B Mentor:</b> Paramjeet Sir (paramjeet@onemoneb.org)", body_style)
        ],
        [
            Paragraph("<b>Primary SDG:</b> SDG 12 (Target 12.3 & 12.5)", body_style),
            Paragraph("<b>Dual-Track Model:</b> Track A (AI App) + Track B (Hardware)", body_style),
            Paragraph("<b>Milestones:</b> Prototype: End-Nov 2026 | Deploy: End-Dec 2026", body_style)
        ]
    ]
    meta_table = Table(meta_table_data, colWidths=[174, 180, 169])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_CARD),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------------------
    # PART 1: PROJECT BRIEF & SDG ALIGNMENT
    # -------------------------------------------------------------------------
    story.append(Paragraph("1. Executive Project Brief, Problem & SDG Alignment", h1_style))
    story.append(Paragraph(
        "<b>Anna-Setu</b> (from Sanskrit: <i>'Anna'</i> meaning sustenance and <i>'Setu'</i> meaning bridge) is a closed-loop socio-technical framework designed for institutional campus dining ecosystems. It attacks food waste at two interconnected points: "
        "<b>1) At the kitchen level</b>, where unforecasted safety margins create 10%-30% surplus buffers, and "
        "<b>2) At the diner plate level</b>, where students routinely take excessive portions onto their plates and dump uneaten leftovers into garbage bins.",
        body_style
    ))
    story.append(Paragraph(
        "By coupling an AI predictive software engine (<b>Track A</b>) with an on-site smart plate-waste interceptor and accelerated bio-recycling converter (<b>Track B</b>), Anna-Setu creates a zero-waste circular campus economy: untouched kitchen food is safely redistributed to verified night shelters, while plate scraps are converted on-site into high-grade organic bio-fertilizer, relieving municipal authorities (Lucknow Nagar Nigam) and preventing fugitive methane emissions in landfills.",
        body_style
    ))

    # SDG Alignment Table
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Table 1.1: Sustainable Development Goal (SDG) Alignment Matrix</b>", h2_style))
    sdg_data = [
        [Paragraph("UN SDG", table_header), Paragraph("Specific Target", table_header), Paragraph("Anna-Setu Implementation & Impact", table_header)],
        [
            Paragraph("<b>SDG 12: Responsible Consumption</b><br/><i>(Primary)</i>", table_cell),
            Paragraph("<b>Target 12.3:</b> Halve food waste by 2030.<br/><b>Target 12.5:</b> Substantially reduce waste via recycling.", table_cell),
            Paragraph("<b>Track A</b> reduces kitchen overcooking by 15-25% via predictive ML; <b>Track B</b> deters over-serving with behavioral plate nudges and upcycles plate waste into organic fertilizer.", table_cell)
        ],
        [
            Paragraph("<b>SDG 2: Zero Hunger</b><br/><i>(Secondary)</i>", table_cell),
            Paragraph("<b>Target 2.1 & 2.2:</b> End hunger; ensure access to safe, nutritious food.", table_cell),
            Paragraph("Untouched surplus is checked through FSSAI statutory holding algorithms and safely dispatched to local night shelters (Rain Basera Charbagh, KGMU, Gomti Nagar).", table_cell)
        ],
        [
            Paragraph("<b>SDG 11: Sustainable Cities</b>", table_cell),
            Paragraph("<b>Target 11.6:</b> Reduce urban municipal per-capita environmental impact.", table_cell),
            Paragraph("Eliminates organic wet-waste burden on municipal collection trucks and avoids ₹5,000-₹25,000 penalties under Lucknow Nagar Nigam Solid Waste By-Laws.", table_cell)
        ],
        [
            Paragraph("<b>SDG 13: Climate Action</b>", table_cell),
            Paragraph("<b>Target 13.3:</b> Climate mitigation and institutional awareness.", table_cell),
            Paragraph("Diverts organic matter from anaerobic landfill decomposition, eliminating methane (CH4) emissions. Real-time displays show diners their carbon and water footprints.", table_cell)
        ]
    ]
    t_sdg = Table(sdg_data, colWidths=[105, 128, 290])
    t_sdg.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_COLOR),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_CARD])
    ]))
    story.append(t_sdg)

    # Beneficiaries Card
    story.append(Spacer(1, 5))
    story.append(Paragraph("<b>Target Beneficiaries:</b> <b>1) Students:</b> Dynamic nudges build mindful eating habits; <b>2) Mess Management:</b> Cuts procurement bills by 15-25%; <b>3) Lucknow Nagar Nigam:</b> Zero waste burden hauled to landfills; <b>4) Local Shelters:</b> Reliable access to verified nutritious meals; <b>5) Campus Grounds:</b> Free high-grade bio-fertilizer.", body_style))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PART 2: DUAL-TRACK SOLUTION ARCHITECTURE
    # -------------------------------------------------------------------------
    story.append(Paragraph("2. Dual-Track Integrated Solution Architecture", h1_style))
    story.append(Paragraph(
        "Anna-Setu operates two synchronized operational tracks bridging the physical dining floor with digital cloud intelligence:",
        body_style
    ))

    # Track A & B summary boxes
    track_summary_data = [
        [
            Paragraph("<b>TRACK A: ANNA-SETU AI SOFTWARE PLATFORM</b><br/><i>(Status: In Progress / Working Prototype Deployed)</i>", ParagraphStyle("THeaderA", parent=table_cell_bold, textColor=PRIMARY_COLOR, fontSize=8.5)),
            Paragraph("<b>TRACK B: SMART PLATE-WASTE BIO-RECYCLER</b><br/><i>(Status: In Ideation / Hardware Prototype in Progress)</i>", ParagraphStyle("THeaderB", parent=table_cell_bold, textColor=SECONDARY_COLOR, fontSize=8.5))
        ],
        [
            Paragraph(
                "• <b>Module 1 (Dining Demand Advisor):</b> Time-series forecasting model predicting next-day cooking volumes based on turnstiles, exams, and weather.<br/>"
                "• <b>Module 2 (RAG Compliance Engine):</b> Grounded in <b>FSSAI Surplus Regulations (2019)</b> (danger zone 5°C-65°C, 2h/4h ambient rule) and <b>Lucknow Nagar Nigam By-Laws</b> (45m transit buffer across 8 zones).<br/>"
                "• <b>IBM Granite Model Compiler:</b> Generates WhatsApp/SMS alerts (<60w) and official <b>FSSAI Form B & LNN Gate Pass manifests</b>.<br/>"
                "• <b>Live Assets:</b> Deployed on Hugging Face Spaces (Gradio) and local Streamlit app with 5 automated test cases.",
                table_cell
            ),
            Paragraph(
                "• <b>Behavioral Nudge Front-End:</b> Precision plate scale (0-20kg) at tray return counter + 7-inch display showing wasted grams, water footprint, and hostel leaderboards to stop diners from taking extra food.<br/>"
                "• <b>Pre-Processing Shredder:</b> Reduces uneaten food scrap size to 3-5mm.<br/>"
                "• <b>Accelerated Bio-Composting Chamber:</b> Thermophilic heating (55°C-65°C) + active aerobic aeration + microbial enzymes achieve <b>85%-90% volume reduction in 12-24h</b>.<br/>"
                "• <b>Recyclable Resource Output:</b> High-grade <b>Organic Bio-Fertilizer / Soil Conditioner</b> for campus greenery and local farmers.<br/>"
                "• <b>IoT Cloud Bridge:</b> ESP32 streams daily plate waste logs back to Track A AI.",
                table_cell
            )
        ]
    ]
    t_tracks = Table(track_summary_data, colWidths=[260, 263])
    t_tracks.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), BG_LIGHT_GREEN),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#EBF3FE")),
        ('BACKGROUND', (0,1), (0,1), colors.white),
        ('BACKGROUND', (1,1), (1,1), colors.white),
        ('BOX', (0,0), (0,-1), 1, PRIMARY_COLOR),
        ('BOX', (1,0), (1,-1), 1, SECONDARY_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_tracks)

    # Hardware BOM Table
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Table 2.1: Track B Hardware Bill of Materials (BOM) & Cost Feasibility</b>", h2_style))
    bom_data = [
        [Paragraph("Subsystem", table_header), Paragraph("Component", table_header), Paragraph("Technical Role in Station", table_header), Paragraph("Est. Cost (INR)", table_header)],
        [Paragraph("Compute / IoT", table_cell_bold), Paragraph("ESP32 WROOM-32 MCU", table_cell), Paragraph("Wi-Fi telemetry, sensor polling, cloud API bridge", table_cell), Paragraph("₹450", table_cell_center)],
        [Paragraph("Plate Waste Scale", table_cell_bold), Paragraph("0-20 kg Load Cell + HX711", table_cell), Paragraph("Measures individual student plate waste left on tray", table_cell), Paragraph("₹550", table_cell_center)],
        [Paragraph("Nudge Display", table_cell_bold), Paragraph("7-inch IPS / OLED Screen", table_cell), Paragraph("Displays wasted grams, water footprint & leaderboard", table_cell), Paragraph("₹850", table_cell_center)],
        [Paragraph("Thermal Sensing", table_cell_bold), Paragraph("MLX90614 Contactless IR", table_cell), Paragraph("Verifies kitchen surplus food is held safe >=65°C", table_cell), Paragraph("₹750", table_cell_center)],
        [Paragraph("Aerobic Aeration", table_cell_bold), Paragraph("12V Brushless Fan + Carbon", table_cell), Paragraph("Supplies oxygen to composting chamber; stops odors", table_cell), Paragraph("₹250", table_cell_center)],
        [Paragraph("Thermophilic Heat", table_cell_bold), Paragraph("100W PTC Ceramic Strip", table_cell), Paragraph("Maintains 55°C-65°C to accelerate microbial breakdown", table_cell), Paragraph("₹450", table_cell_center)],
        [Paragraph("Power & Housing", table_cell_bold), Paragraph("12V SMPS + SS Kiosk", table_cell), Paragraph("Regulated power and IP65 sanitary stainless housing", table_cell), Paragraph("₹1,370", table_cell_center)],
        [Paragraph("TOTAL BOM", table_cell_bold), Paragraph("<b>Complete Integrated Kiosk</b>", table_cell_bold), Paragraph("<b>Affordable, student-built IoT bio-recycler prototype</b>", table_cell_bold), Paragraph("<b>₹4,670 (~$55)</b>", table_cell_center)]
    ]
    t_bom = Table(bom_data, colWidths=[90, 130, 223, 80])
    t_bom.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_COLOR),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,-1), (-1,-1), BG_LIGHT_GREEN),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, BG_CARD])
    ]))
    story.append(t_bom)

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # PART 3: PROJECT TIMELINE & PHASED ROADMAP
    # -------------------------------------------------------------------------
    story.append(Paragraph("3. Project Timeline & Phased Execution Roadmap", h1_style))
    story.append(Paragraph(
        "The project follows a structured two-month Agile delivery plan anchored to program milestones: "
        "<b>Milestone 1 (End of November 2026):</b> Working prototypes of Track A and Track B integrated, with campus administration approvals; "
        "<b>Milestone 2 (End of December 2026):</b> Live on-campus 2-week pilot deployment, AI model retraining on real waste data, and final impact handover.",
        body_style
    ))
    story.append(Spacer(1, 6))

    timeline_data = [
        [Paragraph("Phase / Sprint", table_header), Paragraph("Date Range", table_header), Paragraph("Key Work Deliverables & Activities", table_header), Paragraph("Gate Status", table_header)],
        [
            Paragraph("<b>Phase 1 & 2:</b><br/>RAG Engine & UI", table_cell),
            Paragraph("Nov 1 - Nov 10, 2026", table_cell_center),
            Paragraph("Codified FSSAI 2019 and LNN by-laws into JSON KB; built TF-IDF vector retriever, compliance calculator, and IBM Granite notification compiler. Deployed Gradio demo on Hugging Face and local Streamlit app. Verified 5 automated test cases.", table_cell),
            Paragraph("<font color='#155724'><b>COMPLETED</b></font>", table_cell_center)
        ],
        [
            Paragraph("<b>Sprint 3A:</b><br/>HW Breadboard & IoT", table_cell),
            Paragraph("Nov 11 - Nov 20, 2026", table_cell_center),
            Paragraph("Procure ESP32, load cell, MLX90614 IR sensor, and display; assemble bench breadboard; flash C++/MicroPython firmware (esp32_smart_kiosk.ino); bridge telemetry to api_server.py.", table_cell),
            Paragraph("<font color='#856404'><b>IN PROGRESS</b></font>", table_cell_center)
        ],
        [
            Paragraph("<b>Sprint 3B:</b><br/>Approvals & Gate 1", table_cell),
            Paragraph("Nov 21 - Nov 30, 2026", table_cell_center),
            Paragraph("Draft permission letter to Dean of Student Welfare / Campus Mess Committee; establish coordination agreement with Rain Basera Charbagh; <b>Milestone 1 Gate Review with 1M1B mentor</b>.", table_cell),
            Paragraph("<b>MILESTONE 1 GATE</b><br/>(End-Nov 2026)", table_cell_center)
        ],
        [
            Paragraph("<b>Phase 4:</b><br/>Enclosure & Pilot", table_cell),
            Paragraph("Dec 1 - Dec 21, 2026", table_cell_center),
            Paragraph("Assemble IP65 stainless enclosure at tray return; conduct 14-day live campus pilot in student mess; log plate-waste reduction via nudge screen; dispatch compliant kitchen surplus; produce first batch of bio-fertilizer.", table_cell),
            Paragraph("PLANNED PILOT<br/>(Central Mess)", table_cell_center)
        ],
        [
            Paragraph("<b>Phase 5:</b><br/>Impact & Closeout", table_cell),
            Paragraph("Dec 22 - Dec 31, 2026", table_cell_center),
            Paragraph("Retrain Module 1 demand model on real pilot plate-waste logs; compute total kg rescued, kg bio-fertilizer harvested, methane avoided, and procurement ₹ saved. Submit final PDF report, PPT, and demo video.", table_cell),
            Paragraph("<b>MILESTONE 2 GATE</b><br/>(End-Dec 2026)", table_cell_center)
        ]
    ]
    t_timeline = Table(timeline_data, colWidths=[90, 85, 268, 80])
    t_timeline.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_COLOR),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_CARD])
    ]))
    story.append(t_timeline)

    story.append(Spacer(1, 14))
    story.append(HRFlowable(width="100%", thickness=1, color=BORDER_LIGHT, spaceAfter=8))
    story.append(Paragraph(
        "<b>Summary Note:</b> The project tracker and activity task breakdown are maintained dynamically in the collaborative Google Sheets register: "
        "<b><font color='#0F62FE'>PankhuriGovila_YIRP</font></b>, shared with <b>paramjeet@onemoneb.org</b>. "
        "The Excel source file is available at <code>PankhuriGovila_YIRP_Project_Tracker.xlsx</code>.",
        body_style
    ))

    # Build Document with NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully built: {filename}")


if __name__ == "__main__":
    build_pdf()
