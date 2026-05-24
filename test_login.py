import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import expect, sync_playwright


class MyViewTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()

    def test_login(self):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/admin/")
        page.get_by_label("Username:").fill("myuser")
        page.get_by_label("Password:").fill("secret")
        page.get_by_role("button", name="Log in").click()
        expect(page.locator(".errornote")).to_be_visible()
        page.close()
