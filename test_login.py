from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright import sync_playwright

class MyViewTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()

    def test_login(self):
        page = self.browser.newPage()
        page.goto(f"{self.live_server_url}/admin/")
        page.waitForSelector('text=Django administration')
        page.fill('[name=username]', 'myuser')
        page.fill('[name=password]', 'secret')
        page.click('text=Log in')
        assert len(page.evalOnSelector(".errornote", "el => el.innerText")) > 0
        page.close()
