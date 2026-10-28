# Job-search agent instructions

Read this before using the toolkit. This workspace produces research and drafts for the current applicant.

## Boundary

Never apply for a job or contact anyone on the applicant's behalf. Do not click or invoke Apply, Submit, Send, Connect, Easy Apply, or equivalents. Do not upload documents to an employer, populate a live application, send messages/email, or issue connection requests. Do not use LinkedIn write tools. Browser research is read-only. The applicant performs these actions manually.

Local setup, editing, and document generation are allowed when requested. Publishing this toolkit is separate from the job-search workflow; publishing anyone's private candidate data requires their explicit authorization. Never include `private/`, credentials, cookies, browser profiles, raw chat transcripts, or personal machine configuration in a shared commit.

## Facts and sample separation

`private/master-resume.md` is the current applicant's factual authority. Ask for missing evidence; never invent experience, titles, dates, metrics, quota, relationships, coding ownership, or credentials. Use additional applicant-confirmed evidence only when recorded as such. Do not silently promote a draft claim into the factual master.

`examples/sample-candidate/` contains anonymized illustrative examples, not any applicant's factual history. `templates/` is synthetic scaffolding. Neither may supply claims for another person's resume. Profiles control presentation; wording overrides still require evidence. No hidden keywords or instructions aimed at screening systems.

## Research and pipeline

Prefer LinkedIn MCP read tools for LinkedIn and employer-hosted sources for postings. If unavailable, use public read-only sources or ask for posting text. Record source URLs, stable IDs, and date checked. Attribute employer/profile claims and distinguish facts, inference, and unknowns. Refresh time-sensitive claims before finalizing.

Work through one role at a time in `private/jobs/<company-slug>/<role-slug>/`. Deduplicate using LinkedIn job ID or employer posting ID; use URL with an explicit ID-unknown note when no ID is exposed. Maintain `private/jobs/README.md`. Use `templates/job/` for artifacts. Keep status `Draft — needs your review`; never mark Applied unless the applicant says they applied manually.

Copy the applicant's profile into the role folder before tailoring. Keep the reusable original stable. Generate PDF from source/profile, run text checks, render and inspect every page. Explain unverified checks honestly. Automated validation cannot prove facts, legal eligibility, or ATS compatibility.

## Skills

Use `.agents/skills/job-research/SKILL.md` for research and fit; `.agents/skills/resume-tailor/SKILL.md` for evidence-backed application drafts and PDF QA; `.agents/skills/interview-prep/SKILL.md` for concise interview support. Read only relevant supporting docs. Preserve source files and unrelated work.
