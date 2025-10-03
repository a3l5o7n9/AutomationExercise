# from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
import selenium.common.exceptions

from element_classes.base_element import BaseElement
from element_classes.google_ads_elements import GoogleAdsElements

class FiltersMenu(BaseElement):
    def __init__(self, wd: WebDriver, base_url):
        super().__init__(wd)
        self.base_url = base_url
        self.google_ads_elements = GoogleAdsElements(self.wd, self.base_url)

    def get_categories_element(self):
        try:
            return self.find_element(By.ID, 'accordian')
        except selenium.common.exceptions as e:
            raise e

    def get_categories_list(self):
        try:
            categories_element = self.find_element(By.ID, 'accordian')
            return categories_element.find_elements(By.XPATH, ".//div/div[@class='panel-heading']/h4/a")
        except selenium.common.exceptions as e:
            raise e

    def get_specific_category_element(self, category_text):
        try:
            categories_list = self.get_categories_list()
            for category_item in categories_list:
                if category_item.get_property('href') == self.wd.current_url + '#' + category_text:
                    return category_item
            return None
        except selenium.common.exceptions as e:
            raise e

    def click_specific_category(self, category_text):
        try:
            self.google_ads_elements.hide_ads()
            category_element = self.get_specific_category_element(category_text)
            if category_element:
                category_element.click()
        except selenium.common.exceptions as e:
            raise e

    def get_subcategories_list(self, base_category_text:str):
        try:
            categories_list = self.get_categories_list()
            for category_element in categories_list:
                if category_element.text == base_category_text.upper():
                    return category_element.find_elements(By.XPATH, f".//../../../div[@id='{base_category_text}']/div/ul/li/a")
            return None
        except selenium.common.exceptions as e:
            raise e

    def get_specific_subcategory_element(self, sub_category_text:str, base_category_text:str):
        try:
            subcategories_list = self.get_subcategories_list(base_category_text)
            for subcategory_item in subcategories_list:
                if subcategory_item.get_attribute('innerHTML').strip(' ') == sub_category_text:
                    return subcategory_item
            return None
        except selenium.common.exceptions as e:
            raise e

    def click_specific_subcategory(self, sub_category_text, base_category_text):
        try:
            self.google_ads_elements.hide_ads()
            sub_category_element = self.get_specific_subcategory_element(sub_category_text, base_category_text)
            if sub_category_element:
                if not sub_category_element.is_displayed():
                    self.click_specific_category(base_category_text)
                sub_category_element.click()
        except selenium.common.exceptions as e:
            raise e

    def get_specific_subcategory_id(self, sub_category_text, base_category_text):
        try:
            sub_category_element = self.get_specific_subcategory_element(sub_category_text, base_category_text)
            if sub_category_element:
                return sub_category_element.get_property('href').removeprefix(f'{self.base_url}category_products/')
            return None
        except selenium.common.exceptions as e:
            raise e

    def get_brands_element(self):
        try:
            return self.find_element(By.XPATH, "//div[@class='brands_products']/div[@class='brands-name']")
        except selenium.common.exceptions as e:
            raise e

    def get_brands_list(self):
        try:
            brands_element = self.get_brands_element()
            return brands_element.find_elements(By.XPATH, ".//ul/li/a")
        except selenium.common.exceptions as e:
            raise e

    def get_specific_brand_element(self, brand_name):
        try:
            brands_list = self.get_brands_list()
            for brand_item in brands_list:
                if brand_item.get_property('href') == self.base_url + 'brand_products/' + brand_name:
                    return brand_item
            return None
        except selenium.common.exceptions as e:
            raise e

    def click_specific_brand(self, brand_name):
        try:
            self.google_ads_elements.hide_ads()
            brand_element = self.get_specific_brand_element(brand_name)
            if brand_element:
                brand_element.click()
        except selenium.common.exceptions as e:
            raise e
