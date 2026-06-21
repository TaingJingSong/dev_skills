# Figma Design Context MCP

Extract bounded, evidence-based Figma context and generate a prompt that can be
pasted directly into Codex, Claude Code, Gemini, Cursor, or another coding agent.
The server does not generate implementation code.

## Capabilities

- Validates Figma file, design, and prototype URLs.
- Extracts layout, text, token candidates, and unverified component categories.
- Separates confirmed prototype reactions from low-confidence name hints.
- Generates a project-aware implementation prompt with responsive,
  accessibility, state, testing, and missing-contract instructions.
- Retries transient Figma failures and caches successful responses.
- Returns structured MCP tool results.

Figma visuals are never treated as API, database, permission, or business-rule
contracts.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Set `FIGMA_ACCESS_TOKEN` in `.env`. Use a token with only the access needed to
read the target files. Never commit `.env`.

Run over stdio:

```bash
python src/server.py
```

Example MCP client configuration:

```json
{
  "mcpServers": {
    "figma-design-context": {
      "command": "/absolute/path/to/.venv/bin/python",
      "args": ["/absolute/path/to/src/server.py"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "${FIGMA_ACCESS_TOKEN}"
      }
    }
  }
}
```

Prefer injecting the token from the client environment or a secret manager
instead of placing it directly in client configuration.

## Recommended Flow

Call `generate_design_based_prompt` with:

- `figma_url`: Figma file or selected-node URL.
- `task`: The implementation objective.
- `target_stack`: `mobile`, `frontend`, `backend`, or `fullstack`.
- Optional project path, existing code reference, API contract, business rules,
  and skill names.

Copy the returned `prompt` field into the coding agent. MCP clients that support
prompts can invoke `design_from_figma` directly.

Use a selected-node URL for large files. Extraction limits are deliberate so a
full design file cannot overwhelm the coding agent context.

## Tools

- `get_design_context`
- `get_design_tokens`
- `get_screen_interactions`
- `map_figma_to_project_components`
- `generate_design_based_prompt`

`get_design_context` already includes design tokens and interaction evidence.
Avoid calling all three extraction tools for the same URL. Repeated successful
requests are cached, but unnecessary calls can still consume quota when no cache
entry exists.

## Configuration

| Variable | Default | Purpose |
| --- | ---: | --- |
| `FIGMA_ACCESS_TOKEN` | required | Figma REST API token |
| `FIGMA_REQUEST_TIMEOUT_SECONDS` | `30` | Request timeout |
| `FIGMA_REQUEST_RETRIES` | `3` | Retries for network and 5xx failures |
| `FIGMA_CACHE_DIR` | user cache directory | Cached Figma responses |
| `FIGMA_CACHE_TTL_SECONDS` | `600` | Cache lifetime; `0` disables cache reads |
| `FIGMA_MAX_NODES` | `1500` | Maximum nodes included per extraction |
| `FIGMA_MAX_TEXT_LABELS` | `250` | Maximum text nodes included |
| `FIGMA_MAX_PROMPT_INPUT_CHARS` | `20000` | Maximum size per free-text prompt input |

Cached responses may contain proprietary design text and metadata. The server
stores them in a user-only cache directory with restrictive permissions. Set
`FIGMA_CACHE_TTL_SECONDS=0` to disable caching.

## Rate Limits

HTTP 429 responses return immediately rather than waiting through automatic
retries. The error includes Figma's `Retry-After`, plan tier, and rate-limit type
headers when available.

Wait for the indicated period and retry once. Persistent 429 responses usually
require checking the seat and plan attached to the requested file. Figma's file
and file-node endpoints are Tier 1 and can have very low quotas for Viewer or
Collab seats.

## Validation

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m compileall -q src tests
```
