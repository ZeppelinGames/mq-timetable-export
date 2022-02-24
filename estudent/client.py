
import requests
import pyppeteer

from .misc import LOGIN_URL, TIMETABLE_URL, make_soup
from .exceptions import LoginError
from .my_classes_page import MyClassesPage


class Client:
    """Represents a client connection providing access to the eStudent site."""

    TIMEOUT = 10000

    def __init__(self, browser):
        self.session = requests.Session()
        self.browser = browser
        self.page = None

    def request(self, verb, url, *args, timeout=TIMEOUT, **kwargs):
        return self.session.request(verb, url, *args, timeout=timeout, **kwargs)

    def _aspnet_viewstate_params(self, soup):
        param_names = ('__VIEWSTATE', '__VIEWSTATEGENERATOR', '__EVENTVALIDATION')
        return {n: soup.find(id=n)['value'] for n in param_names}

    async def login(self, username, password):
        """
        Parameters
        ----------
        username: str
            Your student ID.
        password: str
            Your eStudent password.
        """
        #resp = self.request('GET', LOGIN_URL, timeout=self.TIMEOUT)
        #soup = make_soup(resp.text)
        self.page = await self.browser.newPage()
        page = self.page
        await page.goto(LOGIN_URL)
        await page.waitForSelector("#okta-signin-username")

        await page.type("#okta-signin-username", username)
        await page.type("#okta-signin-password", password)
        await page.click("#okta-signin-submit")
        try:
            await page.waitForNavigation(timeout=Client.TIMEOUT)
        except: 
            raise LoginError()
        await page.waitForSelector(".cssT1SmBannerLogo")
        #resp = self.request('POST', LOGIN_URL, json=data, allow_redirects=True, timeout=self.TIMEOUT)
        #if resp.status_code != 302:
        #    raise LoginError(resp)

    async def fetch_my_classes_page(self):
        page = self.page
        await page.goto(TIMETABLE_URL)

        text = await page.content()
        soup = make_soup(text)
        if soup.select_one('#loginFormHeader'):
            raise RuntimeError('call `self.login()` first')
        return MyClassesPage(self, text, soup)


'''
print('TEST CLIENT ENABLED')
from pathlib import Path
RESOURCES_DIR = Path(__file__).parent.parent/'tests'/'files'
MY_CLASSES_HTML_FILE = RESOURCES_DIR/'45434344_2019-s1.html'

class Client(Client):
    def __init__(self):
        self.session = None

    def login(self, username, password):
        pass

    def fetch_my_classes_page(self):
        with open(MY_CLASSES_HTML_FILE) as fh:
            page = fh.read()
        return MyClassesPage(self, page)
'''#'''
