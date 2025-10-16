# from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions

from page_classes.base_page import BasePage
from element_classes.cart_contents import CartContents
from element_classes.breadcrumbs import Breadcrumbs

class Cart(BasePage):
    def __init__(self, wd: WebDriver, base_url):
        super().__init__(wd, base_url)
        self.cart_contents = CartContents(self.wd, self.base_url, 'cart')
        self.breadcrumbs = Breadcrumbs(self.wd, self.base_url)

    def check_url(self):
        try:
            self.wait.until(EC.url_contains('view_cart'))
            return self.wd.current_url == f'{self.base_url}view_cart'
        except selenium.common.exceptions.TimeoutException as e:
            print('Cart page was not loaded properly!')
            raise

    def get_empty_cart_element(self):
        return self.find_element(By.ID, 'empty_cart')

    def get_cart_contents_table_element(self):
        if self.get_empty_cart_element().is_displayed():
            print('Cart is empty')
            return None
        return self.cart_contents.get_cart_contents_table()

    def get_specific_cart_product_delete_button(self, criteria_type, criteria_value):
        if self.get_empty_cart_element().is_displayed():
            print('Whoops! Cart is already empty!')
            return None
        if len(self.cart_contents.get_products_in_cart_elements_list()) == 0:
            return None
        specific_product_element = self.cart_contents.get_specific_cart_product_element(criteria_type, criteria_value)
        return self.find_element(By.XPATH, ".//td[@class='cart_delete']/a[1]", specific_product_element)

    def click_specific_cart_product_delete_by_id(self, product_id):
        self.google_ads_elements.hide_ads()
        if len(self.cart_contents.get_products_in_cart_elements_list()) == 0:
            return
        specific_product_delete_element = self.get_specific_cart_product_delete_button('id', product_id)
        specific_product_delete_element.click()

    def click_specific_cart_product_delete_by_index(self, product_index):
        self.google_ads_elements.hide_ads()
        if len(self.cart_contents.get_products_in_cart_elements_list()) == 0:
            return
        specific_product_delete_element = self.get_specific_cart_product_delete_button('index', product_index)
        specific_product_delete_element.click()

    def get_proceed_to_checkout_button(self):
        return self.find_element(By.LINK_TEXT, 'Proceed To Checkout')

    def click_proceed_to_checkout_button(self):
        self.google_ads_elements.hide_ads()
        proceed_to_checkout_button = self.get_proceed_to_checkout_button()
        proceed_to_checkout_button.click()
