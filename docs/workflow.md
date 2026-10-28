# Working through a job search

These three skills package the practices developed in the original resume-building workspace. They are new reusable entrypoints for this starter kit; they are not recovered copies of historical custom `SKILL.md` files.

The toolkit researches and drafts. You review and perform every application or outreach action yourself.

## Keep your facts and working files private

Your factual source is `private/master-resume.md`. Start from `templates/master-resume.md`, replace its illustrative entries with your actual history, and have your agent check the format. Keep reusable profiles in `private/profile.json` (or additional profiles under `private/profiles/`) and your pipeline in `private/jobs/README.md`.

The source examples in `examples/sample-candidate/` show how a resume can be arranged for different roles. Their experience IDs and generalized claims are illustrative placeholders. Build your own profiles against your own source; copying a sample profile unchanged will either fail because its IDs do not exist or insert unsupported wording.

The public kit contains empty job scaffolds under `templates/job/`. Copy those into a new role folder only when you begin working on it. The `private/` directory and generated output directories are excluded from Git by this starter kit. Check staged files before publishing any changes; ignore rules do not remove material already committed.

## Invoke a skill

Open this repository in your agent and read `AGENTS.md` first. In a client that discovers repository skills, explicitly name the skill with `$`:

```text
$job-research Research this role: <posting URL>.
Compare it with private/master-resume.md, save sources and gaps,
and create a draft role folder. Do not apply or contact anyone.
```

```text
$resume-tailor Draft the resume and cover letter for
private/jobs/<company>/<role>/ using only supported facts.
Build the PDF and check the extracted text and rendered pages.
```

```text
$interview-prep Prepare a short hiring-manager brief for
private/jobs/<company>/<role>/ and rehearse one question at a time.
```

If the client does not discover a skill, ask it to read the corresponding `.agents/skills/<name>/SKILL.md` directly and follow it. The instructions and build scripts remain usable without a particular model. LinkedIn tools depend on your own MCP setup; unavailable tools should be reported, not simulated.

## One role, one folder

Use `private/jobs/<company-slug>/<role-slug>/`. Check the pipeline for the stable LinkedIn job ID or employer posting ID before adding a role; multiple URLs can identify the same opening.

| Artifact | Purpose |
| --- | --- |
| `README.md` | Status, stable identifiers, links, artifact checklist |
| `job-description.md` | Sourced responsibilities, requirements, conditions |
| `fit-analysis.md` | Evidence map, direct/transferable matches, gaps and questions |
| `outreach.md` | Relevant people and unsent message drafts, when requested |
| `sources.json` | Source URLs, stable IDs, dates checked and availability |
| `resume.md` | Role-specific constrained Markdown, created when drafting starts |
| `resume-profile.json` | Role-specific presentation and selection profile |
| `cover-letter.md` | Review-only letter draft |
| `application-checklist.md` | Factual, document and manual-submission checks |
| `interview-brief.md` | Optional sourced preparation and truthful story outlines |

Keep the pipeline's links relative to `private/jobs/README.md`. Use `Draft — needs your review` for new packages. Mark `Applied` only after you tell the agent you applied manually, recording the date you provide. A generated PDF is not an application.

## Sources and fit

Prefer the employer's live posting for current role requirements and the LinkedIn MCP's read tools for LinkedIn research. Keep the original URL and stable ID when a posting moves or expires. Record an ISO date for each check. Treat employer descriptions and profile text as claims from those sources, and label the agent's assessment as an inference.

A useful evidence map separates direct experience, transferable experience, and unsupported requirements. Preserve "estimated," "approximately," "co-led," internship dates, and other qualifiers. Never infer quota attainment from vendor management, account ownership from institutional readership, or programming fluency from directing AI-assisted development. Missing evidence belongs in questions and gaps.

If LinkedIn is unavailable, the agent may use an accessible employer posting or text you provide, label that source, and continue with the supported scope. It must not invent LinkedIn results, bypass login challenges, or fill live application forms.

## Build, inspect, review

Follow [the resume format and build guide](resume-format.md). Build from editable Markdown and JSON; regenerate the LaTeX after changes. From the repository root, for example:

```sh
make resume \
  SOURCE=private/jobs/example-company/example-role/resume.md \
  PROFILE=private/jobs/example-company/example-role/resume-profile.json \
  NAME=example-company-example-role
```

This writes `output/pdf/example-company-example-role.pdf` and extraction/rendering files under `tmp/pdfs/example-company-example-role/`. Use your actual role folder names. The guide explains optional expected-text checks and tool overrides.

Automated extraction checks catch missing text and some readability problems. Render and inspect every page to catch layout defects. Neither check verifies that a career claim is true: compare the final document with your source and evidence map.

Before you use a draft, confirm your contact details, job dates, titles, metric qualifiers, role-specific claims, and any application answers. Work authorization, compensation, availability, travel, and similar answers come from you. Refresh time-sensitive employer facts before submitting manually.
