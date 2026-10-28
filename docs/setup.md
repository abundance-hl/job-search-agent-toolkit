# Setup and troubleshooting

You can research and draft Markdown without PDF tools or LinkedIn. Add those components when needed.

## PDF toolchain

Use Python 3.10+ for the toolkit, Tectonic to compile LaTeX, Poppler (`pdftoppm`) to render pages, and Make. The LinkedIn MCP has its own Python requirement and is isolated by uv.

macOS:

```sh
brew install python tectonic poppler make
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
make demo
```

Linux: install Python, venv support, Make, and Poppler with your distribution's package manager; install Tectonic through its [official installation guide](https://tectonic-typesetting.github.io/en-US/install.html). Ubuntu/Debian packages commonly include `python3-venv`, `make`, and `poppler-utils`. Then create the venv and install the requirements as above.

Windows: use WSL with the Linux setup for the supplied Makefile. Native Windows may run the Python scripts, but the shell/Make workflow has not been validated there.

All paths in the toolkit are repository-relative. You can override tools without changing files:

```sh
make demo PYTHON=/path/to/python3 TECTONIC=/path/to/tectonic PDFTOPPM=/path/to/pdftoppm
```

The default fonts come from the TeX bundle. Optional profile font overrides require that font to be available on the machine. A font change can change wrapping and pagination, so re-render and inspect all pages.

## Working copy

Use `private/master-resume.md` as your source of truth, `private/profile.json` for your reusable presentation profile, and `private/jobs/` for role packages. The template is synthetic scaffolding, not a completed resume. Profiles reference employer/role IDs, so copying a the sample candidate profile onto unrelated work history will fail or select the wrong content. Build your own IDs as documented in [resume-format.md](resume-format.md).

`make demo` and `make qa` use the shipped examples; `make resume SOURCE=... PROFILE=... NAME=...` builds your own files. Use names without spaces or shell metacharacters for `NAME` (for example `my-resume`). Quote source/profile path arguments containing spaces.

## Skill discovery

The `.agents/skills/` folders ship with the repo. Open the repo root in a fresh Codex chat. Type `$job-research`, `$resume-tailor`, or `$interview-prep`, or explicitly ask the agent to read the corresponding `SKILL.md`. Other clients can follow those Markdown instructions even if they do not support Codex's discovery syntax. [Official skills guidance](https://learn.chatgpt.com/docs/customization/overview#skills).

No global skill copy, model-specific setting, plugin install, API key, or cloud deployment is required for the scripts. An agent product itself may require an account/subscription.

## Common build failures

- **Missing package:** activate `.venv` and install `requirements.txt` with that interpreter. Pass `PYTHON=python` if your environment needs it.
- **Unknown experience ID:** update the profile to match the company/role headings in your source.
- **Font unavailable:** remove the custom `font` override to use the bundled default, then rerun visual QA.
- **First Tectonic build stalls:** it downloads resources; check network access and the compiler message.
- **More than two pages or underfilled page one:** edit bullet selection/page-break settings, not font size below the readability threshold.
- **Expected phrase missing:** compare the extracted text with the intended source. A check file is a regression aid, not a factual database.
- **Draft looks fine but text checks fail:** fix extraction/glyph issues before sharing; do not treat screenshots alone as QA.

## Checks

Run `python -m unittest discover -s tests -v` for focused script tests and `make qa` for the four example builds. See [verification.md](verification.md) for the checks actually performed during packaging and their limits.
