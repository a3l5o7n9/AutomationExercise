# from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
import selenium.common.exceptions

from element_classes.base_element import BaseElement
from element_classes.google_ads_elements import GoogleAdsElements

class Breadcrumbs(BaseElement):
    def __init__(self, wd: WebDriver, base_url):
        super().__init__(wd)
        self.base_url = base_url
        self.google_ads_elements = GoogleAdsElements(self.wd, self.base_url)

    def get_breadcrumbs_element(self):
        try:
            return self.find_element(By.XPATH, "//div[@class='breadcrumbs']/ol[@class='breadcrumb']")
        except selenium.common.exceptions as e:
            raise

    def get_breadcrumbs_elements_list(self):
        try:
            breadcrumbs_element = self.get_breadcrumbs_element()
            return breadcrumbs_element.find_elements(By.TAG_NAME, 'li')
        except selenium.common.exceptions as e:
            raise

    def get_breadcrumb_element_at_index(self, breadcrumb_index):
        try:
            breadcrumbs_elements_list = self.get_breadcrumbs_elements_list()
            if len(breadcrumbs_elements_list) > 0 and breadcrumb_index < len(breadcrumbs_elements_list):
                return breadcrumbs_elements_list[breadcrumb_index]
            return None
        except selenium.common.exceptions as e:
            raise
