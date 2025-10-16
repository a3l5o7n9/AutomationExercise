# from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions

from page_classes.base_page import BasePage

class PaymentDone(BasePage):
    def __init__(self, wd: WebDriver, base_url):
        super().__init__(wd, base_url)

    def check_url(self):
        try:
            self.wait.until(EC.url_contains('payment_done'))
            return f'{self.base_url}payment_done' in self.wd.current_url
        except selenium.common.exceptions.TimeoutException as e:
            print('Payment Done page was not loaded properly!')
            raise

    def get_download_invoice_button(self):
        return self.find_element(By.LINK_TEXT, 'Download Invoice')

    def click_download_invoice_button(self):
        download_invoice_button = self.get_download_invoice_button()
        if not download_invoice_button:
            return
        download_invoice_button.click()

    def get_continue_button(self):
        return self.find_element(By.XPATH, "//a[@data-qa='continue-button']")

    def click_continue_button(self):
        continue_button = self.get_continue_button()
        if not continue_button:
            return
        continue_button.click()
