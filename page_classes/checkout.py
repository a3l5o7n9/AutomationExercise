# from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions

from page_classes.base_page import BasePage
from element_classes.cart_contents import CartContents

class Checkout(BasePage):
    def __init__(self, wd: WebDriver, base_url):
        super().__init__(wd, base_url)
        self.cart_contents = CartContents(self.wd, self.base_url, 'checkout')

    def check_url(self):
        try:
            self.wait.until(EC.url_contains('checkout'))
            return self.wd.current_url == f'{self.base_url}checkout'
        except selenium.common.exceptions.TimeoutException as e:
            print('Checkout page was not loaded properly!')
            raise

    def get_address_details_header_element(self):
        return self.find_element(By.XPATH, ".//div[@class='step-one'][1]")

    def get_review_order_header_element(self):
        return self.find_element(By.XPATH, "//div[@class='step-one'][2]")

    def get_address_details_element(self, address_type):
        match address_type:
            case 'address_delivery' | 'address_invoice':
                return self.find_element(By.ID, address_type)
            case _:
                print('Invalid address type')
                return None

    def get_address_specific_details_element(self, details_type, address_type):
        address_details_element = self.get_address_details_element(address_type)
        locator = ""
        match details_type:
            case 'gender_title firstname lastname':
                locator = ".//li[@class='address_firstname address_lastname'][1]"
            case 'company':
                locator = ".//li[@class='address_address1 address_address2'][1]"
            case 'address1':
                locator = ".//li[@class='address_address1 address_address2'][2]"
            case 'address2':
                locator = ".//li[@class='address_address1 address_address2'][3]"
            case 'city state postcode':
                locator = ".//li[@class='address_city address_state_name address_postcode'][1]"
            case 'country':
                locator = ".//li[@class='address_country_name'][1]"
            case 'phone':
                locator = ".//li[@class='address_phone'][1]"
            case _:
                print('Invalid detail type')
                return None
        return self.find_element(By.XPATH, locator, address_details_element)

    def get_address_type_detail_name_value(self, detail_name, address_type):
        specific_details_element = self.get_address_specific_details_element(detail_name, address_type)
        return specific_details_element.text

    def get_address_delivery_gender_title_firstname_lastname(self):
        return self.get_address_type_detail_name_value('gender_title firstname lastname', 'address_delivery')

    def get_address_billing_gender_title_firstname_lastname(self):
        return self.get_address_type_detail_name_value('gender_title firstname lastname', 'address_invoice')

    def get_address_delivery_company(self):
        return self.get_address_type_detail_name_value('company', 'address_delivery')

    def get_address_billing_company(self):
        return self.get_address_type_detail_name_value('company', 'address_invoice')

    def get_address_delivery_address1(self):
        return self.get_address_type_detail_name_value('address1', 'address_delivery')

    def get_address_billing_address1(self):
        return self.get_address_type_detail_name_value('address1', 'address_invoice')

    def get_address_delivery_address2(self):
        return self.get_address_type_detail_name_value('address2', 'address_delivery')

    def get_address_billing_address2(self):
        return self.get_address_type_detail_name_value('address2', 'address_invoice')

    def get_address_delivery_city_state_postcode(self):
        return self.get_address_type_detail_name_value('city state postcode', 'address_delivery')

    def get_address_billing_city_state_postcode(self):
        return self.get_address_type_detail_name_value('city state postcode', 'address_invoice')

    def get_address_delivery_country(self):
        return self.get_address_type_detail_name_value('country', 'address_delivery')

    def get_address_billing_country(self):
        return self.get_address_type_detail_name_value('country', 'address_invoice')

    def get_address_delivery_phone(self):
        return self.get_address_type_detail_name_value('phone', 'address_delivery')

    def get_address_billing_phone(self):
        return self.get_address_type_detail_name_value('phone', 'address_invoice')

    def get_comment_field(self):
        return self.find_element(By.XPATH, "//textarea[@name='message'][1]")

    def set_comment_field(self, comment_input):
        self.google_ads_elements.hide_ads()
        comment_field = self.get_comment_field()
        comment_field.clear()
        comment_field.send_keys(comment_input)

    def click_place_order_button(self):
        self.google_ads_elements.hide_ads()
        self.find_element(By.LINK_TEXT, 'Place Order').click()

