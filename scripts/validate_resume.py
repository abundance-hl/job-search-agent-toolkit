#!/usr/bin/env python3
"""Check that a generated resume PDF remains searchable and structurally intact."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

import pdfplumber
from pypdf import PdfReader


def load_expected(path: Path | None) -> list[str]:
    """Read caller-selected extraction checks, never a particular person's facts."""
    if path is None:
        return []
    phrases = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(phrases, list) or not all(isinstance(item, str) and item.strip() for item in phrases):
        raise ValueError("Expected text must be a JSON array of non-empty strings.")
    return phrases


def normalize_extracted_text(value: str) -> str:
    """Allow typeset quote substitutions while keeping word boundaries significant."""
    return re.sub(r"\s+", " ", value).translate(str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"'}))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--text-output", type=Path)
    parser.add_argument("--expected", type=Path, help="JSON array of text that must survive PDF extraction.")
    args = parser.parse_args()

    reader = PdfReader(args.pdf)
    page_text = [(page.extract_text() or "").strip() for page in reader.pages]
    text = "\n\n".join(page_text)
    normalized_text = normalize_extracted_text(text)
    font_size_characters: Counter[float] = Counter()

    def record_font_size(
        fragment: str,
        _current_transform: list[float],
        _text_matrix: list[float],
        _font: dict | None,
        font_size: float,
    ) -> None:
        visible_characters = len(fragment.strip())
        if visible_characters:
            font_size_characters[round(float(font_size), 2)] += visible_characters

    for page in reader.pages:
        page.extract_text(visitor_text=record_font_size)

    dominant_font_size = font_size_characters.most_common(1)[0][0] if font_size_characters else 0.0
    missing = [phrase for phrase in load_expected(args.expected) if normalize_extracted_text(phrase) not in normalized_text]
    suspicious = re.findall(r"[\ufffd\u25a0]", text)

    if args.text_output:
        args.text_output.parent.mkdir(parents=True, exist_ok=True)
        args.text_output.write_text(text + "\n", encoding="utf-8")

    print(f"Pages: {len(reader.pages)}")
    print(f"Extracted characters: {len(text)}")
    print(f"Dominant font size: {dominant_font_size:.2f} pt")
    if any(not page for page in page_text):
        raise SystemExit("Resume contains an empty or non-searchable page.")
    if missing:
        raise SystemExit("Missing expected extracted text: " + ", ".join(missing))
    if suspicious:
        raise SystemExit("Extracted text contains replacement or black-square glyphs.")
    if not 1 <= len(reader.pages) <= 2:
        raise SystemExit("Resume should be one or two pages.")
    if dominant_font_size < 10.5:
        raise SystemExit("Dominant resume text must be at least 10.5 pt for readability.")
    if len(reader.pages) == 2:
        with pdfplumber.open(args.pdf) as pdf:
            first_page_characters = [
                character
                for character in pdf.pages[0].chars
                if character.get("text", "").strip()
            ]
        first_page_bottom = max(
            (float(character["bottom"]) for character in first_page_characters),
            default=0.0,
        )
        print(f"First-page text bottom: {first_page_bottom:.1f} pt")
        if first_page_bottom < 575.0:
            raise SystemExit(
                "First page is underfilled; remove or move the manual page break before delivery."
            )
    print("Text extraction check: PASS")
    print("This checks PDF structure and readability, not factual accuracy or an ATS score.")


if __name__ == "__main__":
    main()
