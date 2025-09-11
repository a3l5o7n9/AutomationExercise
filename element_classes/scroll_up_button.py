from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By

from element_classes.base_element import BaseElement
from element_classes.google_ads_elements import GoogleAdsElements

class ScrollUpButton(BaseElement):
    def __init__(self, wd: WebDriver, base_url):
        super().__init__(wd)
        self.base_url = base_url
        self.google_ads_elements = GoogleAdsElements(self.wd, self.base_url)

    def get_scroll_up_button(self):
        return self.find_element(By.ID, 'scrollUp')

    def click_scroll_up_button(self):
        scroll_up_button = self.get_scroll_up_button()
        if not scroll_up_button.is_displayed():
            print('Already at the top of the page')
            return
        scroll_up_button.click()