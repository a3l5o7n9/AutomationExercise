from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class GoogleAdsElements:
    def __init__(self, wd:WebDriver, base_url):
        self.wd = wd
        self.base_url = base_url

    def check_ad_visibility(self, element:WebElement):
        return element.is_displayed()

    def hide_ads(self):
        element_list = self.wd.find_elements(By.XPATH, "//ins[@class='adsbygoogle adsbygoogle-noablate']")
        for ad_element in element_list:
            if self.check_ad_visibility(ad_element):
                self.wd.execute_script("arguments[0].style.display = 'none';", ad_element)