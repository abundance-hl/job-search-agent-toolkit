# Resume source and build format

The builder accepts a deliberately small Markdown format, shown in
[`templates/master-resume.md`](../templates/master-resume.md). It is not a general
Markdown-to-PDF converter. Use Python 3.10 or newer.

## Master resume

1. Put the applicant's name on the first non-empty line, in `**bold**`.
2. Put the factual summary below it.
3. Use one contact line containing an email address and `|` separators.
4. Keep the exact markers `**WORK EXPERIENCE**` and `**EDUCATION**`.
5. For each experience, use a bold employer line followed by a bold role line:
   `**Role - Location | Dates**`.
6. Use `* ` for bullet lines. Other lines within an experience are description
   paragraphs. Bold-only lines start a new experience, so avoid those in bullets.
7. Education content follows `**EDUCATION**`.

Single-line HTML comments and standalone `---` separators are ignored. Inline
bold, italic, and Markdown links are supported; nested formatting, tables, images,
and multiline bullets are not.

## JSON profiles

The master stores facts; a profile selects their presentation. Copy
[`templates/profile.json`](../templates/profile.json) and edit the copy. Sample
profiles select the sample candidate's experience IDs and therefore do **not** work unchanged
with another person's master.

Each experience ID is the lowercase employer name plus role, with punctuation
converted to hyphens. Text after ` - ` in the employer line is excluded from the
ID. For example, `Example Employer` and `Your Role` produce
`example-employer-your-role`. The builder prints available IDs if one is wrong.

| Field | Meaning |
| --- | --- |
| `summary` | Optional visible summary override; it must remain factual. |
| `sections` | Ordered sections, each with a `heading` and `entries`. |
| `entries[].id` | Master experience ID; each may appear only once. |
| `entries[].bullet_indexes` | Zero-based indexes selecting original bullets. |
| `entries[].bullets_override` | Replacement bullets; takes precedence over indexes. Human verification required. |
| `entries[].include_description` | Whether to retain the source description (default true). |
| `entries[].description_override` | Replacement description, or empty string to omit it. |
| `contact` | Optional array replacing the source contact fields. Check this before sharing a profile. |
| `contact_break_after` | Split the contact array after this many fields. |
| `page_break.before_experience` | Start a page before the specified included ID. |
| `page_break.after_bullet` | Object with `experience` and `count`; split after that many selected bullets. |
| `education_before_section` | Move education before the exact named section. |
| `font` | Optional installed font; default is the bundled TeX Gyre Termes. |
| `pdf_subject` | PDF subject metadata; also check this before sharing. |

The two page-break forms are mutually exclusive. Omit page breaks initially,
then inspect the rendered PDF before adding one. Optional `layout` settings
include `body_font_size`, `body_leading`, `item_sep`, `item_top_sep`,
`section_before`, `section_after`, `company_vspace`, `description_vspace`, and
`education_vspace` (positive values in points). `font_kerning` is `On` or `Off`.

## Build and review

With Python dependencies installed, and `tectonic` and `pdftoppm` on PATH:

```sh
make demo
make qa
make resume SOURCE=private/master-resume.md PROFILE=private/profile.json NAME=my-resume
```

`NAME` is an output filename stem; use simple letters, numbers, underscores, or
hyphens. Output goes to `output/pdf/`, generated TeX to `build/`, and extracted
text plus rendered PNG pages to `tmp/pdfs/<name>/`. Pass `PYTHON`, `TECTONIC`, or
`PDFTOPPM` to Make to override the executables. Do not edit generated TeX.

Tectonic may download its TeX bundle on the first build. The default font uses
files from that bundle and does not need Microsoft fonts. A custom `font` requires
that font to be installed on the machine doing the build.

The PDF check requires one or two searchable pages, rejects broken replacement
glyphs, checks a dominant font size of at least 10.5 pt, and flags an underfilled
first page when there are two pages. These are document checks, **not** fact
verification, layout approval, or an ATS ranking guarantee. Open every page and
inspect it for clipping, spacing, and sensible breaks after it passes.

For text-specific checks, create a JSON array of important visible phrases:

```json
["Your Name", "Your Institution", "An important verified result"]
```

```sh
make resume SOURCE=private/master-resume.md PROFILE=private/profile.json NAME=my-resume EXPECTED=private/expected.json
python3 scripts/validate_resume.py output/pdf/my-resume.pdf --expected private/expected.json
```

Expected phrases detect lost text during extraction. They do not prove that the
claims are true. Review profile overrides against the factual master separately.

The example checks in `examples/sample-candidate/expected/` include each profile's entire
summary, so missing word spaces fail validation. The validator tolerates smart
versus straight quotes but never removes word spaces to make a check pass.

`pypdf` is deliberately pinned to **6.10.0**. On these same PDFs, 6.21.3 joined
words in three sample summaries even though 6.10.0 preserved them. An independent
check with `pdfplumber` and `x_tolerance=2` preserved all four summaries; its
default 3-point threshold can also join words whose gaps are slightly smaller
than 3 points. This is extraction-version/tolerance sensitivity, not missing
visible words. When upgrading PDF libraries, run `make test` and `make qa`, then
review extracted text and the rendered pages. Do not treat an upgrade as safe
merely because the PDF still opens.

## Cover letters

The optional cover-letter renderer uses plain paragraphs, removes a leading
Markdown title and `Status:` line, and adds the supplied name/contact header.
Avoid duplicating that header in the letter body. It does not render general
Markdown formatting.

```sh
python3 scripts/build_cover_letter_pdf.py private/cover-letter.md output/pdf/cover-letter.pdf \
  --title "Cover letter draft" --name "Your Name" --contact "you@example.com | Your city"
```

The name also becomes PDF author metadata. The renderer uses Arial where present
on macOS and ReportLab's standard Helvetica elsewhere. Inspect the resulting PDF
before using it; this command does not send or upload anything.
