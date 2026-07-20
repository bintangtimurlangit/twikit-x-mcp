"""
Client-side rate limiting for the twikit MCP server.

Automating X too aggressively risks rate-limit errors and account suspension, so
the server smooths outgoing tool calls to a safe pace **by default**. It can be
tuned or fully disabled via environment variables:

    TWIKIT_MCP_RATE_LIMIT             on (default) | off   -> master toggle
    TWIKIT_MCP_RATE_LIMIT_PER_MINUTE  max tool calls / minute (default 30)

Set ``TWIKIT_MCP_RATE_LIMIT=off`` (or 0/false/no) to remove throttling entirely.
"""

from __future__ import annotations

import asyncio
import os
import time

DEFAULT_PER_MINUTE = 30.0

_FALSEY = {"0", "false", "off", "no", "disable", "disabled", ""}


def _env_enabled(name: str, default: bool) -> bool:
    val = os.environ.get(name)
    if val is None:
        return default
    return val.strip().lower() not in _FALSEY


class RateLimiter:
    """Async token-bucket limiter shared across all MCP tools.

    Allows at most ``rate`` operations per ``per`` seconds, with token-bucket
    smoothing (short bursts up to ``rate`` are permitted, then calls are spaced
    out). When disabled, :meth:`acquire` is a no-op.
    """

    def __init__(self, rate: float, per: float = 60.0, enabled: bool = True):
        self.rate = max(float(rate), 0.0)
        self.per = float(per)
        # A zero/negative rate can never grant a token, so treat it as disabled
        # rather than deadlocking every call.
        self.enabled = bool(enabled) and self.rate > 0
        self._allowance = self.rate
        self._last = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        """Block until one token is available (no-op when disabled)."""
        if not self.enabled:
            return
        async with self._lock:
            now = time.monotonic()
            self._allowance += (now - self._last) * (self.rate / self.per)
            self._last = now
            if self._allowance > self.rate:
                self._allowance = self.rate
            if self._allowance < 1.0:
                wait = (1.0 - self._allowance) * (self.per / self.rate)
                await asyncio.sleep(wait)
                self._allowance = 0.0
                # Re-anchor the clock past the sleep so the waited time isn't
                # also credited as elapsed on the next call (which would let
                # calls through at ~2x the configured rate under load).
                self._last = time.monotonic()
            else:
                self._allowance -= 1.0

    def describe(self) -> str:
        if not self.enabled:
            return "rate limiting: disabled"
        return f"rate limiting: {self.rate:g} calls / {self.per:g}s"

    @classmethod
    def from_env(cls) -> RateLimiter:
        enabled = _env_enabled("TWIKIT_MCP_RATE_LIMIT", True)
        raw = os.environ.get("TWIKIT_MCP_RATE_LIMIT_PER_MINUTE")
        try:
            rate = float(raw) if raw is not None else DEFAULT_PER_MINUTE
        except ValueError:
            rate = DEFAULT_PER_MINUTE
        return cls(rate=rate, per=60.0, enabled=enabled)
