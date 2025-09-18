from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By

from page_classes.base_page import BasePage

class AccountDeleted(BasePage):
    def __init__(self, wd: WebDriver, base_url):
        super().__init__(wd, base_url)

    def get_account_deleted_header(self):
        return self.find_element(By.XPATH, "//h2[@data-qa='account-deleted'][1]")

    def get_continue_button(self):
        return self.find_element(By.LINK_TEXT, 'Continue')

    def click_continue_button(self):
        self.google_ads_elements.hide_ads()
        continue_button = self.get_continue_button()
        if not continue_button:
            print('Continue button could not be found')
            return
        continue_button.click()
