# from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from page_classes.base_page import BasePage
from element_classes.features_items import FeaturesItems
from element_classes.filters_menu import FiltersMenu

class Products(BasePage):
    def __init__(self, wd: WebDriver, base_url):
        super().__init__(wd, base_url)
        self.features_items = FeaturesItems(self.wd, self.base_url)
        self.filters_menu = FiltersMenu(self.wd, self.base_url)

    def get_search_box_element(self):
        return self.find_element(By.ID, 'search_product')

    def set_search_box_value(self, search_input):
        self.google_ads_elements.hide_ads()
        search_box_element = self.get_search_box_element()
        search_box_element.clear()
        search_box_element.send_keys(search_input)

    def get_search_submit_button(self):
        return self.find_element(By.ID, 'submit_search')

    def click_search_submit_button(self):
        self.google_ads_elements.hide_ads()
        search_submit_button = self.get_search_submit_button()
        search_submit_button.click()
