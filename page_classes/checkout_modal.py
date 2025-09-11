from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class CheckoutModal:
    def __init__(self, wd:WebDriver, base_url):
        self.wd = wd
        self.base_url = base_url
        self.wait = WebDriverWait(self.wd, 10)

    def get_checkout_modal(self):
        modal_element = self.wait.until(EC.visibility_of_element_located((By.ID, 'checkoutModal')))
        return modal_element

    def click_continue_on_cart_in_modal(self):
        modal_element = self.get_checkout_modal()
        continue_shopping_button = modal_element.find_element(By.XPATH, ".//button[@class='btn btn-success close-checkout-modal btn-block'][1]")
        continue_shopping_button.click()

    def click_register_login_in_modal(self):
        modal_element = self.get_checkout_modal()
        register_login_element = modal_element.find_element(By.LINK_TEXT, 'Register / Login')
        register_login_element.click()
