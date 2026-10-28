# Anonymized illustrative resumes

Four illustrative adaptations show how one set of sample activities can be arranged for different roles. **These are demonstration statements, not any applicant's verified facts.** They must never be copied into a real application as personal experience.

- `master-resume.md`: anonymized source used for robotics, sales-engineering, and crypto presentation examples.
- `crypto-venture-fund.md`: a condensed research example with generic AI-assisted project demonstrations.
- `profiles/*.json`: presentation choices, section ordering, and selected bullets.
- `expected.json` and `expected/*.json`: shared phrases and complete summaries used to check PDF extraction.
- `pdf/*.pdf`: generated illustrations carrying the same visible anonymization notice.

Names, personal contacts, employers, clients, products, locations, dates, institutions, honors, extracurriculars, distinctive accomplishments, and exact personal metrics were removed or generalized. The contact address uses the reserved `.invalid` domain; it is not a working contact. The examples preserve the format and role-dependent organization of the workflow, not a person's biography.

Run `make qa` from the repository root to rebuild into `output/pdf/` and render inspection images into `tmp/pdfs/`. Inspect every page after changing content, profiles, fonts, or compiler behavior.

Use the empty [master template](../../templates/master-resume.md) and [profile template](../../templates/profile.json) for real work, then supply your own verified information.
