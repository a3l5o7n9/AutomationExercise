import os
# from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions

from page_classes.base_page import BasePage

class ContactUs(BasePage):
    def __init__(self, wd: WebDriver, base_url):
        super().__init__(wd, base_url)

    def check_url(self):
        try:
            self.wait.until(EC.url_contains('contact_us'))
            return self.wd.current_url == f'{self.base_url}contact_us'
        except selenium.common.exceptions.TimeoutException as e:
            print('Contact Us page was not loaded properly!')
            raise

    def get_left_form_header(self):
        return self.find_element(By.XPATH, "//div[@class='contact-form']/h2[1]")

    def get_specific_form_field(self, field_name):
        data_qa = ''
        match field_name:
            case 'name' | 'email' | 'subject' | 'submit-button':
                data_qa = field_name
            case 'message':
                return self.find_element(By.ID, field_name)
            case 'upload_file':
                return self.find_element(By.XPATH, "//input[@name='upload_file'][1]")
            case _:
                print('Invalid field name')
                return None
        return self.find_element(By.XPATH, f"//input[@data-qa='{data_qa}'][1]")

    def get_name_field(self):
        return self.get_specific_form_field('name')

    def get_email_field(self):
        return self.get_specific_form_field('email')

    def get_subject_field(self):
        return self.get_specific_form_field('subject')

    def get_message_field(self):
        return self.get_specific_form_field('message')

    def get_file_upload_field(self):
        return self.get_specific_form_field('upload_file')

    def get_submit_button(self):
        return self.get_specific_form_field('submit-button')

    def set_specific_form_field(self, field_name, field_input):
        self.google_ads_elements.hide_ads()
        form_field_element = self.get_specific_form_field(field_name)
        match field_name:
            case 'upload_file':
                upload_file = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", field_input))
                field_input = upload_file
            case 'submit-button':
                print('Element is not editable')
                return
            case _:
                pass
        form_field_element.clear()
        form_field_element.send_keys(field_input)

    def set_name_field(self, name_input):
        self.set_specific_form_field('name', name_input)

    def set_email_field(self, email_input):
        self.set_specific_form_field('email', email_input)

    def set_subject_field(self, subject_input):
        self.set_specific_form_field('subject', subject_input)

    def set_message_field(self, message_input):
        self.set_specific_form_field('message', message_input)

    def upload_file(self, file_path_input):
        self.set_specific_form_field('upload_file', file_path_input)

    def click_submit_button(self):
        self.google_ads_elements.hide_ads()
        submit_button = self.get_submit_button()
        submit_button.click()

    def click_ok_in_popup(self):
        alert_obj = self.wd.switch_to.alert
        alert_obj.accept()

    def get_success_message_element(self):
        return self.find_element(By.XPATH, "//div[@class='status alert alert-success'][1]")

    def get_success_button(self):
        return self.find_element(By.XPATH, "//a[@class='btn btn-success'][1]")
    def click_success_button(self):
        self.google_ads_elements.hide_ads()
        success_button = self.get_success_button()
        success_button.click()
