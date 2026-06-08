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
REPO_LINK_LABEL = "overleaf-codex-kit en GitHub"
CONTENT_WIDTH = 7.25 * inch


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="GuideTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=21,
        leading=24,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="GuideSubtitle",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.7,
        leading=12,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#334155"),
        spaceAfter=9,
    )
)
styles.add(
    ParagraphStyle(
        name="GuideH2",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=12.8,
        leading=15,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=7,
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="GuideBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.9,
        leading=11.5,
        textColor=colors.HexColor("#1f2937"),
        spaceAfter=3,
    )
)
styles.add(
    ParagraphStyle(
        name="GuideBodyKeep",
        parent=styles["GuideBody"],
        keepWithNext=True,
    )
)
styles.add(
    ParagraphStyle(
        name="GuideList",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.8,
        leading=11.2,
        leftIndent=14,
        firstLineIndent=-10,
        textColor=colors.HexColor("#1f2937"),
        spaceAfter=2,
    )
)
styles.add(
    ParagraphStyle(
        name="GuideSmall",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=7.2,
        leading=8.8,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#64748b"),
    )
)
CODE_STYLE = ParagraphStyle(
    name="GuideCode",
    parent=styles["Code"],
    fontName="Courier",
    fontSize=7.1,
    leading=8.5,
    textColor=colors.HexColor("#111827"),
    wordWrap="CJK",
)


class CopyBadge(Flowable):
    """Small visual copy hint for code blocks."""

    def __init__(self) -> None:
        super().__init__()
        self.width = 50
        self.height = 14

    def draw(self) -> None:
        canvas = self.canv
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#0f172a"))
        canvas.setFillColor(colors.HexColor("#0f172a"))
        canvas.setLineWidth(0.95)
        canvas.roundRect(2, 3, 8, 9, 1.3, stroke=1, fill=0)
        canvas.roundRect(6, 6, 8, 9, 1.3, stroke=1, fill=0)
        canvas.setFont("Helvetica-Bold", 7.0)
        canvas.drawString(18, 4.0, "Copiar")
        canvas.restoreState()


def inline_markup(text: str) -> str:
    markdown_link_pattern = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
    parts = []
    cursor = 0
    for match in markdown_link_pattern.finditer(text):
        parts.append(html.escape(text[cursor : match.start()]))
        label = html.escape(match.group(1))
        url = html.escape(match.group(2), quote=True)
        parts.append(f'<link href="{url}"><u><font color="#2563eb">{label}</font></u></link>')
        cursor = match.end()
    parts.append(html.escape(text[cursor:]))
    text = "".join(parts)

    def angle_link(match: re.Match[str]) -> str:
        url = match.group(1)
        return f'<link href="{url}"><u><font color="#2563eb">{url}</font></u></link>'

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
    lines = [line for line in text.rstrip().splitlines() if line.strip()]
    header = Table(
        [[Paragraph("", styles["GuideSmall"]), CopyBadge()]],
        colWidths=[CONTENT_WIDTH - 0.72 * inch, 0.66 * inch],
        splitByRow=0,
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
    body_cells = [[Paragraph(f'<font name="Courier">{code_markup(line)}</font>', CODE_STYLE)] for line in lines]
    table = Table([[header], *body_cells], colWidths=[CONTENT_WIDTH], splitByRow=0)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("LINEBELOW", (0, 0), (-1, 0), 0.35, colors.HexColor("#e2e8f0")),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return table


def callout(text: str, bg: str = "#eff6ff", border: str = "#3b82f6") -> Table:
    table = Table([[Paragraph(inline_markup(text), styles["GuideBody"])]], colWidths=[CONTENT_WIDTH])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(bg)),
                ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor(border)),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
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
                story.append(Spacer(1, 0.04 * inch))
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
            story.append(callout(f"Repositorio del curso: [{REPO_LINK_LABEL}]({REPO_URL})"))
            story.append(Spacer(1, 0.06 * inch))
            first_heading = False
            continue

        if stripped.startswith("Repositorio del curso:"):
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

        label_style = "GuideBodyKeep" if stripped.endswith(":") else "GuideBody"
        story.append(Paragraph(inline_markup(stripped), styles[label_style]))

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
        rightMargin=0.55 * inch,
        leftMargin=0.55 * inch,
        topMargin=0.45 * inch,
        bottomMargin=0.55 * inch,
        title="Guia rapida Codex Overleaf Git",
        author="Curso IA - USFQ",
        subject="Instalacion de Overleaf Codex Kit",
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
