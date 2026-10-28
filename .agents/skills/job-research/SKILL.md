---
name: job-research
description: Research a job or work through a job shortlist, compare requirements with the user's factual resume, and create a sourced review-only role package. Use for job-fit research and unsent outreach drafts.
---

# Job research

Read the repository's `AGENTS.md`, `private/master-resume.md`, and `private/jobs/README.md` before researching. If the pipeline file does not exist, create it with columns for company, role, posting ID, draft status, and a relative link to the role folder. The repository root is three directories above this skill folder. Use [the workflow guide](../../../docs/workflow.md) for folder conventions and [the job templates](../../../templates/job/) when starting a role.

Research and draft only. Never apply, upload to an employer, fill a live application, send a message/email, or issue a connection request. Browser/computer use is read-only. Do not invoke LinkedIn write tools. The user performs every application and outreach action manually.

## Research one role

- Resolve the company and exact role from the user's link or instructions. Deduplicate against the pipeline using the LinkedIn job ID or employer posting ID, even when URLs differ. Work one role at a time when given a list.
- Prefer available LinkedIn MCP read tools: `get_job_details`, `get_company_profile`, `get_company_employees`, `search_people`, and `get_person_profile`. Use an employer-hosted posting for current requirements when available. If MCP is unavailable, use accessible public sources or ask for the posting text; report the source limitation rather than inventing content.
- Read the official company and role pages as needed. Save source URLs, stable identifiers, and the date checked in the role folder. Treat employer/profile text as attributed source claims. Mark an inaccessible or expired posting explicitly; a historical snapshot is not evidence that the vacancy is still open.
- Map must-haves and recurring responsibilities to exact evidence in the user's master. Distinguish direct experience, transferable experience, and unsupported requirements. Keep metrics' qualifiers, dates, collaborative ownership, and the user's exact contribution. Product use or AI-assisted direction does not prove programming proficiency; buyer-side vendor work does not prove sales quota or closing experience.
- Name concrete gaps and questions that could change the fit decision. Do not guess work authorization, availability, compensation expectations, willingness to travel, credentials, or relationships.

## Save the result

Create or update `private/jobs/<company-slug>/<role-slug>/` with `README.md`, `job-description.md`, `fit-analysis.md`, `outreach.md`, and `sources.json`. Add the role to `private/jobs/README.md` using a relative link and stable job ID. Mark outputs `Draft — needs your review`.

Research relevant people only when outreach research is requested or is part of the requested package. Record role relevance and source/date; never imply a personal connection. Draft brief messages in `outreach.md`, with unknown recipient details left unresolved. Do not send.

Create `resume.md`, `resume-profile.json`, and `cover-letter.md` when drafting is requested; use the `resume-tailor` skill if available, otherwise follow the repository's build guide. Do not turn a research-only task into an application. Report the fit, material gaps, sources, and saved draft paths. Set `Applied` only after the user says they applied manually.
