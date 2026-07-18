"""
Tests for the client-side rate limiter (enabled by default, toggleable).
"""

import asyncio
import time

from twikit_mcp.ratelimit import RateLimiter, _env_enabled


def test_disabled_is_noop_and_fast():
    limiter = RateLimiter(rate=1, per=60, enabled=False)

    async def run():
        start = time.monotonic()
        for _ in range(10):
            await limiter.acquire()
        return time.monotonic() - start

    elapsed = asyncio.run(run())
    assert elapsed < 0.1  # no throttling


def test_enabled_throttles_beyond_burst():
    # 60/min == 1/sec. Bucket starts full (burst of 60), so to observe spacing we
    # use a small rate with a small bucket.
    limiter = RateLimiter(rate=2, per=1.0, enabled=True)  # 2 per second

    async def run():
        start = time.monotonic()
        # burst of 2 is free, the next 2 must wait ~0.5s each
        for _ in range(4):
            await limiter.acquire()
        return time.monotonic() - start

    elapsed = asyncio.run(run())
    assert elapsed >= 0.8, elapsed  # roughly 2 * 0.5s of waiting


def test_zero_rate_is_treated_as_disabled():
    limiter = RateLimiter(rate=0, per=60, enabled=True)
    assert limiter.enabled is False
    asyncio.run(limiter.acquire())  # must not hang


def test_env_toggle_parsing():
    import os

    for val, expected in [
        ("off", False),
        ("0", False),
        ("false", False),
        ("no", False),
        ("on", True),
        ("1", True),
        ("30", True),
    ]:
        os.environ["TWIKIT_MCP_RATE_LIMIT"] = val
        assert _env_enabled("TWIKIT_MCP_RATE_LIMIT", True) is expected, val
    del os.environ["TWIKIT_MCP_RATE_LIMIT"]
    assert _env_enabled("TWIKIT_MCP_RATE_LIMIT", True) is True  # default


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"ok  {name}")
    print("all passed")
