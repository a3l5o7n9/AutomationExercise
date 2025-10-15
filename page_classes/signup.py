import selenium.common.exceptions
# from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from page_classes.base_page import BasePage

class Signup(BasePage):
    def __init__(self, wd: WebDriver, base_url):
        super().__init__(wd, base_url)

    def check_url(self):
        return self.wd.current_url == f'{self.base_url}signup'

    def get_form_section_title(self):
        return self.find_element(By.XPATH, "//div[@class='login-form']/h2")

    def get_form_field_by_id(self, element_id):
        return self.find_element(By.ID, element_id)

    def set_form_field_by_id(self, element_id, field_input):
        self.google_ads_elements.hide_ads()
        element = self.get_form_field_by_id(element_id)
        try:
            element.clear()
            element.send_keys(field_input)
        except selenium.common.exceptions.TimeoutException as e:
            raise
        except selenium.common.exceptions.NoSuchElementException as e:
            raise
        except selenium.common.exceptions.ElementNotInteractableException as e:
            print(f'Minor Bug: {e.msg}')
        except selenium.common.exceptions.InvalidElementStateException as e:
            print(f'Minor Bug: {e.msg}')

    def get_select_field_by_id(self, select_element_id):
        return Select(self.find_element(By.ID, select_element_id))

    def get_select_field_dict_by_id(self, select_element_id):
        self.google_ads_elements.hide_ads()
        select_element = self.get_select_field_by_id(select_element_id)
        select_element_options = select_element.options
        select_element_options_dict = {}
        for select_element_option in select_element_options:
            select_element_options_dict[select_element_option.get_attribute('innerHTML')] = select_element_option.get_attribute('value')
        return select_element_options_dict

    def select_select_field_value(self, select_element_id, select_input):
        self.google_ads_elements.hide_ads()
        select_element = self.get_select_field_by_id(select_element_id)
        select_element_options_dict = self.get_select_field_dict_by_id(select_element_id)
        if select_input not in select_element_options_dict:
            if select_input not in select_element_options_dict.values():
                print(f'{select_input} is not a valid {select_element_id.removesuffix('s')}')
                return
            else:
                select_element.select_by_value(select_input)
                return
        select_element.select_by_visible_text(select_input)

    def get_title_field(self):
        return self.find_element(By.XPATH, "//div[@class='clearfix'][1]")

    def select_gender_title(self, gender_text):
        self.google_ads_elements.hide_ads()
        title_field = self.get_title_field()
        title_radio_elements = title_field.find_elements(By.XPATH, ".//input[@name='title']")
        title_options_list = []
        for title_radio_element in title_radio_elements:
            title_options_list.append(title_radio_element.get_attribute('value'))
        if gender_text not in title_options_list:
            print('Invalid gender')
            return
        gender_locator = ".//input[@value='" + gender_text + "'][1]"
        self.find_element(By.XPATH, gender_locator, title_field).click()

    def get_name_field(self):
        return self.get_form_field_by_id('name')

    def set_name_field(self, name_input):
        self.set_form_field_by_id('name', name_input)

    def get_email_field(self):
        return self.get_form_field_by_id('email')

    def set_email_field(self, email_input):
        self.set_form_field_by_id('email', email_input)

    def get_password_field(self):
        return self.get_form_field_by_id('password')

    def set_password_field(self, password_input):
        self.set_form_field_by_id('password', password_input)

    def get_dob_day_field(self):
        return self.get_form_field_by_id('days')

    def select_dob_day_value(self, day_input):
       self.select_select_field_value('days', day_input)

    def get_dob_month_field(self):
        return self.get_form_field_by_id('months')

    def select_dob_month_value(self, month_input):
        self.select_select_field_value('months', month_input)

    def get_dob_year_field(self):
        return self.get_form_field_by_id('years')

    def select_dob_year_value(self, year_input):
        self.select_select_field_value('years', year_input)

    def get_newsletter_checkbox(self):
        return self.get_form_field_by_id('newsletter')

    def click_newsletter_checkbox(self):
        self.google_ads_elements.hide_ads()
        newsletter_checkbox = self.get_newsletter_checkbox()
        newsletter_checkbox.click()

    def get_opt_in_checkbox(self):
        return self.get_form_field_by_id('optin')

    def click_opt_in_checkbox(self):
        self.google_ads_elements.hide_ads()
        opt_in_checkbox = self.get_opt_in_checkbox()
        opt_in_checkbox.click()

    def get_first_name_field(self):
        return self.get_form_field_by_id('first_name')

    def set_first_name_field(self, first_name_input):
        self.set_form_field_by_id('first_name', first_name_input)

    def get_last_name_field(self):
        return self.get_form_field_by_id('last_name')

    def set_last_name_field(self, last_name_input):
        self.set_form_field_by_id('last_name', last_name_input)

    def get_company_field(self):
        return self.get_form_field_by_id('company')

    def set_company_field(self,  company_input):
        self.set_form_field_by_id('company', company_input)

    def get_address1_field(self):
        return self.get_form_field_by_id('address1')

    def set_address1_field(self, address1_input):
        self.set_form_field_by_id('address1', address1_input)

    def get_address2_field(self):
        return self.get_form_field_by_id('address2')

    def set_address2_field(self, address2_input):
        self.set_form_field_by_id('address2', address2_input)

    def get_country_field(self):
        return self.get_form_field_by_id('country')

    def select_country_value(self, country_input):
        self.select_select_field_value('country', country_input)

    def get_state_field(self):
        return self.get_form_field_by_id('state')

    def set_state_field(self, state_input):
        self.set_form_field_by_id('state', state_input)

    def get_city_field(self):
        return self.get_form_field_by_id('city')

    def set_city_field(self, city_input):
        self.set_form_field_by_id('city', city_input)

    def get_zipcode_field(self):
        return self.get_form_field_by_id('zipcode')

    def set_zipcode_field(self, zipcode_input):
        self.set_form_field_by_id('zipcode', zipcode_input)

    def get_mobile_number_field(self):
        return self.get_form_field_by_id('mobile_number')

    def set_mobile_number_field(self, mobile_number_input):
        self.set_form_field_by_id('mobile_number', mobile_number_input)

    def get_submit_button(self):
        return self.find_element(By.XPATH, "//button[@data-qa='create-account'][1]")

    def click_submit_button(self):
        self.google_ads_elements.hide_ads()
        submit_button = self.get_submit_button()
        submit_button.click()
