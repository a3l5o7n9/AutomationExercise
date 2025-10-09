# from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
import selenium.common.exceptions

from element_classes.base_element import BaseElement
from element_classes.scroll_up_button import ScrollUpButton
from element_classes.navbar import NavBar
from element_classes.google_ads_elements import GoogleAdsElements
from element_classes.subscription import Subscription

class BasePage:
    def __init__(self, wd:WebDriver, base_url):
        self.wd = wd
        self.base_url = base_url
        self.wait = WebDriverWait(self.wd, 10)
        self.base_element = BaseElement(self.wd)
        self.scroll_up_button = ScrollUpButton(self.wd, self.base_url)
        self.navbar = NavBar(self.wd, self.base_url)
        self.google_ads_elements = GoogleAdsElements(self.wd, self.base_url)
        self.subscription = Subscription(self.wd, self.base_url)

    def find_element(self, locator_type, element_locator, start_element:WebElement = None):
        try:
            return self.base_element.find_element(locator_type, element_locator, start_element)
        except selenium.common.exceptions as e:
            raise
