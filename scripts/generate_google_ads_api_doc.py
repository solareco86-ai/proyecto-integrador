#!/usr/bin/env python3
"""
Generador de documento PDF oficial para la solicitud de Basic Access de Google Ads API.
Genera 'DataMaq_Google_Ads_API_Tool_Documentation.pdf'.
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

OUTPUT_PATH = "/home/agustin/proyectos_software/www-datamaq/docs/DataMaq_Google_Ads_API_Tool_Documentation.pdf"


def generate_pdf():
    doc = SimpleDocTemplate(OUTPUT_PATH, pagesize=letter, rightMargin=45, leftMargin=45, topMargin=45, bottomMargin=45)

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=6,
    )

    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#475569"),
        spaceAfter=15,
    )

    h1_style = ParagraphStyle(
        "SectionH1",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#1e40af"),
        spaceBefore=12,
        spaceAfter=6,
    )

    body_style = ParagraphStyle(
        "BodyTextCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6,
    )

    bullet_style = ParagraphStyle("BulletCustom", parent=body_style, leftIndent=15, firstLineIndent=-10, spaceAfter=4)

    code_style = ParagraphStyle(
        "CodeStyle",
        parent=styles["Code"],
        fontName="Courier",
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        spaceBefore=4,
        spaceAfter=6,
    )

    story = []

    # Header
    story.append(Paragraph("Google Ads API — Tool Design & Architecture Documentation", title_style))
    story.append(
        Paragraph(
            "<b>Applicant Company:</b> DataMaq (https://datamaq.com.ar) &nbsp;|&nbsp; <b>Developer Token:</b> Basic Access Application &nbsp;|&nbsp; <b>Date:</b> August 2026",
            subtitle_style,
        )
    )
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563eb"), spaceAfter=12))

    # 1. Company Overview
    story.append(Paragraph("1. Company Overview & Business Model", h1_style))
    story.append(
        Paragraph(
            "<b>DataMaq</b> (https://datamaq.com.ar) is an industrial IoT, energy efficiency, and electrical telemetery engineering company based in Buenos Aires, Argentina. "
            "DataMaq installs hardware analyzers (Powermeter SmartPlus, IoT Gateways, and PLCs) in manufacturing facilities, helping PyMEs monitor energy consumption, eliminate reactive power penalties (cos &phi;), and avoid maximum demand surcharges.",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "<b>Business Model:</b> We operate under a field installation and engineering consulting model. Our cloud software platform is provided free ($0 SaaS) to our clients. Revenue is generated exclusively from professional technical installation services, energy diagnostics, and ISO 50001 consulting.",
            body_style,
        )
    )

    # 2. Tool Description
    story.append(Paragraph("2. Tool Description & Purpose", h1_style))
    story.append(
        Paragraph(
            "The tool being built is an <b>internal operational intelligence and budget-pacing monitor</b> (DataMaq Ads Auditor & MCP Tool). "
            "The tool connects exclusively to DataMaq's own Google Ads account to perform two core functions:",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "&bull; <b>Automated Budget Pacing & Overrun Prevention:</b> Checks current daily ad spend against an internal limit ($1,500 ARS/day) to ensure advertising campaigns stay within approved operational thresholds.",
            bullet_style,
        )
    )
    story.append(
        Paragraph(
            "&bull; <b>Search Terms & Keyword Quality Audit:</b> Analyzes real search queries from industrial users (e.g., 'multa factor de potencia', 'analizador de redes trifasico') to identify negative keywords and improve campaign quality scores.",
            bullet_style,
        )
    )
    story.append(
        Paragraph(
            "&bull; <b>Conversion Attribution Cross-Check:</b> Matches incoming B2B technical leads from our website contact forms with Google Ads click identifiers (GCLID) and UTM parameters.",
            bullet_style,
        )
    )

    # 3. Target Audience & Users
    story.append(Paragraph("3. Target Audience & User Access", h1_style))
    story.append(
        Paragraph(
            "<b>User Access:</b> <u>Internal Users Only (DataMaq employees / technical operators).</u><br/>"
            "The tool is strictly an internal administrative utility. It is not offered to third parties, clients, or the general public as a service. No external client accounts are managed or accessed through this developer token.",
            body_style,
        )
    )

    # 4. Architecture & Technical Design
    story.append(Paragraph("4. Architecture & Technical Design", h1_style))

    table_data = [
        [
            Paragraph("<b>Component</b>", body_style),
            Paragraph("<b>Technology / Implementation</b>", body_style),
            Paragraph("<b>Role / Function</b>", body_style),
        ],
        [
            Paragraph("Backend Core", body_style),
            Paragraph("Python 3.12+ / FastAPI / FastMCP", body_style),
            Paragraph("Executes internal queries and reporting tools via stdio / REST", body_style),
        ],
        [
            Paragraph("Authentication", body_style),
            Paragraph("OAuth 2.0 (Offline Refresh Token)", body_style),
            Paragraph("Secure token-based auth with Google Ads API v18+", body_style),
        ],
        [
            Paragraph("API Scope Used", body_style),
            Paragraph("https://www.googleapis.com/auth/adwords", body_style),
            Paragraph(
                "Strictly read-only reporting queries (SELECT from campaign, customer, search_term_view)", body_style
            ),
        ],
        [
            Paragraph("Security Storage", body_style),
            Paragraph("Local encrypted environment (.env)", body_style),
            Paragraph("Secrets, client ID, and refresh token never exposed to clients", body_style),
        ],
    ]
    t = Table(table_data, colWidths=[110, 180, 230])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(t)
    story.append(Spacer(1, 8))

    # 5. Data Flow & Security
    story.append(Paragraph("5. Data Flow & Privacy Compliance", h1_style))
    story.append(
        Paragraph(
            "1. The tool initiates a scheduled query using GoogleAdsClient with stored OAuth 2.0 refresh credentials.<br/>"
            "2. Google Ads API processes the query via GoogleAdsService.SearchStream (GAQL).<br/>"
            "3. Metrics (impressions, clicks, cost, conversions) are aggregated and checked against daily safety budgets.<br/>"
            "4. Data is displayed exclusively to internal operators. <b>No data is stored on public databases or shared with third parties.</b>",
            body_style,
        )
    )

    # 6. Sample Queries
    story.append(Paragraph("6. Sample GAQL Queries Executed by the Tool", h1_style))
    story.append(Paragraph("<b>Budget Pacing Query:</b>", body_style))
    story.append(
        Paragraph(
            "SELECT metrics.cost_micros, metrics.clicks FROM customer WHERE segments.date DURING TODAY", code_style
        )
    )
    story.append(Paragraph("<b>Campaign Performance Query:</b>", body_style))
    story.append(
        Paragraph(
            "SELECT campaign.id, campaign.name, metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions FROM campaign WHERE segments.date DURING LAST_7_DAYS",
            code_style,
        )
    )

    doc.build(story)
    print(f"✔ PDF generado exitosamente en: {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_pdf()
