"""MCP (Model Context Protocol) server exposing twikit's Twitter/X capabilities.

Run with:  python -m twikit_mcp
"""

from .server import main, mcp

__all__ = ["mcp", "main"]
