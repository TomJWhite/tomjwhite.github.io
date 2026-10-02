"""Build Tom White's ATS-readable two-page CV PDF."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "Tom_White_C.V.pdf"

INK = colors.HexColor("#24313A")
MUTED = colors.HexColor("#59656E")
DEEP = colors.HexColor("#16485D")
ACCENT = colors.HexColor("#A94828")
LINE = colors.HexColor("#D8DFE2")

PAGE_WIDTH, PAGE_HEIGHT = A4
LEFT = 16 * mm
RIGHT = 16 * mm
TOP = 13 * mm
BOTTOM = 14 * mm


class CVDocument(BaseDocTemplate):
    def __init__(self, filename: str):
        super().__init__(
            filename,
            pagesize=A4,
            leftMargin=LEFT,
            rightMargin=RIGHT,
            topMargin=TOP,
            bottomMargin=BOTTOM,
            title="Tom White - Curriculum Vitae",
            author="Tom White",
            subject="Technical business analysis, systems, data and solution delivery",
            keywords="technical business analyst, systems analysis, solution delivery, RFI, RFP, vendor assessment, AI, Copilot, ChatGPT, GTFS, SQL, Python, Azure DevOps",
        )
        frame = Frame(
            LEFT,
            BOTTOM,
            PAGE_WIDTH - LEFT - RIGHT,
            PAGE_HEIGHT - TOP - BOTTOM,
            id="content",
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
        )
        self.addPageTemplates(PageTemplate(id="cv", frames=[frame], onPage=self._draw_page))

    def _draw_page(self, canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.5)
        canvas.line(LEFT, 9.5 * mm, PAGE_WIDTH - RIGHT, 9.5 * mm)
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 7.4)
        footer = f"Tom White  |  tomjwhite.github.io  |  Page {doc.page} of 2"
        footer_width = stringWidth(footer, "Helvetica", 7.4)
        canvas.drawString((PAGE_WIDTH - footer_width) / 2, 5.5 * mm, footer)
        canvas.restoreState()


styles = getSampleStyleSheet()
name_style = ParagraphStyle(
    "Name",
    parent=styles["Heading1"],
    fontName="Helvetica-Bold",
    fontSize=24,
    leading=25,
    textColor=DEEP,
    spaceAfter=2,
)
headline_style = ParagraphStyle(
    "Headline",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=10.2,
    leading=12,
    textColor=INK,
    spaceAfter=4,
)
contact_style = ParagraphStyle(
    "Contact",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.2,
    leading=10,
    textColor=MUTED,
    spaceAfter=8,
)
section_style = ParagraphStyle(
    "Section",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=11.2,
    leading=13,
    textColor=DEEP,
    spaceBefore=8,
    spaceAfter=4,
    keepWithNext=True,
)
body_style = ParagraphStyle(
    "Body",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=8.45,
    leading=10.55,
    textColor=INK,
    spaceAfter=3,
)
capability_style = ParagraphStyle(
    "Capability",
    parent=body_style,
    fontSize=8.1,
    leading=10.1,
    spaceAfter=2,
)
role_style = ParagraphStyle(
    "Role",
    parent=styles["Heading3"],
    fontName="Helvetica-Bold",
    fontSize=9.5,
    leading=11.2,
    textColor=DEEP,
    spaceBefore=3,
    spaceAfter=1,
    keepWithNext=True,
)
meta_style = ParagraphStyle(
    "Meta",
    parent=body_style,
    fontName="Helvetica-Bold",
    fontSize=7.7,
    leading=9.2,
    textColor=MUTED,
    spaceAfter=3,
    keepWithNext=True,
)
bullet_style = ParagraphStyle(
    "Bullet",
    parent=body_style,
    leftIndent=9,
    firstLineIndent=-7,
    bulletIndent=0,
    spaceAfter=2.2,
)
project_style = ParagraphStyle(
    "Project",
    parent=role_style,
    fontSize=9.1,
    leading=10.5,
    spaceBefore=3,
)
small_style = ParagraphStyle(
    "Small",
    parent=body_style,
    fontSize=7.9,
    leading=9.5,
)


def paragraph(text: str, style=body_style):
    return Paragraph(text, style)


def section(title: str):
    return [
        Paragraph(title.upper(), section_style),
        HRFlowable(width="100%", thickness=0.65, color=LINE, spaceAfter=4),
    ]


def bullet(text: str):
    return Paragraph(f"- {text}", bullet_style)


def role(title: str, organisation: str, dates: str, location: str = "Auckland, New Zealand"):
    return [
        Paragraph(f"{organisation} - {title}", role_style),
        Paragraph(f"{dates}  |  {location}", meta_style),
    ]


story = [
    Paragraph("Tom White", name_style),
    Paragraph("TECHNICAL BUSINESS ANALYST  |  SYSTEMS, DATA &amp; SOLUTION DELIVERY", headline_style),
    Paragraph(
        'Auckland, New Zealand  |  021 446 849  |  <a href="mailto:tomjwhite@outlook.com" color="#A94828">tomjwhite@outlook.com</a>  |  '
        '<a href="https://www.linkedin.com/in/thomasjacksonwhite/" color="#A94828">LinkedIn</a>  |  '
        '<a href="https://tomjwhite.github.io/" color="#A94828">Portfolio</a>',
        contact_style,
    ),
]

story += section("Profile")
story.append(
    paragraph(
        "Business analyst with a technical background spanning systems, data, software delivery, and operational change. "
        "At Auckland Transport, I coordinate complex timetable and network changes, validate public transport data across connected systems, and work with internal teams and technology vendors to resolve issues before they affect customer information. "
        "I use SQL, Python, and AI-assisted workflows to investigate problems, automate manual processes, and build practical tools where existing approaches fall short. "
        "I am looking to take the next step into a role with greater ownership of technical solutions, integrations, platforms, or implementations."
    )
)

story += section("Core capabilities")
story.extend(
    [
        paragraph("<b>Solution &amp; systems:</b> Systems analysis | Downstream impact analysis | Data flows and dependencies | Technical problem solving | Technical requirements | Solution options | Integration support | Data quality and reliability", capability_style),
        paragraph("<b>Delivery &amp; implementation:</b> Release and change coordination | Acceptance criteria | Testing and UAT | Workflow redesign and automation | Cross-functional technical delivery | Vendor liaison | RFI/RFP support and vendor assessment", capability_style),
        paragraph("<b>Tools &amp; platforms:</b> SQL | Python | Excel | Power BI | GTFS | IVU.plan | Azure DevOps | Visio | Microsoft 365 Copilot | ChatGPT | Claude | Gemini | Codex | TypeScript / React (project experience)", capability_style),
    ]
)

story += section("Professional experience")
story += role(
    "Business Analyst, Public Transport Data & Customer Information",
    "Auckland Transport",
    "May 2022 - Present",
)
story.extend(
    [
        bullet("Drive and coordinate the end-to-end change process for monthly timetable and network releases through Azure DevOps, aligning requirements, dependencies, testing, vendor activity, and release evidence from small metadata corrections to major service changes."),
        bullet("Act as subject matter expert for public transport schedule datasets and the IVU scheduling platform, helping protect accurate customer information across AT Mobile, Google Maps, operational tools, and the enterprise data warehouse."),
        bullet("Lead technical validation with SQL, Excel, and Python across GTFS datasets; clarify expected system behaviour, develop test cases, coordinate UAT, and investigate data or software-dependent issues before release."),
        bullet("Serve as primary liaison with IVU Traffic Technologies for configuration, upgrades, issue resolution, and service performance, translating operational needs and observed behaviour into actionable technical outcomes."),
        bullet("Contribute to RFI and RFP processes for product procurement and vendor assessment, helping define requirements, evaluate responses, and document findings for decision-makers."),
        bullet("Identify cross-system dependencies and downstream impacts across operations, product, data, software, and vendor processes, bringing the right teams together to resolve delivery risks."),
        bullet("Built Python and SQL workflows, using AI-assisted development, to load GTFS feeds into SQL and generate tester-ready outputs, reducing reliance on slower manual preparation; later extended ingestion to work directly from web links."),
        bullet("Conduct service reviews and process mapping, support business cases, and evaluate future capability options; provide SME input to National Ticketing, City Rail Link, and Community Connect / OpenLoop."),
        bullet("Work with external developers on data-publishing services and integrations, contributing schedule-data context to solution and delivery decisions."),
    ]
)

story.append(PageBreak())

story += section("Earlier experience")
story += role("Analyst", "Retail Performance", "September 2016 - November 2021")
story.extend(
    [
        bullet("Converted mystery-shopping and market-research data into client-ready findings, recommendations, executive summaries, graphs, and written commentary for non-technical audiences."),
        bullet("Designed and maintained web-based forms and data-collection structures to improve consistency, reporting quality, and downstream analysis."),
        bullet("Worked directly with remote clients to clarify problems, explain evidence, and turn analysis into practical action."),
    ]
)
story += role("Web Administrator", "Digital Works", "January 2016 - September 2016")
story.append(
    bullet("Produced customer-focused, SEO-aware content and supported web administration, analytics, and content maintenance for client sites.")
)

story += section("Selected projects")
story.append(Paragraph("Reconcile GTFS Comparator  |  Independent product", project_style))
story.extend(
    [
        bullet("Identified that conventional GTFS file comparison obscures meaningful service changes, then designed and built a browser-based tool that separates genuine timetable and network changes from routine feed churn."),
        bullet("Defined the comparison logic, user workflows, evidence model, and outputs across routes, stops, trips, and shapes, with local processing to protect source data."),
        bullet("Took the product from problem definition through design, implementation, testing, iteration, and deployment, using AI-assisted development while retaining ownership of product decisions, acceptance criteria, and quality."),
    ]
)
story.append(Paragraph("Blake Twigden Artist Website  |  Client product delivery", project_style))
story.append(
    bullet("Shaped and shipped the official six-page portfolio site for a New Zealand artist, taking responsibility for content structure, accessible gallery interactions, responsive delivery, SEO foundations, and a secure contact workflow.")
)
story.append(Paragraph("Copilot-based ITIL Study Agent  |  Applied AI", project_style))
story.append(
    bullet("Built a source-grounded assistant using ITIL training material, notes, and sample exams to generate practice questions, assess answers, and reference the supporting material.")
)

story += section("Education & professional development")
story.extend(
    [
        Paragraph("Bachelor of Computer and Information Sciences - Auckland University of Technology (2015)", role_style),
        paragraph("Double Major: Software Development and IT Service Science", small_style),
        paragraph("<b>ITIL 4 Foundation</b> - PeopleCert (2026)  |  <b>Project Management Essentials (PMBOK)</b> - Lumify (2024)  |  <b>Data Analyst in Python / SQL</b> - Dataquest (2020)", small_style),
        paragraph("Ongoing self-directed development in AI, LLM workflows, automation, and modern digital delivery.", small_style),
    ]
)

def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    document = CVDocument(str(OUTPUT))
    document.build(story)
    print(f"Built {OUTPUT}")


if __name__ == "__main__":
    build()
