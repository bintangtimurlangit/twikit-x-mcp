# Configuration

For installing the package, see **[Install](../README.md#install)** in the README. For **per-client, copy-paste** setup (Claude Code, Claude Desktop, Cursor, Windsurf, VS Code), see **[INSTALL.md](../INSTALL.md)**.

> **Cookie auth required.** X's automated login trips a "verify you're human" challenge, so authenticate by copying two cookies from a browser already logged in to x.com: `auth_token` and `ct0`. There is no API key.

---

## Authentication

From DevTools → **Application** (Chrome/Edge) or **Storage** (Firefox) → **Cookies** → `https://x.com`, copy the **Value** of `auth_token` and `ct0`, then set them as environment variables.

| Variable                           | Required | Description                                          |
| ---------------------------------- | :------: | ---------------------------------------------------- |
| `TWIKIT_AUTH_TOKEN`                | ✅       | the `auth_token` cookie value                        |
| `TWIKIT_CT0`                       | ✅       | the `ct0` cookie value                               |
| `TWIKIT_LANGUAGE`                  |          | language header (default `en-US`)                    |
| `TWIKIT_PROXY`                     |          | e.g. `http://user:pass@host:port`                    |
| `TWIKIT_MCP_RATE_LIMIT`            |          | `on` (default); set `off`/`0`/`false` to disable     |
| `TWIKIT_MCP_RATE_LIMIT_PER_MINUTE` |          | max tool calls per minute (default `30`)             |

> 🔐 Treat the cookies like a password. Don't commit them (`.env` is gitignored). They rotate when you log out of that browser session — refresh them if requests start failing.

Copy `.env.example` to `.env` for local development, or set these in your MCP client's `env` block.

---

## MCP configuration

This server uses **stdio**. The typical entry runs it via `uvx` (no install step):

```json
{
  "mcpServers": {
    "twikit": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/bintangtimurlangit/twikit-mcp", "twikit-mcp"],
      "env": {
        "TWIKIT_AUTH_TOKEN": "…",
        "TWIKIT_CT0": "…"
      }
    }
  }
}
```

Exact per-client file locations and variants (pipx/pip/clone) are in **[INSTALL.md](../INSTALL.md)**. Using an undocumented client? Point its AI at **[llms-install.md](../llms-install.md)**.

## Rate limiting

To reduce the risk of rate-limit errors or account suspension, the server throttles tool calls **by default** (token bucket, 30 calls/minute). Call the `rate_limit_status` tool to see the active configuration.
