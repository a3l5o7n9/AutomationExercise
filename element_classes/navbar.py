# from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
import selenium.common.exceptions

from element_classes.base_element import BaseElement
from element_classes.google_ads_elements import GoogleAdsElements

class NavBar(BaseElement):
    def __init__(self, wd: WebDriver, base_url):
        super().__init__(wd)
        self.base_url = base_url
        self.google_ads_elements = GoogleAdsElements(self.wd, self.base_url)

    def get_header(self):
        return self.find_element(By.ID, 'header')

    def get_logo(self):
        try:
            header = self.get_header()
            return self.find_element(By.XPATH, ".//[@class='logo pull-left']/a[1]", header)
        except selenium.common.exceptions as e:
            raise e

    def get_navbar_items(self):
        try:
            header = self.get_header()
            return header.find_elements(By.XPATH, ".//ul[@class='nav navbar-nav']/li/a")
        except selenium.common.exceptions as e:
            raise e

    def click_logo(self):
        self.google_ads_elements.hide_ads()
        try:
            logo = self.get_logo()
            logo.click()
        except selenium.common.exceptions as e:
            raise e

    def click_navbar_item(self, target_text):
        self.google_ads_elements.hide_ads()
        try:
            navbar_list = self.get_navbar_items()
            for navbar_item in navbar_list:
                if target_text in navbar_item.text:
                    navbar_item.click()
                    break
        except selenium.common.exceptions as e:
            raise e

    def get_logged_in_as_element(self):
        try:
            navbar_list = self.get_navbar_items()
            for navbar_item in navbar_list:
                if 'Logged in as ' in navbar_item.text:
                    return navbar_item
            return None
        except selenium.common.exceptions as e:
            raise e
