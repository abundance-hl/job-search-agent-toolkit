# LinkedIn MCP setup

Upstream project: **[stickerdaniel/linkedin-mcp-server](https://github.com/stickerdaniel/linkedin-mcp-server)**. This is independent software, not an official LinkedIn integration. The full upstream server includes write actions; this toolkit exposes only selected research tools.

Checked 2026-10-27. The example pins [PyPI version 4.28.0](https://pypi.org/project/mcp-server-linkedin/4.28.0/) and requests Python 3.12 through uv. The published package requires Python >=3.12.4 and <3.15. Review [upstream releases](https://github.com/stickerdaniel/linkedin-mcp-server/releases) before changing the pin. Upstream also documents `@latest`, which opts into automatic updates; the starter uses a fixed version.

## 1. Install uv and sign in yourself

Install [uv using its official instructions](https://docs.astral.sh/uv/getting-started/installation/). On macOS with Homebrew, `brew install uv` is an option. Then run:

```sh
uvx --python 3.12 mcp-server-linkedin==4.28.0 --no-auto-import --login
```

Complete sign-in and any verification in the browser yourself. Keep passwords, MFA codes, cookies, and browser-session files out of chats and Git. The server may download its browser on first use; leave time for setup. `--no-auto-import` prevents importing a session from an ordinary signed-in browser; the server can still reuse its own previously saved session. This guide does not establish account eligibility or authorize bypassing access restrictions.

## 2. Add the read-tool configuration

Read [config/linkedin.codex.toml.example](../config/linkedin.codex.toml.example). Merge that entire table into `~/.codex/config.toml`, or use `.codex/config.toml` in a trusted project. **Do not overwrite an existing config.** If a `linkedin` server already exists, reconcile that table instead of duplicating it.

The example file does nothing by itself. It contains no credentials. The server command is `uvx`; if a desktop app cannot find it, use the absolute path returned by `command -v uvx` in your local config only. Restart the client/server after making changes. [Official Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp) documents these locations, timeouts, and `enabled_tools` filtering.

The allowlist is essential to this workflow. Do not remove it to solve a connection error. Do not also enable an unrestricted duplicate LinkedIn server/plugin.

## 3. Verify the connection

Ask your agent:

```text
List the tools available from the LinkedIn server. Confirm they match the
read-tool allowlist in config/linkedin.codex.toml.example. Do not call any
message, connection, application, or other write tool. If the tool list is
correct, read the company profile at a public company URL I provide and
report its source URL. Stop if authentication or access fails.
```

If you use Codex CLI, `codex mcp list` checks configuration. Tool availability must also be checked in the active chat. The setup commands were checked against current upstream docs; a fresh account login was not performed as part of packaging.

## Useful tools

- `get_job_details(job_id=...)`: use the numeric ID from a LinkedIn posting URL.
- `get_company_profile(company_name=...)`: use the exact company URL slug, not an assumed display-name match.
- `search_companies`: resolve ambiguous company slugs.
- `get_company_employees`: research people associated with a company.
- `search_people`: research relevant roles. For `current_company`, use the numeric company URN from company data; a company name may not filter correctly.
- `get_person_profile`: read public profile information and record the source.

Tool schemas can change. Inspect the available schema before calling. Record IDs, URLs, and access dates in each role folder. Avoid collecting unrelated personal information.

## Troubleshooting

| Symptom | Next step |
| --- | --- |
| `uvx` not found | Install uv, then restart the app or set the executable path locally. |
| Browser setup/authentication in progress | Let the browser download/sign-in finish, then retry one read. |
| No tools after config change | Check table spelling and actual tool names; restart. Keep the allowlist in place. Use public employer pages while investigating. |
| Login challenge, checkpoint, or denied access | Stop. Let the user handle it manually; do not bypass it or loop retries. |
| Same server configured twice | Keep one intended instance with the research allowlist. |
| Teammate cannot use your connection | Each person must configure and authenticate their own local server. |

Only source/configuration checks are claimed here; your local client and account need the smoke check above.
