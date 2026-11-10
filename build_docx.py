"""
Generates the editable Microsoft Word (.docx) version of:
Anna_Setu_Project_Brief_Timeline_and_Tracker.docx
Exact replica of the 3-page PDF with Parts 1, 2, and 3.
"""

import zipfile
import xml.sax.saxutils as saxutils

def escape(txt):
    return saxutils.escape(txt)

def p_xml(text="", style=None, bold=False, italic=False, color=None, size_pt=None, space_after_pt=4, space_before_pt=0, align=None):
    pPr = "<w:pPr>"
    if style:
        pPr += f'<w:pStyle w:val="{style}"/>'
    if align:
        pPr += f'<w:jc w:val="{align}"/>'
    pPr += f'<w:spacing w:before="{int(space_before_pt * 20)}" w:after="{int(space_after_pt * 20)}"/>'
    pPr += "</w:pPr>"
    
    rPr = "<w:rPr>"
    if bold:
        rPr += "<w:b/>"
    if italic:
        rPr += "<w:i/>"
    if color:
        rPr += f'<w:color w:val="{color}"/>'
    if size_pt:
        rPr += f'<w:sz w:val="{int(size_pt * 2)}"/><w:szCs w:val="{int(size_pt * 2)}"/>'
    rPr += "</w:rPr>"
    
    return f"<w:p>{pPr}<w:r>{rPr}<w:t>{escape(text)}</w:t></w:r></w:p>"

def run_xml(text, bold=False, italic=False, color=None, size_pt=None):
    rPr = "<w:rPr>"
    if bold:
        rPr += "<w:b/>"
    if italic:
        rPr += "<w:i/>"
    if color:
        rPr += f'<w:color w:val="{color}"/>'
    if size_pt:
        rPr += f'<w:sz w:val="{int(size_pt * 2)}"/><w:szCs w:val="{int(size_pt * 2)}"/>'
    rPr += "</w:rPr>"
    return f"<w:r>{rPr}<w:t xml:space=\"preserve\">{escape(text)}</w:t></w:r>"

def p_multi_run(runs, style=None, space_after_pt=4, space_before_pt=0, align=None):
    pPr = "<w:pPr>"
    if style:
        pPr += f'<w:pStyle w:val="{style}"/>'
    if align:
        pPr += f'<w:jc w:val="{align}"/>'
    pPr += f'<w:spacing w:before="{int(space_before_pt * 20)}" w:after="{int(space_after_pt * 20)}"/>'
    pPr += "</w:pPr>"
    
    body = "".join(run_xml(r[0], bold=r[1] if len(r)>1 else False, italic=r[2] if len(r)>2 else False, color=r[3] if len(r)>3 else None, size_pt=r[4] if len(r)>4 else None) for r in runs)
    return f"<w:p>{pPr}{body}</w:p>"

def table_xml(rows_data, col_widths, col_align=None, header_bg="1B4D3E", border_color="D3D3D3"):
    tblPr = f"""<w:tblPr>
        <w:tblW w:w="5000" w:type="pct"/>
        <w:tblBorders>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>
            <w:left w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>
            <w:insideV w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>
        </w:tblBorders>
        <w:tblCellMar>
            <w:top w:w="120" w:type="dxa"/>
            <w:bottom w:w="120" w:type="dxa"/>
            <w:left w:w="150" w:type="dxa"/>
            <w:right w:w="150" w:type="dxa"/>
        </w:tblCellMar>
    </w:tblPr>"""
    
    grid = "<w:tblGrid>" + "".join(f'<w:gridCol w:w="{w}"/>' for w in col_widths) + "</w:tblGrid>"
    
    rows_xml = []
    for r_idx, row in enumerate(rows_data):
        is_header = (r_idx == 0 and header_bg is not None)
        trPr = "<w:trPr>"
        if is_header:
            trPr += "<w:tblHeader/>"
        trPr += "</w:trPr>"
        
        tcs = []
        for c_idx, cell in enumerate(row):
            w = col_widths[c_idx] if c_idx < len(col_widths) else 2000
            shd = f'<w:shd w:val="clear" w:color="auto" w:fill="{header_bg}"/>' if is_header else (
                '<w:shd w:val="clear" w:color="auto" w:fill="F8F9FA"/>' if r_idx % 2 == 1 else '<w:shd w:val="clear" w:color="auto" w:fill="FFFFFF"/>'
            )
            tcPr = f"<w:tcPr><w:tcW w:w=\"{w}\" w:type=\"dxa\"/>{shd}</w:tcPr>"
            
            align = col_align[c_idx] if col_align and c_idx < len(col_align) else ("center" if is_header else "left")
            
            if isinstance(cell, list):
                cell_content = "".join(cell)
            elif isinstance(cell, str) and cell.strip().startswith("<w:p"):
                cell_content = cell
            else:
                text_color = "FFFFFF" if is_header else "212529"
                bold = is_header
                cell_content = p_xml(cell, bold=bold, color=text_color, size_pt=9.5 if not is_header else 9.5, align=align, space_after_pt=2)
                
            tcs.append(f"<w:tc>{tcPr}{cell_content}</w:tc>")
            
        rows_xml.append(f"<w:tr>{trPr}{''.join(tcs)}</w:tr>")
        
    return f"<w:tbl>{tblPr}{grid}{''.join(rows_xml)}</w:tbl>"

