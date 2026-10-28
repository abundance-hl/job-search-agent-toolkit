#!/usr/bin/env python3
"""Convert the documented Markdown resume format into searchable LaTeX output."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class Experience:
    company: str
    role: str
    location: str
    dates: str
    description: List[str]
    bullets: List[str]


def slugify(value: str) -> str:
    value = normalize_text(value).lower()
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def experience_id(item: Experience) -> str:
    employer = item.company.split(" - ", 1)[0]
    return f"{slugify(employer)}-{slugify(item.role)}"


def normalize_text(value: str) -> str:
    replacements = {
        "\u2010": "-",
        "\u2011": "-",
        "\u2012": "-",
        "\u2013": "-",
        "\u2014": "-",
        "\u2212": "-",
        "\u2192": "to",
        "\u00a0": " ",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    value = re.sub(r"\\([<>~\\-])", r"\1", value)
    return re.sub(r"[ \t]+", " ", value)


def latex_escape(value: str) -> str:
    value = normalize_text(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "<": r"\textless{}",
        ">": r"\textgreater{}",
        "|": r"\textbar{}",
    }
    return "".join(replacements.get(char, char) for char in value)


INLINE_TOKEN = re.compile(r"(\[[^\]]+\]\([^)]+\)|\*\*[^*]+\*\*|\*[^*]+\*)")


def latex_inline(value: str) -> str:
    parts: List[str] = []
    for token in INLINE_TOKEN.split(normalize_text(value)):
        if not token:
            continue
        link = re.fullmatch(r"\[([^\]]+)\]\(([^)]+)\)", token)
        if link:
            label, url = link.groups()
            safe_url = url.replace("%", r"\%").replace("#", r"\#")
            parts.append(r"\href{" + safe_url + "}{" + latex_escape(label) + "}")
        elif token.startswith("**") and token.endswith("**"):
            parts.append(r"\textbf{" + latex_escape(token[2:-2]) + "}")
        elif token.startswith("*") and token.endswith("*"):
            parts.append(r"\emph{" + latex_escape(token[1:-1]) + "}")
        else:
            parts.append(latex_escape(token))
    return "".join(parts)


def bold_line(line: str) -> str | None:
    match = re.fullmatch(r"\*\*(.+?)\*\*\s*", line.strip())
    return normalize_text(match.group(1)).strip() if match else None


def split_role(value: str) -> tuple[str, str, str]:
    left, separator, dates = value.rpartition(" | ")
    if not separator:
        return value, "", ""
    role, location_separator, location = left.rpartition(" - ")
    if not location_separator:
        return left, "", dates
    return role, location, dates


def parse_resume(source: Path) -> dict:
    lines = [line.rstrip().rstrip("  ") for line in source.read_text(encoding="utf-8").splitlines()]
    lines = [line for line in lines if not re.fullmatch(r"\s*<!--.*-->\s*", line)]
    lines = [line for line in lines if line.strip() != "---"]

    work_marker = lines.index("**WORK EXPERIENCE**")
    education_marker = lines.index("**EDUCATION**")
    header = [line.strip() for line in lines[:work_marker] if line.strip()]
    work = [line.strip() for line in lines[work_marker + 1 : education_marker] if line.strip()]
    education = [line.strip() for line in lines[education_marker + 1 :] if line.strip()]

    name = bold_line(header[0])
    if not name:
        raise ValueError("The first non-empty line must contain the name in bold Markdown.")
    contact_index = next((index for index, line in enumerate(header[1:], 1) if "@" in line and "|" in line), None)
    if contact_index is None:
        raise ValueError("Could not identify the contact line.")
    summary = " ".join(header[1:contact_index])
    contact = [part.strip() for part in header[contact_index].split("|")]

    experiences: List[Experience] = []
    index = 0
    while index < len(work):
        company = bold_line(work[index])
        if not company:
            raise ValueError(f"Expected a bold company name near: {work[index]}")
        index += 1
        if index >= len(work):
            raise ValueError(f"Missing role line after {company}")
        role_line = bold_line(work[index])
        if not role_line:
            raise ValueError(f"Expected a bold role line after {company}")
        role, location, dates = split_role(role_line)
        index += 1

        description: List[str] = []
        bullets: List[str] = []
        while index < len(work) and bold_line(work[index]) is None:
            if work[index].startswith("* "):
                bullets.append(work[index][2:].strip())
            else:
                description.append(work[index])
            index += 1
        experiences.append(Experience(company, role, location, dates, description, bullets))

    return {
        "name": name,
        "summary": summary,
        "contact": contact,
        "experiences": experiences,
        "education": education,
    }


def apply_profile(data: dict, profile: dict) -> tuple[dict, List[dict], dict | None]:
    source_by_id = {experience_id(item): item for item in data["experiences"]}
    if len(source_by_id) != len(data["experiences"]):
        raise ValueError("Experience IDs are not unique; company and role names must distinguish entries.")

    sections: List[dict] = []
    used_ids = set()
    for section in profile.get("sections", []):
        heading = section.get("heading", "").strip()
        if not heading:
            raise ValueError("Every profile section needs a heading.")
        entries: List[Experience] = []
        for spec in section.get("entries", []):
            item_id = spec.get("id")
            if item_id not in source_by_id:
                available = ", ".join(sorted(source_by_id))
                raise ValueError(f"Unknown experience ID '{item_id}'. Available IDs: {available}")
            if item_id in used_ids:
                raise ValueError(f"Experience ID '{item_id}' appears more than once in the profile.")
            used_ids.add(item_id)
            source = source_by_id[item_id]

            if "description_override" in spec:
                override = spec["description_override"]
                description = [override] if override else []
            elif spec.get("include_description", True):
                description = list(source.description)
            else:
                description = []

            if "bullets_override" in spec:
                bullets = list(spec["bullets_override"])
            elif "bullet_indexes" in spec:
                bullets = []
                for bullet_index in spec["bullet_indexes"]:
                    if not 0 <= bullet_index < len(source.bullets):
                        raise ValueError(
                            f"Bullet index {bullet_index} is invalid for '{item_id}', which has {len(source.bullets)} bullets."
                        )
                    bullets.append(source.bullets[bullet_index])
            else:
                bullets = list(source.bullets)

            entries.append(
                Experience(
                    company=source.company,
                    role=source.role,
                    location=source.location,
                    dates=source.dates,
                    description=description,
                    bullets=bullets,
                )
            )
        sections.append({"heading": heading, "experiences": entries})

    if not sections:
        raise ValueError("The profile must contain at least one experience section.")

    page_break = profile.get("page_break")
    if page_break:
        before_id = page_break.get("before_experience")
        after = page_break.get("after_bullet")
        if before_id and after:
            raise ValueError("A profile page break may use before_experience or after_bullet, not both.")
        if before_id and before_id not in used_ids:
            raise ValueError(f"Page break refers to unused experience ID '{before_id}'.")
        if after:
            after_id = after.get("experience")
            count = after.get("count")
            selected = next(
                (item for section in sections for item in section["experiences"] if experience_id(item) == after_id),
                None,
            )
            if selected is None:
                raise ValueError(f"Page break refers to unused experience ID '{after_id}'.")
            if not isinstance(count, int) or not 1 <= count < len(selected.bullets):
                raise ValueError("after_bullet count must leave at least one selected bullet on each page.")

    profiled_data = dict(data)
    profiled_data["summary"] = profile.get("summary", data["summary"])
    profiled_data["contact"] = profile.get("contact", data["contact"])
    contact_break_after = profile.get("contact_break_after")
    if contact_break_after is not None:
        if not isinstance(contact_break_after, int) or not 1 <= contact_break_after < len(profiled_data["contact"]):
            raise ValueError("contact_break_after must split the contact list into two non-empty lines.")
    profiled_data["contact_break_after"] = contact_break_after
    education_before_section = profile.get("education_before_section")
    if education_before_section is not None:
        section_headings = {section["heading"] for section in sections}
        if education_before_section not in section_headings:
            raise ValueError("education_before_section must match a profile section heading.")
    profiled_data["education_before_section"] = education_before_section
    profiled_data["font"] = profile.get("font", "TeX Gyre Termes")
    font_kerning = profile.get("font_kerning", "On")
    if font_kerning not in {"On", "Off"}:
        raise ValueError("font_kerning must be 'On' or 'Off'.")
    profiled_data["font_kerning"] = font_kerning
    profiled_data["pdf_subject"] = profile.get("pdf_subject", "")
    profiled_data["layout"] = profile.get("layout", {})
    return profiled_data, sections, page_break


def default_sections(data: dict) -> List[dict]:
    return [{"heading": "WORK EXPERIENCE", "experiences": data["experiences"]}]


def render_latex(data: dict, sections: List[dict], page_break: dict | None = None) -> str:
    layout = data.get("layout", {})
    font = data.get("font", "TeX Gyre Termes")
    # File-based selection lets Tectonic resolve its own font bundle on any OS.
    if font == "TeX Gyre Termes":
        font_setup = (
            r"\setmainfont{texgyretermes}[Extension=.otf,UprightFont=*-regular,"
            r"BoldFont=*-bold,ItalicFont=*-italic,BoldItalicFont=*-bolditalic,"
            r"Ligatures=TeX,Numbers=Lining,Kerning=@@FONTKERNING@@]"
        )
    else:
        font_setup = (
            r"\setmainfont{" + latex_escape(font)
            + r"}[Ligatures=TeX,Numbers=Lining,Kerning=@@FONTKERNING@@]"
        )

    def layout_value(name: str, default: float) -> str:
        value = float(layout.get(name, default))
        if value <= 0:
            raise ValueError(f"Layout value {name!r} must be positive.")
        return f"{value:g}"

    rendered_education = []
    for line in data["education"]:
        rendered = latex_inline(line)
        rendered = rendered.replace(
            r"\textbar{}} Extracurriculars:",
            r"}\linebreak Extracurriculars:",
        )
        rendered_education.append(r"\resumeEducation{" + rendered + "}")
    education_blocks = "\n\n".join(rendered_education)
    education_section = r"\section*{EDUCATION}" + "\n" + education_blocks

    section_blocks: List[str] = []
    for section in sections:
        if data.get("education_before_section") == section["heading"]:
            section_blocks.append(education_section)
        experience_blocks: List[str] = [r"\section*{" + latex_escape(section["heading"]) + "}"]
        for item in section["experiences"]:
            item_id = experience_id(item)
            if page_break and page_break.get("before_experience") == item_id:
                experience_blocks.append(r"\newpage")
            if item.location and item.dates:
                meta = latex_escape(item.location) + r" \textbar{} " + latex_escape(item.dates)
            elif item.dates:
                meta = latex_escape(item.dates)
            else:
                meta = latex_escape(item.location)
            lines = [
                r"\resumeCompany{" + latex_escape(item.company) + "}",
                r"\resumeRole{" + latex_escape(item.role) + "}{" + meta + "}",
            ]
            for paragraph in item.description:
                lines.append(r"\resumeDescription{" + latex_inline(paragraph) + "}")
            if item.bullets:
                lines.append(r"\begin{itemize}")
                for bullet_index, bullet in enumerate(item.bullets, 1):
                    lines.append(r"  \resumeItem{" + latex_inline(bullet) + "}")
                    if (
                        page_break
                        and page_break.get("after_bullet", {}).get("experience") == item_id
                        and page_break["after_bullet"].get("count") == bullet_index
                    ):
                        lines.extend(
                            [
                                r"\end{itemize}",
                                r"\newpage",
                                r"\resumeCompany{" + latex_escape(item.company) + r" (continued)}",
                                r"\resumeRole{" + latex_escape(item.role) + "}{" + meta + "}",
                                r"\begin{itemize}",
                            ]
                        )
                lines.append(r"\end{itemize}")
            experience_blocks.append("\n".join(lines))
        section_blocks.append("\n\n".join(experience_blocks))

    education_tail = "" if data.get("education_before_section") else education_section
    contact_parts = [latex_inline(part) for part in data["contact"]]
    contact_separator = r" \enspace\textbar\enspace "
    contact_break_after = data.get("contact_break_after")
    if contact_break_after:
        contact = (
            contact_separator.join(contact_parts[:contact_break_after])
            + r"\\ "
            + contact_separator.join(contact_parts[contact_break_after:])
        )
    else:
        contact = contact_separator.join(contact_parts)

    return TEMPLATE.replace("@@NAME@@", latex_escape(data["name"])) \
        .replace("@@FONTSETUP@@", font_setup) \
        .replace("@@FONTKERNING@@", data.get("font_kerning", "On")) \
        .replace("@@PDFSUBJECT@@", latex_escape(data.get("pdf_subject", ""))) \
        .replace("@@BODYFONT@@", layout_value("body_font_size", 11)) \
        .replace("@@BODYLEADING@@", layout_value("body_leading", 12.35)) \
        .replace("@@ITEMSEP@@", layout_value("item_sep", 1.2)) \
        .replace("@@ITEMTOPSEP@@", layout_value("item_top_sep", 1.6)) \
        .replace("@@SECTIONBEFORE@@", layout_value("section_before", 8)) \
        .replace("@@SECTIONAFTER@@", layout_value("section_after", 3)) \
        .replace("@@COMPANYVSPACE@@", layout_value("company_vspace", 6)) \
        .replace("@@DESCRIPTIONVSPACE@@", layout_value("description_vspace", 0.8)) \
        .replace("@@EDUCATIONVSPACE@@", layout_value("education_vspace", 3)) \
        .replace("@@SUMMARY@@", latex_inline(data["summary"])) \
        .replace("@@CONTACT@@", contact) \
        .replace("@@EXPERIENCE@@", "\n\n".join(section_blocks)) \
        .replace("@@EDUCATION_TAIL@@", education_tail)


TEMPLATE = r"""\documentclass[11pt,letterpaper]{article}
\usepackage[letterpaper,top=0.70in,bottom=0.70in,left=0.80in,right=0.80in]{geometry}
\usepackage{fontspec}
@@FONTSETUP@@
\usepackage{microtype}
\usepackage{enumitem}
\usepackage{needspace}
\usepackage{titlesec}
\usepackage{xcolor}
\usepackage[hidelinks]{hyperref}
\hypersetup{pdfsubject={@@PDFSUBJECT@@}}
\usepackage{ragged2e}

