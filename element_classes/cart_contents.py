# from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
import selenium.common.exceptions

from element_classes.base_element import BaseElement

class CartContents(BaseElement):
    def __init__(self, wd: WebDriver, base_url, page_type):
        super().__init__(wd)
        self.base_url = base_url
        self.page_type = page_type

    def get_cart_contents_table(self):
        try:
            match self.page_type:
                case 'cart':
                    return self.find_element(By.ID, 'cart_info_table')
                case 'checkout':
                    return self.find_element(By.ID, 'cart_info')
                case _:
                    print('Invalid page type')
                    return None
        except selenium.common.exceptions as e:
            raise e

    def get_products_in_cart_elements_list(self):
        try:
            cart_products_table_element = self.get_cart_contents_table()
            cart_product_elements_list = []
            if cart_products_table_element:
                cart_product_elements_list = cart_products_table_element.find_elements(By.XPATH, './/tbody/tr')
            return cart_product_elements_list
        except selenium.common.exceptions as e:
            raise e

    def get_cart_products_dictionary(self):
        try:
            cart_products_list = self.get_products_in_cart_elements_list()
            cart_products_dict = {}
            for i in range(0, len(cart_products_list)):
                product_id = self.get_cart_product_id_by_index(i)
                cart_products_dict[product_id] = i
            return cart_products_dict
        except selenium.common.exceptions as e:
            raise e

    def get_cart_product_id_by_index(self, product_index):
        try:
            cart_products_list = self.get_products_in_cart_elements_list()
            if len(cart_products_list) in (0, product_index):
                return None
            cart_product_element = cart_products_list[product_index]
            product_id = cart_product_element.get_attribute('id').removeprefix('product-')
            return product_id
        except selenium.common.exceptions as e:
            raise e

    def get_specific_cart_product_element(self, criteria_type, criteria_value):
        try:
            cart_products_elements_list = self.get_products_in_cart_elements_list()
            if len(cart_products_elements_list) == 0:
                return None
            cart_products_dict = self.get_cart_products_dictionary()
            match criteria_type:
                case 'id':
                    return cart_products_elements_list[cart_products_dict[criteria_value]]
                case 'index':
                    return cart_products_elements_list[criteria_value]
                case _:
                    print('Invalid criteria')
                    return None
        except selenium.common.exceptions as e:
            raise e

    def get_specific_cart_product_element_by_id(self, product_id):
        try:
            return self.get_specific_cart_product_element('id', product_id)
        except selenium.common.exceptions as e:
            raise e

    def get_specific_cart_product_element_by_index(self, product_index):
        try:
            return self.get_specific_cart_product_element('index', product_index)
        except selenium.common.exceptions as e:
            raise e

    def get_specific_cart_product_detail(self, criteria_type, criteria_value, detail_name):
        try:
            specific_cart_product_element = self.get_specific_cart_product_element(criteria_type, criteria_value)
            match detail_name:
                case 'product_name':
                    return self.find_element(By.XPATH, ".//td[@class='cart_description']/h4/a[1]", specific_cart_product_element)
                case 'product_category':
                    return self.find_element(By.XPATH ,".//td[@class='cart_description']/p[1]", specific_cart_product_element)
                case 'product_price':
                    return self.find_element(By.XPATH, ".//td[@class='cart_price']/p[1]", specific_cart_product_element)
                case 'product_quantity':
                    return self.find_element(By.XPATH, ".//td[@class='cart_quantity']/button[1]", specific_cart_product_element)
                case 'product_total_price':
                    return self.find_element(By.XPATH, ".//td[@class='cart_total']/p[1]", specific_cart_product_element)
                case _:
                    print('Invalid detail name')
                    return None
        except selenium.common.exceptions as e:
            raise e

    def get_specific_cart_product_name_by_id(self, product_id):
        try:
            return self.get_specific_cart_product_detail('id', product_id, 'product_name').text
        except selenium.common.exceptions as e:
            raise e

    def get_specific_cart_product_name_by_index(self, product_index):
        try:
            return self.get_specific_cart_product_detail('index', product_index, 'product_name').text
        except selenium.common.exceptions as e:
            raise e

    def get_specific_cart_product_category_by_id(self, product_id):
        try:
            return self.get_specific_cart_product_detail('id', product_id, 'product_category').text
        except selenium.common.exceptions as e:
            raise e

    def get_specific_cart_product_category_by_index(self, product_index):
        try:
            return self.get_specific_cart_product_detail('index', product_index, 'product_category').text
        except selenium.common.exceptions as e:
            raise e

    def get_specific_cart_product_price_by_id(self, product_id):
        try:
            return self.get_specific_cart_product_detail('id', product_id, 'product_price').text
        except selenium.common.exceptions as e:
            raise e

    def get_specific_cart_product_price_by_index(self, product_index):
        try:
            return self.get_specific_cart_product_detail('index', product_index, 'product_price').text
        except selenium.common.exceptions as e:
            raise e

    def get_specific_cart_product_quantity_by_id(self, product_id):
        try:
            return self.get_specific_cart_product_detail('id', product_id, 'product_quantity').text
        except selenium.common.exceptions as e:
            raise e

    def get_specific_cart_product_quantity_by_index(self, product_index):
        try:
            return self.get_specific_cart_product_detail('index', product_index, 'product_quantity').text
        except selenium.common.exceptions as e:
            raise e

    def get_specific_cart_product_total_price_by_id(self, product_id):
        try:
            return self.get_specific_cart_product_detail('id', product_id, 'product_total_price').text
        except selenium.common.exceptions as e:
            raise e

    def get_specific_cart_product_total_price_by_index(self, product_index):
        try:
            return self.get_specific_cart_product_detail('index', product_index, 'product_total_price').text
        except selenium.common.exceptions as e:
            raise e
