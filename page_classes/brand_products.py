from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By

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

