# Development

## Setup

```bash
git clone https://github.com/bintangtimurlangit/twikit-x-mcp
cd twikit-x-mcp
uv sync --extra dev          # or: pip install -e ".[dev]"
pre-commit install && pre-commit install --hook-type commit-msg
```

## Commands

| Command                       | Description                                                     |
| ----------------------------- | -------------------------------------------------------------- |
| `uv run ruff check .`         | Lint (`--fix` to auto-fix)                                      |
| `uv run ruff format .`        | Format (`--check` to verify)                                    |
| `uv run mypy twikit_x_mcp`      | Type-check our code (advisory — see below)                     |
| `uv run pytest`               | Run the test suite                                             |
| `python -m twikit_x_mcp`        | Run the server manually (or the `twikit-x-mcp` script)           |

## Project layout

```
twikit_x_mcp/
  __init__.py
  __main__.py         # entry point (python -m twikit_x_mcp)
  server.py           # MCP server + all tool definitions
  serialization.py    # twikit objects -> plain dicts for MCP responses
  ratelimit.py        # token-bucket throttle
twikit/               # VENDORED upstream twikit (patched login) — do not lint/format
tests/
  test_auth.py
  test_cursor.py
  test_ratelimit.py
  test_serialization.py
```

## The vendored twikit fork

This repo **bundles a lightly patched copy of twikit** under `twikit/` (MIT, license preserved at `licenses/twikit-LICENSE.txt`), because the published twikit is currently broken on X (the `Couldn't get KEY_BYTE indices` login bug). When upstream ships a fix, delete `twikit/` and depend on the PyPI `twikit` package instead.

Patches carried on top of upstream:

| Patch | Why |
| --- | --- |
| Login (`KEY_BYTE indices`) | The published twikit can't authenticate against current X. |
| Pagination cursors (`Client._extract_cursor_value`) | X moved the cursor from `content.itemContent.value` to `content.value`, and wraps the nested "show more replies" cursor under `item` instead of `content`. Upstream still indexes the old path unconditionally, raising `KeyError: 'itemContent'` — most visibly in `get_tweet_by_id()` on long-form posts. Covered by `tests/test_cursor.py`. |

Keep this table current when patching `twikit/` — it is the checklist for what to re-apply (or drop) when the vendored copy is refreshed or removed.

**Tooling excludes `twikit/`**: Ruff (`extend-exclude`) and mypy (`exclude`) only check our own `twikit_x_mcp/` and `tests/`.

## Type checking (advisory)

`mypy` is configured (`[tool.mypy]` in `pyproject.toml`) and runs in CI as a **non-blocking** step for now — the existing code isn't fully typed. Making it a hard gate is a planned follow-up; it is not required for a green build today.

## Tech stack

- Python 3.10+
- `mcp` (Model Context Protocol SDK), `httpx`
- Ruff (lint + format), mypy, pytest
