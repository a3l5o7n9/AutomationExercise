# from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions

from element_classes.base_element import BaseElement
from element_classes.google_ads_elements import GoogleAdsElements

class FeaturesItems(BaseElement):
    def __init__(self, wd: WebDriver, base_url):
        super().__init__(wd)
        self.base_url = base_url
        self.google_ads_elements = GoogleAdsElements(self.wd, self.base_url)

    def get_features_items_element(self):
        try:
            return self.find_element(By.XPATH,"//div[@class='features_items'][1]")
        except selenium.common.exceptions.TimeoutException as e:
            raise

    def get_featured_items_header(self):
        try:
            all_products_list_element = self.get_features_items_element()
            return self.find_element(By.XPATH, ".//h2[@class='title text-center'][1]", all_products_list_element)
        except selenium.common.exceptions.TimeoutException as e:
            raise

    def get_features_products_list_items(self):
        try:
            return self.get_features_items_element().find_elements(By.XPATH,".//div[@class='col-sm-4']/div[@class='product-image-wrapper']")
        except selenium.common.exceptions.TimeoutException as e:
            raise

    def get_products_dictionary(self):
        try:
            products_list = self.get_features_products_list_items()
            products_dict = {}
            for i in range(0, len(products_list)):
                product_id = self.get_product_id_by_index(i)
                products_dict[product_id] = i
            return products_dict
        except selenium.common.exceptions.TimeoutException as e:
            raise

    def get_product_id_by_index(self, product_index):
        try:
            products_list = self.get_features_products_list_items()
            add_to_cart_element = self.find_element(By.LINK_TEXT, 'Add to cart', products_list[product_index])
            product_id = add_to_cart_element.get_attribute('data-product-id')
            return product_id
        except selenium.common.exceptions.TimeoutException as e:
            raise

    def get_specific_product_element(self, criteria_type, criteria_value):
        try:
            products_list = self.get_features_products_list_items()
            match criteria_type:
                case 'index':
                    return products_list[criteria_value]
                case 'id':
                    products_dict = self.get_products_dictionary()
                    return products_list[products_dict[criteria_value]]
                case _:
                    print('Invalid criteria')
                    return None
        except selenium.common.exceptions.TimeoutException as e:
            raise

    def get_specific_product_element_by_id(self, product_id):
        try:
            return self.get_specific_product_element('id', product_id)
        except selenium.common.exceptions.TimeoutException as e:
            raise

    def get_specific_product_element_by_index(self, product_index):
        try:
            return self.get_specific_product_element('index', product_index)
        except selenium.common.exceptions.TimeoutException as e:
            raise

    def click_specific_product_button(self, criteria_type, criteria_value, button_text):
        try:
            self.google_ads_elements.hide_ads()
            product_element_index = 0
            match criteria_type:
                case 'id':
                    product_element_index = self.get_products_dictionary()[criteria_value]
                case 'index':
                    product_element_index = int(criteria_value)
            product_element = self.get_specific_product_element(criteria_type, criteria_value)
            button_element = ''
            match button_text:
                case 'Add to cart':
                    button_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[@class='col-sm-4'][{product_element_index + 1}]/div[@class='product-image-wrapper']/div[@class='single-products']/div[@class='product-overlay']/div/a")))
                case 'View Product':
                    button_element = self.find_element(By.LINK_TEXT, button_text, product_element)
                case _:
                    print('Invalid criteria')
                    return
            button_element.click()
        except selenium.common.exceptions.TimeoutException as e:
            raise

    def get_specific_product_detail(self, criteria_type, criteria_value, detail_name):
        try:
            specific_product_element = self.get_specific_product_element(criteria_type, criteria_value)
            match detail_name:
                case 'product_name':
                    return self.find_element(By.XPATH, ".//div[@class='productinfo text-center']/p[1]", specific_product_element)
                case 'product_price':
                    return self.find_element(By.XPATH, ".//div[@class='productinfo text-center']/h2[1]", specific_product_element)
                case _:
                    print('Invalid detail name')
                    return None
        except selenium.common.exceptions.TimeoutException as e:
            raise

    def get_specific_product_name_by_id(self, product_id):
        try:
            return self.get_specific_product_detail('id', product_id, 'product_name').text
        except selenium.common.exceptions.TimeoutException as e:
            raise

    def get_specific_product_name_by_index(self, product_index):
        try:
            return self.get_specific_product_detail('index', product_index, 'product_name').text
        except selenium.common.exceptions.TimeoutException as e:
            raise

    def get_specific_product_price_by_id(self, product_id):
        try:
            return self.get_specific_product_detail('id', product_id, 'product_price').text
        except selenium.common.exceptions.TimeoutException as e:
            raise

    def get_specific_product_price_by_index(self, product_index):
        try:
            return self.get_specific_product_detail('index', product_index, 'product_price').text
        except selenium.common.exceptions.TimeoutException as e:
            raise

    def click_specific_product_add_to_cart_by_id(self, product_id):
        self.click_specific_product_button('id', product_id, 'Add to cart')

    def click_specific_product_add_to_cart_by_index(self, product_index):
        self.click_specific_product_button('index', product_index, 'Add to cart')

    def click_specific_product_view_button_by_id(self, product_id):
        self.click_specific_product_button('id', product_id, 'View Product')

    def click_specific_product_view_button_by_index(self, product_index):
        self.click_specific_product_button('index', product_index, 'View Product')