def generate_document_xml():
    body = []
    
    # Title & Subtitle
    body.append(p_xml("ANNA-SETU: PROJECT BRIEF & PHASED TIMELINE", bold=True, color="1B4D3E", size_pt=20, space_after_pt=3))
    body.append(p_xml("1M1B AI for Sustainability Virtual Internship • In Collaboration with IBM SkillsBuild & AICTE", color="0F62FE", size_pt=11, space_after_pt=10))
    
    # Meta Card Table
    meta_rows = [
        [
            p_multi_run([("Intern / Author: ", True), ("Pankhuri Govila", False)]),
            p_multi_run([("Program: ", True), ("1M1B AI for Sustainability Virtual Internship", False)]),
            p_multi_run([("1M1B Mentor: ", True), ("Paramjeet Sir (paramjeet@onemoneb.org)", False)])
        ],
        [
            p_multi_run([("Primary SDG: ", True), ("SDG 12 (Target 12.3 & 12.5)", False)]),
            p_multi_run([("Dual-Track Model: ", True), ("Track A (AI App) + Track B (Hardware)", False)]),
            p_multi_run([("Milestones: ", True), ("Prototype: End-Nov 2026 | Deploy: End-Dec 2026", False)])
        ]
    ]
    body.append(table_xml(meta_rows, [3100, 3300, 3100], header_bg=None, border_color="1B4D3E"))
    body.append(p_xml("", space_after_pt=6))
    
    # -------------------------------------------------------------------------
    # PART 1: PROJECT BRIEF & SDG ALIGNMENT
    # -------------------------------------------------------------------------
    body.append(p_xml("1. Executive Project Brief, Problem & SDG Alignment", style="Heading1", bold=True, color="1B4D3E", size_pt=14, space_before_pt=8, space_after_pt=4))
    body.append(p_multi_run([
        ("Anna-Setu ", True, False, "1B4D3E"),
        ("(from Sanskrit: 'Anna' meaning sustenance and 'Setu' meaning bridge) is a closed-loop socio-technical framework designed for institutional campus dining ecosystems. It attacks food waste at two interconnected points: ", False),
        ("1) At the kitchen level", True),
        (", where unforecasted safety margins create 10%-30% surplus buffers, and ", False),
        ("2) At the diner plate level", True),
        (", where students routinely take excessive portions onto their plates and dump uneaten leftovers into garbage bins.", False)
    ], space_after_pt=4))
    
    body.append(p_multi_run([
        ("By coupling an AI predictive software engine (", False),
        ("Track A", True, False, "1B4D3E"),
        (") with an on-site smart plate-waste interceptor and accelerated bio-recycling converter (", False),
        ("Track B", True, False, "0F62FE"),
        ("), Anna-Setu creates a zero-waste circular campus economy: untouched kitchen food is safely redistributed to verified night shelters, while plate scraps are converted on-site into high-grade organic bio-fertilizer, relieving municipal authorities (Lucknow Nagar Nigam) and preventing fugitive methane emissions in landfills.", False)
    ], space_after_pt=6))
    
    # Table 1.1: SDG Alignment Matrix
    body.append(p_xml("Table 1.1: Sustainable Development Goal (SDG) Alignment Matrix", style="Heading2", bold=True, color="0F62FE", size_pt=11, space_before_pt=6, space_after_pt=3))
    sdg_rows = [
        ["UN SDG", "Specific Target", "Anna-Setu Implementation & Impact"],
        [
            p_multi_run([("SDG 12: Responsible Consumption\n", True), ("(Primary)", True, True, "1B4D3E")]),
            p_multi_run([("Target 12.3: ", True), ("Halve food waste by 2030.\n", False), ("Target 12.5: ", True), ("Substantially reduce waste via recycling.", False)]),
            p_multi_run([("Track A ", True), ("reduces kitchen overcooking by 15-25% via predictive ML; ", False), ("Track B ", True), ("deters over-serving with behavioral plate nudges and upcycles plate waste into organic fertilizer.", False)])
        ],
        [
            p_multi_run([("SDG 2: Zero Hunger\n", True), ("(Secondary)", True, True, "1B4D3E")]),
            p_multi_run([("Target 2.1 & 2.2: ", True), ("End hunger; ensure access to safe, nutritious food.", False)]),
            p_multi_run([("Untouched surplus is checked through FSSAI statutory holding algorithms and safely dispatched to local night shelters (Rain Basera Charbagh, KGMU, Gomti Nagar).", False)])
        ],
        [
            p_multi_run([("SDG 11: Sustainable Cities", True)]),
            p_multi_run([("Target 11.6: ", True), ("Reduce urban municipal per-capita environmental impact.", False)]),
            p_multi_run([("Eliminates organic wet-waste burden on municipal collection trucks and avoids ₹5,000-₹25,000 penalties under Lucknow Nagar Nigam Solid Waste By-Laws.", False)])
        ],
        [
            p_multi_run([("SDG 13: Climate Action", True)]),
            p_multi_run([("Target 13.3: ", True), ("Climate mitigation and institutional awareness.", False)]),
            p_multi_run([("Diverts organic matter from anaerobic landfill decomposition, eliminating methane (CH4) emissions. Real-time displays show diners their carbon and water footprints.", False)])
        ]
    ]
    body.append(table_xml(sdg_rows, [2200, 2400, 4900], header_bg="1B4D3E"))
    
    # Target Beneficiaries
    body.append(p_xml("", space_after_pt=3))
    body.append(p_multi_run([
        ("Target Beneficiaries: ", True, False, "1B4D3E"),
        ("1) Students: ", True), ("Dynamic nudges build mindful eating habits; ", False),
        ("2) Mess Management: ", True), ("Cuts procurement bills by 15-25%; ", False),
        ("3) Lucknow Nagar Nigam: ", True), ("Zero waste burden hauled to landfills; ", False),
        ("4) Local Shelters: ", True), ("Reliable access to verified nutritious meals; ", False),
        ("5) Campus Grounds: ", True), ("Free high-grade bio-fertilizer.", False)
    ], space_after_pt=6))
    
    # Page Break
    body.append("<w:p><w:r><w:br w:type=\"page\"/></w:r></w:p>")
    
    # -------------------------------------------------------------------------
    # PART 2: DUAL-TRACK ARCHITECTURE & HARDWARE BOM
    # -------------------------------------------------------------------------
    body.append(p_xml("2. Dual-Track Integrated Solution Architecture", style="Heading1", bold=True, color="1B4D3E", size_pt=14, space_before_pt=6, space_after_pt=4))
    body.append(p_xml("Anna-Setu operates two synchronized operational tracks bridging the physical dining floor with digital cloud intelligence:", space_after_pt=6))
    
    # Track Comparison Table
    track_rows = [
        [
            p_xml("TRACK A: ANNA-SETU AI SOFTWARE PLATFORM\n(Status: In Progress / Working Prototype Deployed)", bold=True, color="FFFFFF", size_pt=10, align="center"),
            p_xml("TRACK B: SMART PLATE-WASTE BIO-RECYCLER\n(Status: In Ideation / Hardware Prototype in Progress)", bold=True, color="FFFFFF", size_pt=10, align="center")
        ],
        [
            [
                p_multi_run([("• Module 1 (Dining Demand Advisor): ", True), ("Time-series forecasting model predicting next-day cooking volumes based on turnstiles, exams, and weather.", False)]),
                p_multi_run([("• Module 2 (RAG Compliance Engine): ", True), ("Grounded in ", False), ("FSSAI Surplus Regulations (2019) ", True), ("(danger zone 5°C-65°C, 2h/4h ambient rule) and ", False), ("Lucknow Nagar Nigam By-Laws ", True), ("(45m transit buffer across 8 zones).", False)]),
                p_multi_run([("• IBM Granite Model Compiler: ", True), ("Generates WhatsApp/SMS alerts (<60w) and official ", False), ("FSSAI Form B & LNN Gate Pass manifests", True), (".", False)]),
                p_multi_run([("• Live Assets: ", True), ("Deployed on Hugging Face Spaces (Gradio) and local Streamlit app with 5 automated test cases.", False)])
            ],
            [
                p_multi_run([("• Behavioral Nudge Front-End: ", True), ("Precision plate scale (0-20kg) at tray return counter + 7-inch display showing wasted grams, water footprint, and hostel leaderboards to stop diners from taking extra food.", False)]),
                p_multi_run([("• Pre-Processing Shredder: ", True), ("Reduces uneaten food scrap size to 3-5mm.", False)]),
                p_multi_run([("• Accelerated Bio-Composting Chamber: ", True), ("Thermophilic heating (55°C-65°C) + active aerobic aeration + microbial enzymes achieve ", False), ("85%-90% volume reduction in 12-24h", True), (".", False)]),
                p_multi_run([("• Recyclable Resource Output: ", True), ("High-grade ", False), ("Organic Bio-Fertilizer / Soil Conditioner ", True), ("for campus greenery and local farmers.", False)]),
                p_multi_run([("• IoT Cloud Bridge: ", True), ("ESP32 streams daily plate waste logs back to Track A AI.", False)])
            ]
        ]
    ]
    body.append(table_xml(track_rows, [4750, 4750], header_bg="1B4D3E"))
    body.append(p_xml("", space_after_pt=6))
    
    # Table 2.1: Hardware BOM
    body.append(p_xml("Table 2.1: Track B Hardware Bill of Materials (BOM) & Cost Feasibility", style="Heading2", bold=True, color="0F62FE", size_pt=11, space_before_pt=6, space_after_pt=3))
    bom_rows = [
        ["Subsystem", "Component", "Technical Role in Station", "Est. Cost (INR)"],
        ["Compute / IoT", "ESP32 WROOM-32 MCU", "Wi-Fi telemetry, sensor polling, cloud API bridge", "₹450"],
        ["Plate Waste Scale", "0-20 kg Load Cell + HX711", "Measures individual student plate waste left on tray", "₹550"],
        ["Nudge Display", "7-inch IPS / OLED Screen", "Displays wasted grams, water footprint & leaderboard", "₹850"],
        ["Thermal Sensing", "MLX90614 Contactless IR", "Verifies kitchen surplus food is held safe >=65°C", "₹750"],
        ["Aerobic Aeration", "12V Brushless Fan + Carbon", "Supplies oxygen to composting chamber; stops odors", "₹250"],
        ["Thermophilic Heat", "100W PTC Ceramic Strip", "Maintains 55°C-65°C to accelerate microbial breakdown", "₹450"],
        ["Power & Housing", "12V SMPS + SS Kiosk", "Regulated power and IP65 sanitary stainless housing", "₹1,370"],
        [
            p_xml("TOTAL BOM", bold=True, color="1B4D3E", size_pt=9.5),
            p_xml("Complete Integrated Kiosk", bold=True, color="1B4D3E", size_pt=9.5),
            p_xml("Affordable, student-built IoT bio-recycler prototype", bold=True, color="1B4D3E", size_pt=9.5),
            p_xml("₹4,670 (~$55)", bold=True, color="1B4D3E", size_pt=9.5, align="center")
        ]
    ]
    body.append(table_xml(bom_rows, [1800, 2400, 3900, 1400], header_bg="1B4D3E", col_align=["left", "left", "left", "center"]))
    
    # Page Break
    body.append("<w:p><w:r><w:br w:type=\"page\"/></w:r></w:p>")
    
    # -------------------------------------------------------------------------
    # PART 3: PROJECT TIMELINE & PHASED ROADMAP
    # -------------------------------------------------------------------------
    body.append(p_xml("3. Project Timeline & Phased Execution Roadmap", style="Heading1", bold=True, color="1B4D3E", size_pt=14, space_before_pt=6, space_after_pt=4))
    body.append(p_multi_run([
        ("The project follows a structured two-month Agile delivery plan anchored to program milestones: ", False),
        ("Milestone 1 (End of November 2026): ", True),
        ("Working prototypes of Track A and Track B integrated, with campus administration approvals; ", False),
        ("Milestone 2 (End of December 2026): ", True),
        ("Live on-campus 2-week pilot deployment, AI model retraining on real waste data, and final impact handover.", False)
    ], space_after_pt=6))
    
    # Table 3.1: Timeline
    timeline_rows = [
        ["Phase / Sprint", "Date Range", "Key Work Deliverables & Activities", "Gate Status"],
        [
            p_multi_run([("Phase 1 & 2:\n", True), ("RAG Engine & UI", False)]),
            p_xml("Nov 1 - Nov 10, 2026", align="center"),
            p_xml("Codified FSSAI 2019 and LNN by-laws into JSON KB; built TF-IDF vector retriever, compliance calculator, and IBM Granite notification compiler. Deployed Gradio demo on Hugging Face and local Streamlit app. Verified 5 automated test cases."),
            p_xml("COMPLETED", bold=True, color="155724", align="center")
        ],
        [
            p_multi_run([("Sprint 3A:\n", True), ("HW Breadboard & IoT", False)]),
            p_xml("Nov 11 - Nov 20, 2026", align="center"),
            p_xml("Procure ESP32, load cell, MLX90614 IR sensor, and display; assemble bench breadboard; flash C++/MicroPython firmware (esp32_smart_kiosk.ino); bridge telemetry to api_server.py."),
            p_xml("IN PROGRESS", bold=True, color="856404", align="center")
        ],
        [
            p_multi_run([("Sprint 3B:\n", True), ("Approvals & Gate 1", False)]),
            p_xml("Nov 21 - Nov 30, 2026", align="center"),
            p_xml("Draft permission letter to Dean of Student Welfare / Campus Mess Committee; establish coordination agreement with Rain Basera Charbagh; Milestone 1 Gate Review with 1M1B mentor."),
            p_xml("MILESTONE 1 GATE\n(End-Nov 2026)", bold=True, color="0F62FE", align="center")
        ],
        [
            p_multi_run([("Phase 4:\n", True), ("Enclosure & Pilot", False)]),
            p_xml("Dec 1 - Dec 21, 2026", align="center"),
            p_xml("Assemble IP65 stainless enclosure at tray return; conduct 14-day live campus pilot in student mess; log plate-waste reduction via nudge screen; dispatch compliant kitchen surplus; produce first batch of bio-fertilizer."),
            p_xml("PLANNED PILOT\n(Central Mess)", align="center")
        ],
        [
            p_multi_run([("Phase 5:\n", True), ("Impact & Closeout", False)]),
            p_xml("Dec 22 - Dec 31, 2026", align="center"),
            p_xml("Retrain Module 1 demand model on real pilot plate-waste logs; compute total kg rescued, kg bio-fertilizer harvested, methane avoided, and procurement ₹ saved. Submit final PDF report, PPT, and demo video."),
            p_xml("MILESTONE 2 GATE\n(End-Dec 2026)", bold=True, color="1B4D3E", align="center")
        ]
    ]
    body.append(table_xml(timeline_rows, [1800, 1600, 4600, 1500], header_bg="1B4D3E"))
    body.append(p_xml("", space_after_pt=10))
    
    # Summary note
    body.append(p_multi_run([
        ("Summary Note: ", True, False, "1B4D3E"),
        ("The project tracker and activity task breakdown are maintained dynamically in the collaborative Google Sheets register: ", False),
        ("PankhuriGovila_YIRP", True, False, "0F62FE"),
        (", shared with ", False),
        ("paramjeet@onemoneb.org", True),
        (". The Excel source file is available at ", False),
        ("PankhuriGovila_YIRP_Project_Tracker.xlsx", True),
        (".", False)
    ], space_after_pt=6))
    
    # Assemble document.xml
    doc_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" 
            xmlns:cx="http://schemas.microsoft.com/office/drawing/2014/chartex" 
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" 
            xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" 
            xmlns:v="urn:schemas-microsoft-com:vml" 
            xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" 
            xmlns:w10="urn:schemas-microsoft-com:office:word" 
            xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" 
            xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" 
            xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml" 
            xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" 
            xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" 
            xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml">
    <w:body>
        {''.join(body)}
        <w:sectPr>
            <w:pgSz w:w="11906" w:h="16838"/>
            <w:pgMar w:top="850" w:right="720" w:bottom="850" w:left="720" w:header="720" w:footer="720" w:gutter="0"/>
            <w:cols w:space="720"/>
            <w:docGrid w:linePitch="360"/>
        </w:sectPr>
    </w:body>
</w:document>"""
    return doc_xml

def create_docx(output_filename="Anna_Setu_Project_Brief_Timeline_and_Tracker.docx"):
    template_filename = "Anna-Setu_Project_Report.docx"
    new_doc_xml = generate_document_xml()
    
    with zipfile.ZipFile(template_filename, 'r') as zin:
        with zipfile.ZipFile(output_filename, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == "word/document.xml":
                    zout.writestr(item, new_doc_xml.encode('utf-8'))
                else:
                    zout.writestr(item, zin.read(item.filename))
                    
    print(f"Successfully generated editable DOCX: {output_filename}")

if __name__ == "__main__":
    create_docx("Anna_Setu_Project_Brief_Timeline_and_Tracker.docx")
    create_docx("PankhuriGovila_YIRP_Project_Brief_Timeline_and_Tracker.docx")
