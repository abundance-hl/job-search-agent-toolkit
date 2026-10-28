#!/usr/bin/env python3
"""Render the workspace's simple Markdown cover-letter format to a polished PDF."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def clean_markdown(text: str) -> str:
    text = re.sub(r"^# .+?\n+", "", text, count=1)
    text = re.sub(r"^Status:.*?\n+", "", text, count=1, flags=re.MULTILINE)
    text = text.replace("  \n", "\n")
    return text.strip()


def escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--title", required=True)
    parser.add_argument("--name", required=True, help="Applicant name shown in the header and PDF metadata.")
    parser.add_argument("--contact", required=True, help="Contact line shown in the header; plain text only.")
    args = parser.parse_args()

    font_regular = "/System/Library/Fonts/Supplemental/Arial.ttf"
    font_bold = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
    if Path(font_regular).exists() and Path(font_bold).exists():
        pdfmetrics.registerFont(TTFont("LetterArial", font_regular))
        pdfmetrics.registerFont(TTFont("LetterArialBold", font_bold))
        regular, bold = "LetterArial", "LetterArialBold"
    else:
        regular, bold = "Helvetica", "Helvetica-Bold"

    lines = clean_markdown(args.source.read_text(encoding="utf-8")).splitlines()
    blocks: list[str] = []
    current: list[str] = []
    for line in lines:
        if line.strip():
            current.append(line.strip())
        elif current:
            blocks.append("<br/>".join(escape(item) for item in current))
            current = []
    if current:
        blocks.append("<br/>".join(escape(item) for item in current))

    styles = getSampleStyleSheet()
    body = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName=regular,
        fontSize=10.8,
        leading=15.1,
        textColor=HexColor("#111111"),
        alignment=TA_LEFT,
        spaceAfter=9,
    )
    name = ParagraphStyle(
        "Name",
        parent=body,
        fontName=bold,
        fontSize=16,
        leading=19,
        textColor=HexColor("#17324D"),
        spaceAfter=3,
    )
    contact = ParagraphStyle(
        "Contact",
        parent=body,
        fontSize=9.5,
        leading=12,
        textColor=HexColor("#333333"),
        spaceAfter=16,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(args.output),
        pagesize=letter,
        rightMargin=0.82 * inch,
        leftMargin=0.82 * inch,
        topMargin=0.72 * inch,
        bottomMargin=0.72 * inch,
        title=args.title,
        author=args.name,
        subject="Draft - needs applicant review",
        creator="Codex",
    )
    story = [
        Paragraph(escape(args.name), name),
        Paragraph(escape(args.contact), contact),
    ]
    for index, block in enumerate(blocks):
        story.append(Paragraph(block, body))
        if index == 1:
            story.append(Spacer(1, 3))
    doc.build(story)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
