# from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions

from page_classes.base_page import BasePage
from element_classes.features_items import FeaturesItems
from element_classes.filters_menu import FiltersMenu
from element_classes.breadcrumbs import Breadcrumbs

class BrandProducts(BasePage):
    def __init__(self, wd: WebDriver, base_url):
        super().__init__(wd, base_url)
        self.features_items = FeaturesItems(self.wd, self.base_url)
        self.filters_menu = FiltersMenu(self.wd, self.base_url)
        self.breadcrumbs = Breadcrumbs(self.wd, self.base_url)

    def check_url(self):
        try:
            self.wait.until(EC.url_contains('brand_products'))
            return f'{self.base_url}brand_products' in self.wd.current_url
        except selenium.common.exceptions.TimeoutException as e:
            print('Brand Products page was not loaded properly!')
            raise
