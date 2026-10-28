# Sharing and privacy

The public edition contains workflow instructions, scripts, templates, and anonymized illustrative samples. It excludes the original job pipeline, outreach drafts, recruiter details, interview notes, chat transcripts, credentials, browser sessions, and personal machine configuration.

The examples use a generic candidate name and reserved example contact values. Employer and institution names, locations, employment dates, named clients/projects, exact personal metrics, affiliations, and distinctive personal activities have been removed or generalized. Source filenames, profile IDs, expected-text fixtures, documentation, copyright attribution, PDF metadata, and link annotations are included in the scrub. These samples are format demonstrations, not factual representations of a real candidate. Supply your own verified facts before drafting an application.

PDFs are rebuilt from anonymized sources rather than covered with visual redaction boxes. The public repository starts with a new root commit using generic author and committer attribution; the earlier repository and its history remain private. The public repository is a separate repository, not a fork of the private one.

The hosting GitHub account remains visible as repository owner. Scrubbing repository content does not anonymize that account or its profile.

Your files belong in ignored `private/`; generated artifacts go in ignored `build/`, `output/`, and `tmp/`. Review `git status` and the staged diff before publishing a fork. Git ignores do not remove previously committed files or prevent access to a public repository. Keep personal application data in your own private workspace.

Never share session cookies, MFA codes, auth files, environment files, or browser profiles. The LinkedIn example configuration contains no credentials; each user authenticates locally.
