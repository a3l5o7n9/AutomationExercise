from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By

from page_classes.base_page import BasePage

class Payment(BasePage):
    def __init__(self, wd: WebDriver, base_url):
        super().__init__(wd, base_url)

    def get_payment_form_element(self):
        return self.find_element(By.ID, 'payment-form')

    def get_specific_payment_form_field(self, field_name):
        payment_form_element = self.get_payment_form_element()
        data_qa = ''
        match field_name:
            case 'name_on_card':
                data_qa = 'name-on-card'
            case 'card_number':
                data_qa = 'card-number'
            case 'cvc':
                data_qa = 'cvc'
            case 'expiry_month':
                data_qa = 'expiry-month'
            case 'expiry_year':
                data_qa = 'expiry-year'
            case _:
                print('Invalid field name')
                return None
        return self.find_element(By.XPATH, f".//input[@data-qa='{data_qa}'][1]", payment_form_element)

    def set_specific_payment_form_field(self, field_name, field_input):
        specific_payment_form_field = self.get_specific_payment_form_field(field_name)
        specific_payment_form_field.clear()
        specific_payment_form_field.send_keys(field_input)

    def get_name_on_card_field(self):
        return self.get_specific_payment_form_field('name_on_card')

    def set_name_on_card_field(self, name_on_card_input):
        self.set_specific_payment_form_field('name_on_card', name_on_card_input)

    def get_card_number_field(self):
        return self.get_specific_payment_form_field('card_number')

    def set_card_number_field(self, card_number_input):
        self.set_specific_payment_form_field('card_number', card_number_input)

    def get_cvc_field(self):
        return self.get_specific_payment_form_field('cvc')

    def set_cvc_field(self, cvc_input):
        self.set_specific_payment_form_field('cvc', cvc_input)

    def get_expiry_month_field(self):
        return self.get_specific_payment_form_field('expiry_month')

    def set_expiry_month_field(self, expiry_month_input):
        self.set_specific_payment_form_field('expiry_month', expiry_month_input)

    def get_expiry_year_field(self):
        return self.get_specific_payment_form_field('expiry_year')

    def set_expiry_year_field(self, expiry_year_input):
        self.set_specific_payment_form_field('expiry_year', expiry_year_input)

    def click_pay_and_confirm_order_button(self):
        submit_button = self.find_element(By.ID, 'submit')
        payment_success_message_element = self.get_order_payment_success_message_element()
        return self.wd.execute_script("arguments[0].click();\nreturn arguments[1].checkVisibility()", submit_button, payment_success_message_element)

    def get_order_payment_success_message_element(self):
        return self.find_element(By.XPATH, "//div[@id='success_message']/div[1]")
