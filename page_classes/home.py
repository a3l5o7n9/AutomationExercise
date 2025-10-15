# from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions

from page_classes.base_page import BasePage
from element_classes.features_items import FeaturesItems
from element_classes.filters_menu import FiltersMenu

class Home(BasePage):
    def __init__(self, wd: WebDriver, base_url):
        super().__init__(wd, base_url)
        self.features_items = FeaturesItems(self.wd, self.base_url)
        self.filters_menu = FiltersMenu(self.wd, self.base_url)

    def check_url(self):
        return self.wd.current_url == f'{self.base_url}'

    def get_slider_element(self):
        try:
            return self.find_element(By.ID, 'slider')
        except selenium.common.exceptions.TimeoutException as e:
            raise

    def get_active_slider_item_second_header(self):
        try:
            slider_element = self.get_slider_element()
            return self.find_element(By.XPATH, ".//div[@id='slider-carousel']/div/div[@class='item active']/div/h2", slider_element)
        except selenium.common.exceptions.TimeoutException as e:
            raise

    def get_recommended_items_section(self):
        try:
            return self.find_element(By.CSS_SELECTOR, '.recommended_items')
        except selenium.common.exceptions.TimeoutException as e:
            raise

    def get_recommended_items_title_element(self):
        try:
            recommended_items_section = self.get_recommended_items_section()
            return self.find_element(By.XPATH, ".//h2[@class='title text-center']", recommended_items_section)
        except selenium.common.exceptions.TimeoutException as e:
            raise

    def get_recommended_items_list(self):
        try:
            recommended_items_section = self.get_recommended_items_section()
            return recommended_items_section.find_elements(By.XPATH, ".//div[@id='recommended-item-carousel']/div/div")
        except selenium.common.exceptions.TimeoutException as e:
            raise

    def get_specific_recommended_item_element(self, criteria_type, criteria_value):
        try:
            recommended_items_list = self.get_recommended_items_list()
            match criteria_type:
                case 'index':
                    if criteria_value >= len(recommended_items_list):
                        return None
                    return recommended_items_list[criteria_value]
                case 'id':
                    for i in range(0, len(recommended_items_list)):
                        if self.get_specific_recommended_item_id(i) == criteria_value:
                            return recommended_items_list[i]
                    return None
                case _:
                    print('Invalid Criteria Type')
                    return None
        except selenium.common.exceptions.TimeoutException as e:
            raise

    def get_specific_recommended_item_id(self, item_index):
        try:
            specific_recommended_item_element = self.get_specific_recommended_item_element('index',item_index)
            if not specific_recommended_item_element:
                return None
            product_image_element = self.find_element(By.TAG_NAME, 'img', specific_recommended_item_element)
            return product_image_element.get_attribute('src').removeprefix(f'{self.base_url}get_product_picture/')
        except selenium.common.exceptions.TimeoutException as e:
            raise

    def get_specific_recommended_item_add_to_cart_button(self, criteria_type, criteria_value):
        try:
            specific_recommended_item_element = self.get_specific_recommended_item_element(criteria_type, criteria_value)
            if not specific_recommended_item_element:
                return None
            return self.find_element(By.XPATH, ".//a[@class='btn btn-default add-to-cart']", specific_recommended_item_element)
        except selenium.common.exceptions.TimeoutException as e:
            raise

    def get_specific_recommended_item_add_to_cart_button_by_index(self, item_index):
        try:
            return self.get_specific_recommended_item_add_to_cart_button('index', item_index)
        except selenium.common.exceptions.TimeoutException as e:
            raise

    def get_specific_recommended_item_add_to_cart_button_by_id(self, product_id):
        try:
            return self.get_specific_recommended_item_add_to_cart_button('id', product_id)
        except selenium.common.exceptions.TimeoutException as e:
            raise

    def click_specific_recommended_item_add_to_cart_button(self, criteria_type, criteria_value):
        try:
            self.google_ads_elements.hide_ads()
            specific_recommended_item_element = self.get_specific_recommended_item_element(criteria_type, criteria_value)
            if not specific_recommended_item_element:
                return
            specific_recommended_item_atc_button = self.get_specific_recommended_item_add_to_cart_button(criteria_type, criteria_value)
            product_id = ''
            match criteria_type:
                case 'index':
                    product_id = self.get_specific_recommended_item_id(criteria_value)
                case 'id':
                    product_id = criteria_value
                case _:
                    print('Invalid Criteria Type')
            if not specific_recommended_item_element.is_displayed():
                self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//div[@id='recommended-item-carousel']/div/div/div/div/div/div/a[@data-product-id='{product_id}']")))
            specific_recommended_item_atc_button.click()
        except selenium.common.exceptions.TimeoutException as e:
            print(f"Exception in Home 'click_specific_recommended_item_add_to_cart_button()': {e.msg}")
            # raise

    def click_specific_recommended_item_add_to_cart_button_by_index(self, item_index):
        self.click_specific_recommended_item_add_to_cart_button('index', item_index)

    def click_specific_recommended_item_add_to_cart_button_by_id(self, product_id):
        self.click_specific_recommended_item_add_to_cart_button('id', product_id)

