# Security

## Supported versions

Security fixes are applied to the **latest release** on the default branch when practical.

## Reporting a vulnerability

Please **do not** open a public GitHub issue for undisclosed security problems.

1. Use [GitHub private vulnerability reporting](https://github.com/bintangtimurlangit/twikit-x-mcp/security/advisories/new) if it is enabled for this repository, **or**
2. Contact the maintainers via a private channel (e.g. email on your GitHub profile).

Include:

- A short description of the issue and its impact
- Steps to reproduce (or a proof-of-concept), if safe to share
- Affected versions or dependency versions, if known

We aim to acknowledge reports within a few days and coordinate disclosure after a fix is available.

## Scope and credential handling

This is a **local MCP server** that authenticates to **Twitter / X** as **your own account** using two session cookies. Be aware:

- Authentication is via `TWIKIT_AUTH_TOKEN` and `TWIKIT_CT0` (the `auth_token` and `ct0` cookies from a logged-in browser). **Treat these like a password** — they grant full access to your account. Set them in your MCP client's `env` block or a local `.env` (which is gitignored); **never commit them**. They rotate when you log out of that browser session.
- The server performs **write actions** (post, delete, like, retweet, follow, DM) on your real account. Review what your MCP client is allowed to call, and keep the built-in rate limiting enabled.
- This project **bundles a lightly patched copy of twikit** under `twikit/` (MIT). Vulnerabilities in the underlying library are best reported [upstream](https://github.com/d60/twikit) as well.

Issues in **X's services** or in **upstream** dependencies (e.g. `mcp`, `httpx`) should be reported to those projects when appropriate.
