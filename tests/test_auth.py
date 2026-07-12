"""
Tests for environment-based authentication resolution in the MCP server.

Focus on the browser-cookie path (TWIKIT_AUTH_TOKEN + TWIKIT_CT0), which is the
most reliable way to authenticate twikit because X's automated login frequently
hits a Cloudflare / browser-verification challenge.
"""
import asyncio
import os

import twikit_mcp.server as server


class FakeClient:
    def __init__(self):
        self.cookies = None
        self.loaded_file = None
        self.logged_in = False

    def set_cookies(self, cookies, clear_cookies=False):
        self.cookies = cookies

    def load_cookies(self, path):
        self.loaded_file = path

    async def login(self, **kwargs):
        self.logged_in = True


def _clear_env():
    for k in ['TWIKIT_AUTH_TOKEN', 'TWIKIT_CT0', 'TWIKIT_COOKIES',
              'TWIKIT_COOKIES_FILE', 'TWIKIT_AUTH_INFO_1', 'TWIKIT_PASSWORD']:
        os.environ.pop(k, None)


def test_auth_token_and_ct0_sets_cookies():
    _clear_env()
    os.environ['TWIKIT_AUTH_TOKEN'] = 'AUTH123'
    os.environ['TWIKIT_CT0'] = 'CT0ABC'
    c = FakeClient()
    asyncio.run(server._authenticate(c))
    assert c.cookies == {'auth_token': 'AUTH123', 'ct0': 'CT0ABC'}
    _clear_env()


def test_raw_cookies_json():
    _clear_env()
    os.environ['TWIKIT_COOKIES'] = '{"auth_token": "X", "ct0": "Y", "extra": "1"}'
    c = FakeClient()
    asyncio.run(server._authenticate(c))
    assert c.cookies['auth_token'] == 'X'
    assert c.cookies['extra'] == '1'
    _clear_env()


def test_invalid_raw_cookies_raises_autherror():
    _clear_env()
    os.environ['TWIKIT_COOKIES'] = 'not-json'
    c = FakeClient()
    try:
        asyncio.run(server._authenticate(c))
        assert False, 'expected AuthError'
    except server.AuthError:
        pass
    finally:
        _clear_env()


def test_no_config_raises_autherror():
    _clear_env()
    c = FakeClient()
    try:
        asyncio.run(server._authenticate(c))
        assert False, 'expected AuthError'
    except server.AuthError as e:
        assert 'TWIKIT_AUTH_TOKEN' in str(e)
    finally:
        _clear_env()


def test_token_takes_precedence_over_login():
    _clear_env()
    os.environ['TWIKIT_AUTH_TOKEN'] = 'A'
    os.environ['TWIKIT_CT0'] = 'B'
    os.environ['TWIKIT_AUTH_INFO_1'] = 'user'
    os.environ['TWIKIT_PASSWORD'] = 'pw'
    c = FakeClient()
    asyncio.run(server._authenticate(c))
    assert c.cookies == {'auth_token': 'A', 'ct0': 'B'}
    assert c.logged_in is False
    _clear_env()


if __name__ == '__main__':
    for name, fn in sorted(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
            print(f'ok  {name}')
    print('all passed')
