---
name: resume-tailor
description: Tailor a truthful resume and cover-letter draft to a sourced job posting, build the resume PDF, and check its extracted text and rendered pages. Use when drafting or revising application documents.
---

# Resume tailoring

Read the repository's `AGENTS.md`, `private/master-resume.md`, and the target role's job description, fit analysis, and sources. The repository root is three directories above this skill folder. Read [the source/profile format](../../../docs/resume-format.md) before editing a profile or building, and [the workflow guide](../../../docs/workflow.md) for artifact locations.

All output is a draft for the user. Never apply, upload to an employer, fill a live application, send correspondence, or issue connection requests. Browser research is read-only. Keep personal work under `private/` and generated outputs in ignored build/output directories.

## Establish the evidence

The user's factual master is authoritative. Samples under `examples/sample-candidate/` illustrate layout and selection only; their generic employment, skills, achievements, and metrics are not facts about this user. Start from the user's own profile if available, or adapt `templates/profile.json` to IDs parsed from their master.

Refresh time-sensitive posting details before finalizing a draft. If the master lacks evidence for an appealing requirement, omit that claim and record the gap. Ask a focused question only when the missing fact materially affects the document. Record newly supplied facts with their source before using them; do not silently promote speculation into the master.

## Draft and build

1. Save the role-specific source as `private/jobs/<company-slug>/<role-slug>/resume.md` and its copied/adapted profile as `resume-profile.json`. Keep the reusable master and profile stable unless the user requests a correction.
2. Lead with the strongest supported evidence. Reorder, condense, and rephrase without changing titles, dates, scope, ownership, or metric qualifiers. Do not relabel transferable work as direct tenure, add unsupported tools, or imply direct code authorship for AI-assisted work.
3. Use only visible text. No hidden keywords, invisible text, or screening-system instructions. Adjust content and deliberate page breaks before shrinking typography.
4. Generate the PDF using the commands in `docs/resume-format.md`. Source Markdown and profile JSON are the editable inputs; generated LaTeX is disposable.
5. Run the extraction/readability validator, using expected phrases chosen from the final source. Render every PDF page and visually inspect layout, clipping, spacing, glyphs, page breaks, and contact readability. A successful build or automated check alone is not visual QA or proof of truthfulness. If rendering/inspection is unavailable, state that limitation and leave visual review pending.
6. Draft a concise `cover-letter.md` around two or three specific matches, grounded in the posting and master. Avoid repeating the entire resume. Keep missing facts as review questions outside the final letter.

Update the role README's artifact checklist and `application-checklist.md` with checks actually completed. Mark documents `Draft — needs your review` in the surrounding README and PDF subject where supported; do not add status text that breaks the constrained resume parser. Report files, key positioning choices, unresolved factual gaps, and verification results. The user submits manually.
