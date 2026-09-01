"""
EcoLoop AI — Markdown to PDF Converter
Renders docs/HONEYWELL_ECOLOOP_AI_PROPOSAL.md into styled PDF document.
"""

from pathlib import Path
from fpdf import FPDF

PROJECT_ROOT = Path(__file__).resolve().parent
MD_PATH = PROJECT_ROOT / "docs" / "HUMANIZED_ECOLOOP_PROPOSAL.md"
PDF_PATH = PROJECT_ROOT / "HONEYWELL_ECOLOOP_AI_PROPOSAL.pdf"
DOCS_PDF_PATH = PROJECT_ROOT / "docs" / "HONEYWELL_ECOLOOP_AI_PROPOSAL.pdf"


def sanitize(text: str) -> str:
    """
    Replaces unicode symbols with Latin-1 safe ASCII equivalents for FPDF.
    """
    replacements = {
        "—": "-",
        "–": "-",
        "°": " deg ",
        "±": "+/-",
        "²": "2",
        "³": "3",
        "≥": ">=",
        "≤": "<=",
        "→": "->",
        "←": "<-",
        "’": "'",
        "‘": "'",
        "“": '"',
        "”": '"',
        "•": "*",
        "💡": "[Idea]",
        "❌": "[X]",
        "⚡": "[Energy]",
        "🧘": "[Comfort]",
        "💰": "[Cost]",
        "🌿": "[Carbon]",
        "🏢": "[Building]",
        "🤖": "[AI]",
        "📈": "[Graph]",
        "📊": "[Chart]",
        "🧪": "[Test]",
        "🛠️": "[Tools]",
        "🚀": "[Launch]",
        "📥": "[Export]",
        "🛡️": "[Security]",
        "⚙️": "[Config]",
        "🕹️": "[Control]"
    }
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)
    # Strip any remaining non-latin1 characters safely
    return text.encode("latin-1", "replace").decode("latin-1")


class ProposalPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(180, 180, 180)
        self.cell(0, 10, sanitize("Honeywell Hackathon - EcoLoop AI Project Proposal"), border=0, new_x="RIGHT", new_y="TOP", align="R")
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}", border=0, new_x="RIGHT", new_y="TOP", align="C")


def generate_pdf():
    pdf = ProposalPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_margins(15, 15, 15)

    with open(MD_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        raw_line = sanitize(line.strip())
        if not raw_line:
            pdf.ln(3)
            continue

        # Header 1 (# Honeywell)
        if raw_line.startswith("# Honeywell"):
            pdf.set_font("Helvetica", "B", 24)
            pdf.set_text_color(220, 20, 20)  # Honeywell Red
            pdf.cell(0, 14, "Honeywell", border=0, new_x="LMARGIN", new_y="NEXT", align="C")
            pdf.ln(2)

        # Header 2 (## Title / Sections)
        elif raw_line.startswith("## "):
            text = raw_line.replace("## ", "").replace("**", "")
            pdf.set_font("Helvetica", "B", 14)
            pdf.set_text_color(180, 0, 0)
            pdf.cell(0, 9, text, border=0, new_x="LMARGIN", new_y="NEXT")
            pdf.set_draw_color(220, 20, 20)
            pdf.set_line_width(0.5)
            pdf.line(15, pdf.get_y(), 195, pdf.get_y())
            pdf.ln(4)

        # Header 3 (### Subsections)
        elif raw_line.startswith("### "):
            text = raw_line.replace("### ", "").replace("**", "")
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(40, 40, 40)
            pdf.cell(0, 7, text, border=0, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)

        # Bullet points
        elif raw_line.startswith("- ") or raw_line.startswith("* "):
            text = raw_line.lstrip("- *").strip().replace("**", "")
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(50, 50, 50)
            pdf.multi_cell(0, 5, f"  *  {text}", new_x="LMARGIN", new_y="NEXT")

        # Code blocks or ASCII diagrams
        elif raw_line.startswith("```") or raw_line.startswith("+--") or raw_line.startswith("|"):
            pdf.set_font("Courier", "", 8)
            pdf.set_text_color(30, 30, 90)
            pdf.multi_cell(0, 4, raw_line.replace("```python", "").replace("```", ""), new_x="LMARGIN", new_y="NEXT")

        # Key metadata lines
        elif "Author:" in raw_line or "Candidate ID:" in raw_line or "Mail ID:" in raw_line or "Project Title:" in raw_line:
            clean = raw_line.replace("**", "")
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(180, 20, 20)
            pdf.cell(0, 7, clean, border=0, new_x="LMARGIN", new_y="NEXT", align="C")

        # Regular paragraph text
        else:
            clean_text = raw_line.replace("**", "").replace("`", "")
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(40, 40, 40)
            pdf.multi_cell(0, 5, clean_text, new_x="LMARGIN", new_y="NEXT")

    pdf.output(str(PDF_PATH))
    pdf.output(str(DOCS_PDF_PATH))
    print(f"Successfully generated PDF at:\n -> {PDF_PATH}\n -> {DOCS_PDF_PATH}")


if __name__ == "__main__":
    generate_pdf()
