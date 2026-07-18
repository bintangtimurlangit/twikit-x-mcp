# twikit-mcp documentation

**twikit-mcp** is a [Model Context Protocol](https://modelcontextprotocol.io/) server that exposes **[twikit](https://github.com/d60/twikit)'s** Twitter / X capabilities to AI assistants over **stdio** — no official X API key required. For Claude Code, Claude Desktop, Cursor, Windsurf, VS Code, and other MCP hosts.

| Document                            | Description                                                                                         |
| ----------------------------------- | -------------------------------------------------------------------------------------------------- |
| [Configuration](./CONFIGURATION.md) | Auth cookies, env vars, rate limiting; per-client setup lives in [INSTALL.md](../INSTALL.md)         |
| [Development](./DEVELOPMENT.md)     | Ruff, mypy, pytest, project layout, the vendored twikit fork                                        |
| [Releases](./RELEASES.md)           | SemVer, git tags, publishing, [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) |
| [Changelog](../CHANGELOG.md)        | Version history ([Keep a Changelog](https://keepachangelog.com/en/1.1.0/))                           |

**Installation** is in the [root README](../README.md#install); **per-client setup** is in [INSTALL.md](../INSTALL.md), and an agent-followable spec is in [llms-install.md](../llms-install.md).

**Community, security, license:** [CONTRIBUTING.md](../CONTRIBUTING.md) · [SECURITY.md](../SECURITY.md) · [Code of Conduct](../CODE_OF_CONDUCT.md) · [MIT License](../LICENSE)
