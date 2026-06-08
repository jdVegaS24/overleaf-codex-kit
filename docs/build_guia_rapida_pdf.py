#!/usr/bin/env python3
"""Build the quick-start PDF guide from the Markdown source."""

from __future__ import annotations

import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Flowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "guia-rapida-overleaf-codex.md"
OUTPUT = ROOT / "guia-rapida-overleaf-codex.pdf"
REPO_URL = "https://github.com/jdVegaS24/overleaf-codex-kit"


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="GuideTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=29,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=12,
    )
)
styles.add(
    ParagraphStyle(
        name="GuideSubtitle",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=11.2,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#334155"),
        spaceAfter=16,
    )
)
styles.add(
    ParagraphStyle(
        name="GuideH2",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=12,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="GuideBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=13.5,
        textColor=colors.HexColor("#1f2937"),
        spaceAfter=5,
    )
)
styles.add(
    ParagraphStyle(
        name="GuideList",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.8,
        leading=13.2,
        leftIndent=14,
        firstLineIndent=-10,
        textColor=colors.HexColor("#1f2937"),
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="GuideSmall",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#64748b"),
    )
)
CODE_STYLE = ParagraphStyle(
    name="GuideCode",
    parent=styles["Code"],
    fontName="Courier",
    fontSize=8.0,
    leading=9.8,
    textColor=colors.HexColor("#111827"),
    wordWrap="CJK",
)


class CopyBadge(Flowable):
    """Small visual copy hint for code blocks."""

    def __init__(self) -> None:
        super().__init__()
        self.width = 54
        self.height = 14

    def draw(self) -> None:
        canvas = self.canv
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#64748b"))
        canvas.setFillColor(colors.HexColor("#64748b"))
        canvas.setLineWidth(0.7)
        canvas.roundRect(2, 4, 7, 8, 1.2, stroke=1, fill=0)
        canvas.roundRect(5, 6, 7, 8, 1.2, stroke=1, fill=0)
        canvas.setFont("Helvetica", 7.3)
        canvas.drawString(17, 4.7, "copiar")
        canvas.restoreState()


def inline_markup(text: str) -> str:
    text = html.escape(text)

    def angle_link(match: re.Match[str]) -> str:
        url = match.group(1)
        return f'<link href="{url}"><font color="#2563eb">{url}</font></link>'

    text = re.sub(r"&lt;(https?://[^&]+)&gt;", angle_link, text)
    text = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    return text


def code_markup(text: str) -> str:
    lines = []
    for line in text.rstrip().splitlines():
        leading = len(line) - len(line.lstrip(" "))
        prefix = "&nbsp;" * leading
        body = html.escape(line[leading:])
        lines.append(prefix + body)
    return "<br/>".join(lines)


def code_block(text: str) -> Table:
    header = Table(
        [[Paragraph("Comando", styles["GuideSmall"]), CopyBadge()]],
        colWidths=[5.62 * inch, 0.65 * inch],
    )
    header.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    body = Paragraph(f'<font name="Courier">{code_markup(text)}</font>', CODE_STYLE)
    table = Table([[header], [body]], colWidths=[6.27 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("LINEBELOW", (0, 0), (-1, 0), 0.35, colors.HexColor("#e2e8f0")),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def callout(text: str, bg: str = "#eff6ff", border: str = "#3b82f6") -> Table:
    table = Table([[Paragraph(inline_markup(text), styles["GuideBody"])]], colWidths=[6.45 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(bg)),
                ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor(border)),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return table


def parse_markdown(text: str) -> list:
    story: list = []
    lines = text.splitlines()
    in_code = False
    code_lines: list[str] = []
    first_heading = True

    for line in lines:
        if line.startswith("```"):
            if in_code:
                story.append(code_block("\n".join(code_lines)))
                story.append(Spacer(1, 0.08 * inch))
                code_lines = []
                in_code = False
            else:
                in_code = True
            continue

        if in_code:
            code_lines.append(line)
            continue

        stripped = line.strip()
        if not stripped:
            continue

        if stripped.startswith("# "):
            title = stripped[2:]
            story.append(Paragraph(inline_markup(title), styles["GuideTitle"]))
            story.append(
                Paragraph(
                    "Pasos minimos para instalar la skill en Codex, conectar Overleaf por Git y recompilar los cambios.",
                    styles["GuideSubtitle"],
                )
            )
            story.append(callout(f"Repositorio del curso: <{REPO_URL}>"))
            story.append(Spacer(1, 0.12 * inch))
            first_heading = False
            continue

        if stripped == f"Repositorio del curso: <{REPO_URL}>":
            continue

        if stripped.startswith("## "):
            heading = stripped[3:]
            story.append(Paragraph(inline_markup(heading), styles["GuideH2"]))
            continue

        ordered = re.match(r"^(\d+)\.\s+(.*)$", stripped)
        if ordered:
            number, item = ordered.groups()
            story.append(Paragraph(f"{number}. {inline_markup(item)}", styles["GuideList"]))
            continue

        if stripped.startswith("- "):
            story.append(Paragraph(f"&#8226; {inline_markup(stripped[2:])}", styles["GuideList"]))
            continue

        if stripped.startswith("Importante:"):
            story.append(callout(stripped, "#fefce8", "#eab308"))
            continue

        if stripped.startswith("Usar un flujo simple:"):
            story.append(callout(stripped, "#ecfdf5", "#10b981"))
            continue

        story.append(Paragraph(inline_markup(stripped), styles["GuideBody"]))

    if first_heading:
        story.insert(0, Paragraph("Guia rapida: Codex + Overleaf + Git", styles["GuideTitle"]))
    return story


def footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#64748b"))
    canvas.drawCentredString(
        letter[0] / 2,
        0.42 * inch,
        f"Overleaf Codex Kit | {REPO_URL} | pagina {doc.page}",
    )
    canvas.restoreState()


def main() -> int:
    story = parse_markdown(SOURCE.read_text(encoding="utf-8"))
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=letter,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.58 * inch,
        bottomMargin=0.68 * inch,
        title="Guia rapida Codex Overleaf Git",
        author="Curso IA - USFQ",
        subject="Instalacion de Overleaf Codex Kit",
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
