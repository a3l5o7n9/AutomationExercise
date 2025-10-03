# from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from page_classes.base_page import BasePage

class Login(BasePage):
    def __init__(self, wd: WebDriver, base_url):
        super().__init__(wd, base_url)

    def get_signup_form(self):
        return self.find_element(By.XPATH, "//div[@class='signup-form']/form[1]")

    def get_signup_form_header(self):
        return self.find_element(By.XPATH, "//div[@class='signup-form']/h2[1]")

    def get_signup_name_field(self):
        return self.find_element(By.XPATH, "//input[@data-qa='signup-name'][1]")

    def get_signup_email_field(self):
        return self.find_element(By.XPATH, "//input[@data-qa='signup-email'][1]")

    def get_signup_error_element(self):
        return self.find_element(By.XPATH, "//form[@action='/signup']/p[@style='color: red;'][1]")

    def get_signup_submit_button(self):
        return self.find_element(By.XPATH, "//button[@data-qa='signup-button'][1]")

    def set_signup_name_field(self, name_input):
        self.google_ads_elements.hide_ads()
        signup_name_field = self.get_signup_name_field()
        signup_name_field.send_keys(name_input)

    def set_signup_email_field(self, email_input):
        self.google_ads_elements.hide_ads()
        signup_email_field = self.get_signup_email_field()
        signup_email_field.send_keys(email_input)

    def click_signup_submit_button(self):
        self.google_ads_elements.hide_ads()
        signup_submit_button = self.get_signup_submit_button()
        signup_submit_button.click()

    def get_login_form(self):
        return self.find_element(By.XPATH, "//div[@class='login-form']/form[1]")

    def get_login_form_header(self):
        return self.find_element(By.XPATH, "//div[@class='login-form']/h2[1]")

    def get_login_email_field(self):
        return self.find_element(By.XPATH, "//input[@data-qa='login-email'][1]")

    def get_login_password_field(self):
        return self.find_element(By.XPATH, "//input[@data-qa='login-password'][1]")

    def get_login_error_element(self):
        return self.find_element(By.XPATH, "//form[@action='/login']/p[@style='color: red;'][1]")

    def get_login_submit_button(self):
        return self.find_element(By.XPATH, "//button[@data-qa='login-button'][1]")

    def set_login_email_field(self, email_input):
        self.google_ads_elements.hide_ads()
        login_email_field = self.get_login_email_field()
        login_email_field.send_keys(email_input)

    def set_login_password_field(self, password_input):
        self.google_ads_elements.hide_ads()
        login_password_field = self.get_login_password_field()
        login_password_field.send_keys(password_input)

    def click_login_submit_button(self):
        self.google_ads_elements.hide_ads()
        login_submit_button = self.get_login_submit_button()
        login_submit_button.click()

