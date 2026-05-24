# Django end-to-end testing with Playwright

A minimal example of running [Playwright](https://playwright.dev/python/) browser tests inside Django's `StaticLiveServerTestCase`, so you can drive a real browser against a real Django server with `manage.py test`.

## Setup

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12+.

```bash
uv sync
uv run playwright install --with-deps chromium
```

## Run the tests

```bash
DJANGO_ALLOW_ASYNC_UNSAFE=1 uv run python manage.py test
```

## What the example shows

[`test_login.py`](./test_login.py) starts a Chromium browser once per test class, opens Django's admin login page served by the live test server, submits invalid credentials, and asserts the error banner is shown:

```python
def test_login(self):
    page = self.browser.new_page()
    page.goto(f"{self.live_server_url}/admin/")
    page.get_by_label("Username:").fill("myuser")
    page.get_by_label("Password:").fill("secret")
    page.get_by_role("button", name="Log in").click()
    expect(page.locator(".errornote")).to_be_visible()
    page.close()
```

`DJANGO_ALLOW_ASYNC_UNSAFE` is needed because Playwright's sync API runs an event loop, which Django otherwise refuses to allow inside the test runner.

## See also

- [Playwright for Python docs](https://playwright.dev/python/)
- [Django: `LiveServerTestCase`](https://docs.djangoproject.com/en/stable/topics/testing/tools/#liveservertestcase)
