from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from page_classes.base_page import BasePage

class ProductDetails(BasePage):
    def __init__(self, wd: WebDriver, base_url):
        super().__init__(wd, base_url)

    def get_product_information_element(self):
        return self.find_element(By.XPATH,"//div[@class='product-information'][1]")

    def get_product_specific_detail_element(self, detail_name):
        product_information_element = self.get_product_information_element()
        locator_type = By.XPATH
        locator = ""
        match detail_name:
            case 'product_name':
                locator_type = By.TAG_NAME
                locator = 'h2'
            case 'category':
                locator_type = By.TAG_NAME
                locator = 'p'
            case 'price':
                locator_type = By.XPATH
                locator = './/span/span[1]'
            case 'quantity' | 'product_id':
                locator_type = By.ID
                locator = detail_name
            case 'availability':
                locator_type = By.XPATH
                locator = './/p[2]'
            case 'condition':
                locator_type = By.XPATH
                locator = './/p[3]'
            case 'brand':
                locator_type = By.XPATH
                locator = './/p[4]'
            case _:
                print('Invalid detail name')
                return None
        return self.find_element(locator_type, locator, product_information_element)

    def get_product_name_element(self):
        return self.get_product_specific_detail_element('product_name')

    def get_product_name_value(self):
        return self.get_product_name_element().text

    def get_product_category_element(self):
        return self.get_product_specific_detail_element('category')

    def get_product_category_value(self):
        return self.get_product_category_element().text.removeprefix('Category: ')

    def get_product_price_element(self):
        return self.get_product_specific_detail_element('price')

    def get_product_price_value(self):
        return self.get_product_price_element().text

    def get_product_quantity_field(self):
        return self.get_product_specific_detail_element('quantity')

    def get_product_quantity_value(self):
        return self.get_product_quantity_field().get_attribute('value')

    def set_product_quantity_field(self, quantity_input):
        self.google_ads_elements.hide_ads()
        quantity_field = self.get_product_quantity_field()
        quantity_field.clear()
        quantity_field.send_keys(quantity_input)

    def get_product_id_field(self):
        return self.get_product_specific_detail_element('product_id')

    def get_product_id_value(self):
        return self.get_product_id_field().get_attribute('value')

    def get_add_to_cart_button(self):
        product_information_element = self.get_product_information_element()
        return self.find_element(By.XPATH, ".//button[@class='btn btn-default cart'][1]", product_information_element)

    def click_add_to_cart_button(self):
        self.google_ads_elements.hide_ads()
        add_to_cart_button = self.get_add_to_cart_button()
        add_to_cart_button.click()

    def get_product_availability_element(self):
        return self.get_product_specific_detail_element('availability')

    def get_product_availability_value(self):
        return self.get_product_availability_element().text.removeprefix('Availability: ')

    def get_product_condition_element(self):
        return self.get_product_specific_detail_element('condition')

    def get_product_condition_value(self):
        return self.get_product_condition_element().text.removeprefix('Condition: ')

    def get_product_brand_element(self):
        return self.get_product_specific_detail_element('brand')

    def get_product_brand_value(self):
        return self.get_product_brand_element().text.removeprefix('Brand: ')

    def get_write_review_label_element(self):
        return self.find_element(By.LINK_TEXT, 'WRITE YOUR REVIEW')

    def get_specific_write_review_field(self, field_name):
        return self.find_element(By.ID, 'name')

    def set_specific_write_review_field(self, field_name, field_input):
        field_element = self.find_element(By.ID, field_name)
        field_element.clear()
        field_element.send_keys(field_input)

    def get_write_review_name_field(self):
        return self.get_specific_write_review_field('name')

    def get_write_review_email_field(self):
        return self.get_specific_write_review_field('email')

    def get_write_review_review_field(self):
        return self.get_specific_write_review_field('review')

    def set_write_review_name_field(self,name_input):
        self.set_specific_write_review_field('name', name_input)

    def set_write_review_email_field(self, email_input):
        self.set_specific_write_review_field('email', email_input)

    def set_write_review_review_field(self, review_input):
        self.set_specific_write_review_field('review', review_input)

    def get_submit_review_button(self):
        return self.get_specific_write_review_field('button-review')

    def click_submit_review_button(self):
        self.google_ads_elements.hide_ads()
        submit_button = self.get_submit_review_button()
        submit_button.submit()

    def get_review_submission_success_element(self):
        return self.find_element(By.XPATH, "//div[@id='review-section']/div/div/span")

