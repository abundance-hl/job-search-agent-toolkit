# Job Search Agent Toolkit

A reusable job-search workflow developed through real job-search work with AI agents: research roles, map experience honestly, draft application materials, build readable PDFs, and prepare for interviews. **You review, apply, and contact people yourself.**

Start here with your agent. The repository includes three reusable skills, a LinkedIn MCP setup guide, editable templates, the resume build tools, and four anonymized illustrative resume examples.

## Give your agent this prompt

```text
Read README.md and AGENTS.md. Help me set up this job-search toolkit.
Check the available tools and dependencies before installing anything.
Create my working files under private/. Help me turn my own resume into
private/master-resume.md and a matching private/profile.json.
Treat examples/sample-candidate/ as formatting examples, never as my experience.
If I want LinkedIn research, walk me through docs/linkedin-mcp.md and let
me complete sign-in myself. Verify only the allowed read tools are exposed.
Then research one role I choose. Never apply, fill a live application,
upload my documents, send outreach, or connect with people on my behalf.
```

## Quick setup

1. Clone this repo and open the folder in Codex (or your agent's local workspace):

   ```sh
   git clone https://github.com/abundance-hl/job-search-agent-toolkit.git
   cd job-search-agent-toolkit
   ```

2. Read [AGENTS.md](AGENTS.md). Your private resume, job pipeline, and drafts belong under `private/`, which Git ignores. Start with:

   ```sh
   mkdir -p private/jobs
   cp templates/master-resume.md private/master-resume.md
   cp templates/profile.json private/profile.json
   ```

   Replace the synthetic placeholders with your facts. The profile refers to exact employer/role IDs; update those too. [Resume format and profile guide](docs/resume-format.md).

3. To build PDFs, install Python 3.10+, [Tectonic](https://tectonic-typesetting.github.io/), Poppler, and Make. On macOS with Homebrew:

   ```sh
   brew install python tectonic poppler make
   python3 -m venv .venv
   . .venv/bin/activate
   python -m pip install -r requirements.txt
   make demo
   ```

   `make demo` builds and checks the robotics example. `make qa` builds all four samples, checks PDF text and readability, and renders pages for inspection. Look at the rendered pages too: automated checks cannot prove the layout or claims are correct. The first Tectonic run needs internet access to download TeX resources. Use [platform notes and troubleshooting](docs/setup.md) for Linux/Windows or missing tools.

4. For LinkedIn research, follow [LinkedIn MCP setup](docs/linkedin-mcp.md). It is optional: employer pages and job text you provide also work. Everyone connects their own account; this repo contains no login state.

5. Open a new Codex chat in this repo and invoke a skill below. Codex discovers repository skills in `.agents/skills/`; another agent can read the corresponding `SKILL.md` directly. See [official OpenAI skills guidance](https://learn.chatgpt.com/docs/customization/overview#skills).

## Invoke the skills

| Skill | Use it for | Example prompt |
| --- | --- | --- |
| [`job-research`](.agents/skills/job-research/SKILL.md) | Role/company research, fit analysis, source tracking, draft outreach | `$job-research Research this job: <posting URL>. Use my private/master-resume.md, record sources, and create one draft role folder.` |
| [`resume-tailor`](.agents/skills/resume-tailor/SKILL.md) | Evidence-backed tailoring, a cover-letter draft, PDF build and review | `$resume-tailor Tailor my resume for private/jobs/<company>/<role>. Use only facts in my master resume and flag gaps.` |
| [`interview-prep`](.agents/skills/interview-prep/SKILL.md) | A concise interview brief, grounded talking points, prioritized questions | `$interview-prep Prepare a glanceable brief for private/jobs/<company>/<role>, with sourced company facts and stories supported by my resume.` |

These skills were **packaged for this repository from the existing workflow**. The original chats used workspace instructions, scripts, profiles, and bundled document tools; no separate custom job-search skill files were recovered. [Provenance and history](docs/provenance.md).

If `$skill-name` does not appear in your client, reopen the project/start a new chat or ask it to read the linked `SKILL.md`. You do not need to install these skills globally. Generic PDF/Word plugins are optional; the included scripts run without them.

## How the workflow works

```mermaid
flowchart LR
  A[Your factual master resume] --> B[Research one role]
  B --> C[Evidence and gap analysis]
  C --> D[Role profile and drafts]
  D --> E[Build PDF]
  E --> F[Text and visual checks]
  F --> G[Your review]
  G --> H[You apply or send manually]
```

The agent creates one folder per role under `private/jobs/<company>/<role>/`, using [templates/job](templates/job). Posting IDs prevent duplicates. `private/jobs/README.md` tracks progress. Every role package stays **Draft — needs your review** unless you explicitly report a status change. [Full workflow](docs/workflow.md).

Build your own profile after replacing the template facts:

```sh
make resume SOURCE=private/master-resume.md PROFILE=private/profile.json NAME=my-resume
```

Generated files go to ignored `build/`, `output/`, and `tmp/`. Review `output/pdf/my-resume.pdf` and its rendered pages. An agent can use `scripts/build_cover_letter_pdf.py --help` for optional cover-letter output.

## Sample resumes

The [sample resumes](examples/sample-candidate/README.md) contain source Markdown, JSON profiles, and rebuilt PDFs. Names, contact details, employers, institutions, locations, dates, named projects, and distinctive metrics have been replaced, omitted, or generalized. They are illustrative adaptations for learning the format, not factual resumes or application-ready claims.

| Example | PDF | Profile |
| --- | --- | --- |
| Robotics & automation | [View](examples/sample-candidate/pdf/robotics.pdf) | [JSON](examples/sample-candidate/profiles/robotics.json) |
| Sales engineering | [View](examples/sample-candidate/pdf/sales-engineering.pdf) | [JSON](examples/sample-candidate/profiles/sales-engineering.json) |
| Crypto research | [View](examples/sample-candidate/pdf/crypto.pdf) | [JSON](examples/sample-candidate/profiles/crypto.json) |
| Crypto venture fund | [View](examples/sample-candidate/pdf/crypto-venture-fund.pdf) | [JSON](examples/sample-candidate/profiles/crypto-venture-fund.json) |

## Repository map

```text
.agents/skills/       Three portable agent workflows
AGENTS.md            Agent boundaries and factual-source rules
config/              Example read-only LinkedIn MCP configuration
docs/                Setup, workflow, format, provenance, and privacy notes
examples/sample-candidate/  Anonymized illustrative resumes and profiles
scripts/             Resume generation, PDF validation, cover-letter rendering
templates/           Blank master/profile and job-package scaffolds
tests/               Focused checks for the portable tools
private/             Your files (created locally, ignored by Git)
```

The toolkit never guarantees an ATS score or hiring outcome. Its checks catch extraction/layout problems; they do not verify employment facts. See [sharing and privacy](docs/privacy.md), [verification](docs/verification.md), and [third-party notices](THIRD_PARTY_NOTICES.md).
