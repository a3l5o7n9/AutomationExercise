# from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from element_classes.base_element import BaseElement
from element_classes.google_ads_elements import GoogleAdsElements

class Subscription(BaseElement):
    def __init__(self, wd: WebDriver, base_url):
        super().__init__(wd)
        self.base_url = base_url
        self.google_ads_elements = GoogleAdsElements(self.wd, self.base_url)

    def get_footer_element_header(self):
        return self.find_element(By.XPATH, "//div[@class='single-widget']/h2[1]")

    def get_subscribe_email_element(self):
        return self.find_element(By.XPATH, "//form[@class='searchform']/input[2]")

    def get_subscribe_success_message_element(self):
        return self.find_element(By.XPATH, "//div[@id='success-subscribe']/div[@class='alert-success alert'][1]")

    def set_subscribe_email_value(self, email_input):
        subscribe_email_element = self.get_subscribe_email_element()
        subscribe_email_element.clear()
        subscribe_email_element.send_keys(email_input)

    def get_subscribe_submit_button(self):
        return self.find_element(By.ID, 'subscribe')

    def click_subscribe_submit_button(self):
        self.google_ads_elements.hide_ads()
        subscribe_submit_button = self.get_subscribe_submit_button()
        subscribe_submit_button.click()