\definecolor{heading}{HTML}{17324D}
\pagestyle{empty}
\urlstyle{same}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0pt}
\hyphenpenalty=10000
\exhyphenpenalty=10000
\emergencystretch=2em
\setlist[itemize]{leftmargin=1.55em,label=\textbullet,itemsep=@@ITEMSEP@@pt,topsep=@@ITEMTOPSEP@@pt,parsep=0pt,partopsep=0pt}
\titleformat{\section}{\fontsize{13}{14}\selectfont\bfseries\color{heading}}{}{0pt}{}[\vspace{-2pt}\color{heading}\titlerule]
\titlespacing*{\section}{0pt}{@@SECTIONBEFORE@@pt}{@@SECTIONAFTER@@pt}

\newcommand{\resumeCompany}[1]{\Needspace{7\baselineskip}\vspace{@@COMPANYVSPACE@@pt}{\fontsize{12}{13}\selectfont\bfseries\color{heading}#1}\par}
\newcommand{\resumeRole}[2]{{\fontsize{10}{11.2}\selectfont\textbf{#1}\hfill\textbf{#2}}\par}
\newcommand{\resumeDescription}[1]{\vspace{@@DESCRIPTIONVSPACE@@pt}#1\par}
\newcommand{\resumeEducation}[1]{\vspace{@@EDUCATIONVSPACE@@pt}#1\par}
\newcommand{\resumeItem}[1]{\Needspace{3\baselineskip}\item #1}

\begin{document}
\RaggedRight
\fontsize{@@BODYFONT@@}{@@BODYLEADING@@}\selectfont

{\fontsize{17}{19}\selectfont\bfseries\color{heading} @@NAME@@}\par
\vspace{7pt}

{\fontsize{12}{13.4}\selectfont @@SUMMARY@@}\par
\vspace{7pt}

{\fontsize{10.5}{12}\selectfont @@CONTACT@@}\par
\vspace{2pt}

@@EXPERIENCE@@

@@EDUCATION_TAIL@@

\end{document}
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--tex", type=Path, required=True)
    parser.add_argument("--profile", type=Path, help="JSON profile controlling summary, sections, and bullet selection.")
    parser.add_argument(
        "--split-experience",
        metavar="EXPERIENCE:BULLETS",
        help="Start page two after this many bullets in a zero-based experience entry.",
    )
    args = parser.parse_args()

    data = parse_resume(args.source)
    sections = default_sections(data)
    page_break = None
    if args.profile:
        profile = json.loads(args.profile.read_text(encoding="utf-8"))
        data, sections, page_break = apply_profile(data, profile)
    if args.split_experience:
        try:
            experience_index, bullet_count = (int(value) for value in args.split_experience.split(":"))
        except (TypeError, ValueError) as error:
            raise SystemExit("--split-experience must look like EXPERIENCE:BULLETS, for example 2:4") from error
        if not 0 <= experience_index < len(data["experiences"]):
            raise SystemExit("--split-experience refers to an experience that does not exist")
        bullets = data["experiences"][experience_index].bullets
        if not 1 <= bullet_count < len(bullets):
            raise SystemExit("The split must leave at least one bullet on each page")
        page_break = {
            "after_bullet": {
                "experience": experience_id(data["experiences"][experience_index]),
                "count": bullet_count,
            }
        }
    args.tex.parent.mkdir(parents=True, exist_ok=True)
    args.tex.write_text(render_latex(data, sections, page_break), encoding="utf-8")
    print(f"Wrote {args.tex}")


if __name__ == "__main__":
    main()
