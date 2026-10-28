# Packaging verification

Checked on **2026-10-27** on macOS with Python 3.12.14, Tectonic 0.17.0, and Poppler 26.05.0.

## Completed checks

| Check | Result |
| --- | --- |
| Dependency install in a fresh virtual environment | Passed with the declared requirements |
| Focused Python tests | 5 passed: generic identity/font rendering, expected-text input validation, missing-text rejection, cover-letter content/metadata identity, and all four full-summary extraction checks |
| Generic master/profile build | Passed: one searchable page, no dependence on a particular identity |
| Robotics, sales-engineering, crypto, venture sample builds | Passed: each has two searchable pages and dominant body text approximately 10.96 pt |
| Rendered sample inspection | All eight pages inspected; no clipped text, overlaps, or broken glyphs observed |
| Three skill definitions | Passed the skill frontmatter validator; support links checked |
| LinkedIn configuration | TOML parses; pinned package; 14 explicit research/session tools; no message/connection tools |
| Privacy scan | Original names, contact strings, profile URLs, and overt career identifiers excluded from public files; PDF metadata and annotations checked |
| Excluded files | Candidate data, generated output, local configuration, environments, and session files covered by Git ignore rules |
| Local documentation links | Checked against the packaged file tree |

The public samples were rebuilt after replacing or removing identifying details. Their generic prose and page breaks were adjusted for readable illustrative layouts. They are format demonstrations and do not preserve an actual applicant's factual resume.

## Extraction regression found during packaging

During initial packaging, unpinned pypdf 6.21.3 merged words in several sample summaries, while 6.10.0 preserved their spaces. The toolkit pins the tested version and verifies each sample's full summary as expected extracted text. Recheck extraction and every rendered page before changing PDF dependencies or fonts. A passing check is not a guarantee about every employer's screening system.

## Not claimed

- No employer applications, outreach, uploads, connection requests, or live form entries were performed.
- No new LinkedIn sign-in was performed. Version/CLI/configuration support was checked against upstream sources; each user's own client/account needs the documented read-only smoke test.
- Linux and Windows/WSL were not run locally. The default font and paths were made portable, and platform notes are provided.
- The anonymized samples are illustrative format demonstrations, not factual resumes. Each applicant supplies their own verified facts.

To repeat the local checks, install dependencies, run `make test`, then `make qa`, and inspect every rendered page under `tmp/pdfs/`.
