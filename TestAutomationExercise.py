from unittest import TestCase
import os
from time import sleep, time

# from selenium.webdriver.firefox.webdriver import WebDriver
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
# import selenium.common.exceptions
from object_classes.user import User
from helper_functions.api_actions import check_existence_of_user_via_api, create_user_via_api, delete_user_via_api
from helper_functions.empty_cart_gui import empty_cart
import json

from element_classes.cart_modal import CartModal
from page_classes.home import Home
from page_classes.login import Login
from page_classes.signup import Signup
from page_classes.account_created import AccountCreated
from page_classes.account_deleted import AccountDeleted
from page_classes.contact_us import ContactUs
from page_classes.products import Products
from page_classes.category_products import CategoryProducts
from page_classes.brand_products import BrandProducts
from page_classes.product_details import ProductDetails
from page_classes.cart import Cart
from element_classes.checkout_modal import CheckoutModal
from page_classes.checkout import Checkout
from page_classes.payment import Payment
from page_classes.payment_done import PaymentDone

class TestAutomationExercise(TestCase):
    def setUp(self):
        # print("Entered 'setUp()'")
        with open('test_data/users.json') as test_data:
            data = json.load(test_data)
            self.users_data = data['users']

        self.download_path = os.path.join(os.getcwd(), 'downloads')
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)
        self.user1 = User(self.users_data[0])
        self.user2 = User(self.users_data[1])

        self.base_url = 'https://automationexercise.com/'

        if check_existence_of_user_via_api(self.user1):
            delete_user_via_api(self.user1)

        if check_existence_of_user_via_api(self.user2):
            delete_user_via_api(self.user2)

        if not check_existence_of_user_via_api(self.user2):
            create_user_via_api(self.user2)

        try:
            empty_cart(self.base_url)
        except TypeError as e:
            print(f"Exception in 'setUp()': {e}")

        prefs = {
            "download.default_directory": self.download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "profile.password_manager_leak_detection": False
        }

        self.options = Options()
        self.options.add_experimental_option("prefs", prefs)
        # For Firefox
        # self.options.set_preference('browser.download.folderList', 2)
        # self.options.set_preference('browser.download.dir', self.download_path)
        # self.options.set_preference('browser.download.manager.showWhenStarting', False)
        # self.options.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/plain')
        self.options.add_argument("--headless")
        self.wd = WebDriver(self.options)
        self.wd.get(self.base_url)
        self.wd.maximize_window()
        self.wd.implicitly_wait(10)
        self.wait = WebDriverWait(self.wd, 10)
        self.ac = ActionChains(self.wd)
        self.cart_modal = CartModal(self.wd, self.base_url)
        self.home = Home(self.wd, self.base_url)
        self.login = Login(self.wd, self.base_url)
        self.signup = Signup(self.wd, self.base_url)
        self.account_created = AccountCreated(self.wd, self.base_url)
        self.account_deleted = AccountDeleted(self.wd, self.base_url)
        self.contact_us = ContactUs(self.wd, self.base_url)
        self.products = Products(self.wd, self.base_url)
        self.category_products = CategoryProducts(self.wd, self.base_url)
        self.brand_products = BrandProducts(self.wd, self.base_url)
        self.product_details = ProductDetails(self.wd, self.base_url)
        self.cart = Cart(self.wd, self.base_url)
        self.checkout_modal = CheckoutModal(self.wd, self.base_url)
        self.checkout = Checkout(self.wd, self.base_url)
        self.payment = Payment(self.wd, self.base_url)
        self.payment_done = PaymentDone(self.wd, self.base_url)
        # print("Exiting 'setUp()'")

    def test_register_user(self):
        self.assertTrue(self.home.get_slider_element().is_displayed())
        self.home.navbar.click_navbar_item('Signup / Login')
        self.assertTrue(self.login.get_signup_form_header().is_displayed())
        self.login.set_signup_name_field(self.user1.username)
        self.login.set_signup_email_field(self.user1.email)
        self.login.click_signup_submit_button()
        if not self.signup.check_url():
            sleep(1)
        self.assertTrue(self.signup.get_form_section_title().is_displayed())
        self.signup.select_gender_title(self.user1.title)
        self.signup.set_name_field(self.user1.username)
        self.signup.set_email_field(self.user1.email)
        self.signup.set_password_field(self.user1.password)
        self.signup.select_dob_day_value(self.user1.dob_day)
        self.signup.select_dob_month_value(self.user1.dob_month)
        self.signup.select_dob_year_value(self.user1.dob_year)
        self.signup.click_newsletter_checkbox()
        self.signup.click_opt_in_checkbox()
        self.signup.set_first_name_field(self.user1.first_name)
        self.signup.set_last_name_field(self.user1.last_name)
        self.signup.set_company_field(self.user1.company)
        self.signup.set_address1_field(self.user1.address1)
        self.signup.set_address2_field(self.user1.address2)
        self.signup.select_country_value(self.user1.country)
        self.signup.set_state_field(self.user1.state)
        self.signup.set_city_field(self.user1.city)
        self.signup.set_zipcode_field(self.user1.zipcode)
        self.signup.set_mobile_number_field(self.user1.mobile_number)
        self.signup.click_submit_button()
        self.assertTrue(self.account_created.get_account_created_header().is_displayed())
        self.account_created.click_continue_button()
        self.assertEqual(self.home.navbar.get_logged_in_as_element().text, f'Logged in as {self.user1.username}')
        self.home.navbar.click_navbar_item('Delete Account')
        self.assertTrue(self.account_deleted.get_account_deleted_header().is_displayed())
        self.account_deleted.click_continue_button()

    def test_login_with_correct_credentials(self):
        self.assertTrue(self.home.get_slider_element().is_displayed())
        self.home.navbar.click_navbar_item('Signup / Login')
        self.assertTrue(self.login.get_login_form_header().is_displayed())
        self.login.set_login_email_field(self.user2.email)
        self.login.set_login_password_field(self.user2.password)
        self.login.click_login_submit_button()
        self.assertEqual(self.home.navbar.get_logged_in_as_element().text, f'Logged in as {self.user2.username}')
        self.home.navbar.click_navbar_item('Delete Account')
        self.assertTrue(self.account_deleted.get_account_deleted_header().is_displayed())

    def test_login_with_incorrect_credentials(self):
        incorrect_email = 'tester3@goo.com'
        incorrect_password = 'Testing'
        self.assertTrue(self.home.get_slider_element().is_displayed())
        self.home.navbar.click_navbar_item('Signup / Login')
        self.assertTrue(self.login.get_login_form_header().is_displayed())
        self.login.set_login_email_field(incorrect_email)
        self.login.set_login_password_field(incorrect_password)
        self.login.click_login_submit_button()
        self.assertTrue(self.login.get_login_error_element().is_displayed())

    def test_logout_user(self):
        self.assertTrue(self.home.get_slider_element().is_displayed())
        self.home.navbar.click_navbar_item('Signup / Login')
        self.assertTrue(self.login.get_login_form_header().is_displayed())
        self.login.set_login_email_field(self.user2.email)
        self.login.set_login_password_field(self.user2.password)
        self.login.click_login_submit_button()
        self.assertEqual(self.home.navbar.get_logged_in_as_element().text, f'Logged in as {self.user2.username}')
        self.home.navbar.click_navbar_item('Logout')
        self.assertEqual(self.wd.current_url, f'{self.base_url}login')
        # self.delete_user(self.user2.email)

    def test_register_user_with_existing_email(self):
        username = 'Tester3'
        home_slider_element = self.home.get_slider_element()
        if not home_slider_element:
            print('Something went wrong! the page was not displayed properly.')
        self.assertTrue(home_slider_element.is_displayed())
        self.home.navbar.click_navbar_item('Signup / Login')
        self.assertTrue(self.login.get_signup_form_header().is_displayed())
        self.login.set_signup_name_field(username)
        self.login.set_signup_email_field(self.user2.email)
        self.login.click_signup_submit_button()
        self.assertTrue(self.login.get_signup_error_element().is_displayed())

    def test_contact_us_form(self):
        home_slider_element = self.home.get_slider_element()
        if not home_slider_element:
            print('Something went wrong! the page was not displayed properly.')
        self.assertTrue(home_slider_element.is_displayed())
        self.home.navbar.click_navbar_item('Contact us')
        self.assertTrue(self.contact_us.get_left_form_header().is_displayed())
        self.contact_us.set_name_field(self.user1.first_name)
        self.contact_us.set_email_field(self.user1.email)
        self.contact_us.set_subject_field('Technical Issue')
        self.contact_us.set_message_field("Hello. I've been experiencing some difficulties using the site.")
        self.contact_us.upload_file('test_data/stub.txt')
        self.contact_us.click_submit_button()
        self.contact_us.click_ok_in_popup()
        self.assertTrue(self.contact_us.get_success_message_element().is_displayed())
        self.contact_us.click_success_button()
        self.assertTrue(self.home.get_slider_element().is_displayed())

    def test_test_cases_page(self):
        self.assertTrue(self.home.get_slider_element().is_displayed())
        self.home.navbar.click_navbar_item('Test Cases')
        self.assertEqual(self.wd.current_url, f'{self.base_url}test_cases')

    def test_all_products_and_product_details_pages(self):
        self.assertTrue(self.home.get_slider_element().is_displayed())
        self.home.navbar.click_navbar_item('Products')
        self.assertEqual(self.wd.current_url, f'{self.base_url}products')
        self.assertTrue(self.products.features_items.get_features_items_element().is_displayed())
        product_id = self.products.features_items.get_product_id_by_index(0)
        self.products.features_items.click_specific_product_view_button_by_index(0)
        self.assertEqual(self.wd.current_url, f'{self.base_url}product_details/{product_id}')
        self.assertTrue(self.product_details.get_product_name_element().is_displayed())
        self.assertTrue(self.product_details.get_product_category_element().is_displayed())
        self.assertTrue(self.product_details.get_product_price_element().is_displayed())
        self.assertTrue(self.product_details.get_product_availability_element().is_displayed())
        self.assertTrue(self.product_details.get_product_condition_element().is_displayed())
        self.assertTrue(self.product_details.get_product_brand_element().is_displayed())

    def test_search_product(self):
        target_product_name = 'tshirt'
        self.assertTrue(self.home.get_slider_element().is_displayed())
        self.home.navbar.click_navbar_item('Products')
        self.assertEqual(self.wd.current_url, f'{self.base_url}products')
        target_products_names_list = []
        all_products_list = self.products.features_items.get_features_products_list_items()
        for i in range(0, len(all_products_list)):
            product_name = self.products.features_items.get_specific_product_name_by_index(i)
            if target_product_name in product_name.replace(' ', '').replace('-', '').lower():
                target_products_names_list.append(product_name)
        self.products.set_search_box_value(target_product_name)
        self.products.click_search_submit_button()
        self.assertEqual(self.products.features_items.get_featured_items_header().text, 'SEARCHED PRODUCTS')
        filtered_shirts_names_list = []
        filtered_products_list = self.products.features_items.get_features_products_list_items()
        for i in range(0, len(filtered_products_list)):
            product_name = self.products.features_items.get_specific_product_name_by_index(i)
            if target_product_name in product_name.replace(' ', '').replace('-', '').lower():
                filtered_shirts_names_list.append(product_name)
        self.assertEqual(len(filtered_products_list), len(target_products_names_list))
        self.assertEqual(target_products_names_list, filtered_shirts_names_list)

    def test_verify_subscription_in_home_page(self):
        self.assertTrue(self.home.get_slider_element().is_displayed())
        self.wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.assertEqual(self.home.subscription.get_footer_element_header().text, 'SUBSCRIPTION')
        self.home.subscription.set_subscribe_email_value(self.user1.email)
        self.home.subscription.click_subscribe_submit_button()
        self.assertTrue(self.home.subscription.get_subscribe_success_message_element().is_displayed())

    def test_verify_subscription_in_cart_page(self):
        home_slider_element = self.home.get_slider_element()
        if not home_slider_element:
            print('Something went wrong! the page was not displayed properly.')
        self.assertTrue(home_slider_element.is_displayed())
        self.home.navbar.click_navbar_item('Cart')
        self.wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.assertEqual(self.cart.subscription.get_footer_element_header().text, 'SUBSCRIPTION')
        self.cart.subscription.set_subscribe_email_value(self.user1.email)
        self.cart.subscription.click_subscribe_submit_button()
        self.assertTrue(self.cart.subscription.get_subscribe_success_message_element().is_displayed())

    def test_add_products_to_cart(self):
        self.assertTrue(self.home.get_slider_element().is_displayed())
        self.home.navbar.click_navbar_item('Products')
        product1_id = self.products.features_items.get_product_id_by_index(0)
        product1_name = self.products.features_items.get_specific_product_name_by_index(0)
        product1_price = self.products.features_items.get_specific_product_price_by_index(0)
        product1_quantity = 1
        product1_total_price = int(product1_price[product1_price.index(' ') + 1 :]) * product1_quantity
        product1_total_price_str = product1_price[0 : product1_price.index(' ') + 1] + str(product1_total_price)
        product2_id = self.products.features_items.get_product_id_by_index(1)
        product2_name = self.products.features_items.get_specific_product_name_by_index(1)
        product2_price = self.products.features_items.get_specific_product_price_by_index(1)
        product2_quantity = 1
        product2_total_price = int(product2_price[product2_price.index(' ') + 1 :]) * product2_quantity
        product2_total_price_str = product2_price[0 : product2_price.index(' ') + 1] + str(product2_total_price)
        self.ac.move_to_element(self.products.features_items.get_specific_product_element_by_index(0)).perform()
        self.products.features_items.click_specific_product_add_to_cart_by_index(0)
        self.cart_modal.click_continue_in_modal()
        self.ac.move_to_element(self.products.features_items.get_specific_product_element_by_index(1)).perform()
        self.products.features_items.click_specific_product_add_to_cart_by_index(1)
        self.cart_modal.click_view_cart_in_modal()
        cart_products_list = self.cart.cart_contents.get_products_in_cart_elements_list()
        cart_products_id_list = []
        for cp in range(0, len(cart_products_list)):
            cart_products_id_list.append(self.cart.cart_contents.get_cart_product_id_by_index(cp))
        self.assertIn(product1_id, cart_products_id_list)
        self.assertIn(product2_id, cart_products_id_list)
        cart_product1_price = self.cart.cart_contents.get_specific_cart_product_price_by_id(product1_id)
        cart_product1_quantity = self.cart.cart_contents.get_specific_cart_product_quantity_by_id(product1_id)
        cart_product1_total_price = self.cart.cart_contents.get_specific_cart_product_total_price_by_id(product1_id)
        cart_product2_price = self.cart.cart_contents.get_specific_cart_product_price_by_id(product2_id)
        cart_product2_quantity = self.cart.cart_contents.get_specific_cart_product_quantity_by_id(product2_id)
        cart_product2_total_price = self.cart.cart_contents.get_specific_cart_product_total_price_by_id(product2_id)
        self.assertEqual(product1_price, cart_product1_price)
        self.assertEqual(str(product1_quantity), cart_product1_quantity)
        self.assertEqual(product1_total_price_str, cart_product1_total_price)
        self.assertEqual(product2_price, cart_product2_price)
        self.assertEqual(str(product2_quantity), cart_product2_quantity)
        self.assertEqual(product2_total_price_str, cart_product2_total_price)

    def test_product_quantity_in_cart(self):
        self.assertTrue(self.home.get_slider_element().is_displayed())
        product_id = '5'
        product_name = self.home.features_items.get_specific_product_name_by_id(product_id)
        product_quantity = '4'
        self.home.features_items.click_specific_product_view_button_by_id(product_id)
        self.assertEqual(self.wd.current_url, f'{self.base_url}product_details/{product_id}')
        self.assertTrue(self.product_details.get_product_name_element().is_displayed())
        self.assertTrue(self.product_details.get_product_category_element().is_displayed())
        self.assertTrue(self.product_details.get_product_price_element().is_displayed())
        self.assertTrue(self.product_details.get_product_availability_element().is_displayed())
        self.assertTrue(self.product_details.get_product_condition_element().is_displayed())
        self.assertTrue(self.product_details.get_product_brand_element().is_displayed())
        self.product_details.set_product_quantity_field(product_quantity)
        self.product_details.click_add_to_cart_button()
        self.cart_modal.click_view_cart_in_modal()
        cart_product_name = self.cart.cart_contents.get_specific_cart_product_name_by_id(product_id)
        cart_product_quantity = self.cart.cart_contents.get_specific_cart_product_quantity_by_id(product_id)
        self.assertEqual(product_name, cart_product_name)
        self.assertEqual(product_quantity, cart_product_quantity)

    def test_placing_order_with_registration_during_checkout(self):
        self.assertTrue(self.home.get_slider_element().is_displayed())
        self.home.navbar.click_navbar_item('Products')
        product1_id = self.products.features_items.get_product_id_by_index(0)
        product1_name = self.products.features_items.get_specific_product_name_by_index(0)
        product1_price = self.products.features_items.get_specific_product_price_by_index(0)
        product1_quantity = 1
        product1_total_price = int(product1_price[product1_price.index(' ') + 1:]) * product1_quantity
        product1_total_price_str = product1_price[0: product1_price.index(' ') + 1] + str(product1_total_price)
        product2_id = self.products.features_items.get_product_id_by_index(1)
        product2_name = self.products.features_items.get_specific_product_name_by_index(1)
        product2_price = self.products.features_items.get_specific_product_price_by_index(1)
        product2_quantity = 1
        product2_total_price = int(product2_price[product2_price.index(' ') + 1:]) * product2_quantity
        product2_total_price_str = product2_price[0: product2_price.index(' ') + 1] + str(product2_total_price)
        self.ac.move_to_element(self.products.features_items.get_specific_product_element_by_index(0)).perform()
        self.products.features_items.click_specific_product_add_to_cart_by_index(0)
        self.cart_modal.click_continue_in_modal()
        self.ac.move_to_element(self.products.features_items.get_specific_product_element_by_index(1)).perform()
        self.products.features_items.click_specific_product_add_to_cart_by_index(1)
        self.cart_modal.click_continue_in_modal()
        self.products.navbar.click_navbar_item('Cart')
        self.assertTrue(self.cart.get_cart_contents_table_element().is_displayed())
        self.cart.click_proceed_to_checkout_button()
        self.checkout_modal.click_register_login_in_modal()
        self.login.set_signup_name_field(self.user1.username)
        self.login.set_signup_email_field(self.user1.email)
        self.login.click_signup_submit_button()
        if not self.signup.check_url():
            sleep(1)
        self.signup.select_gender_title(self.user1.title)
        self.signup.set_name_field(self.user1.username)
        self.signup.set_email_field(self.user1.email)
        self.signup.set_password_field(self.user1.password)
        self.signup.select_dob_day_value(self.user1.dob_day)
        self.signup.select_dob_month_value(self.user1.dob_month)
        self.signup.select_dob_year_value(self.user1.dob_year)
        self.signup.click_newsletter_checkbox()
        self.signup.click_opt_in_checkbox()
        self.signup.set_first_name_field(self.user1.first_name)
        self.signup.set_last_name_field(self.user1.last_name)
        self.signup.set_company_field(self.user1.company)
        self.signup.set_address1_field(self.user1.address1)
        self.signup.set_address2_field(self.user1.address2)
        self.signup.select_country_value(self.user1.country)
        self.signup.set_state_field(self.user1.state)
        self.signup.set_city_field(self.user1.city)
        self.signup.set_zipcode_field(self.user1.zipcode)
        self.signup.set_mobile_number_field(self.user1.mobile_number)
        self.signup.click_submit_button()
        self.assertTrue(self.account_created.get_account_created_header().is_displayed())
        self.account_created.click_continue_button()
        self.assertEqual(self.home.navbar.get_logged_in_as_element().text, f'Logged in as {self.user1.username}')
        self.home.navbar.click_navbar_item('Cart')
        self.cart.click_proceed_to_checkout_button()
        self.assertTrue(self.checkout.get_address_details_header_element().is_displayed())
        self.assertTrue(self.checkout.get_review_order_header_element().is_displayed())
        checkout_product1_name = self.checkout.cart_contents.get_specific_cart_product_name_by_id(product1_id)
        checkout_product1_price = self.checkout.cart_contents.get_specific_cart_product_price_by_id(product1_id)
        checkout_product1_quantity = self.checkout.cart_contents.get_specific_cart_product_quantity_by_id(product1_id)
        checkout_product1_total_price = self.checkout.cart_contents.get_specific_cart_product_total_price_by_id(product1_id)
        checkout_product2_name = self.checkout.cart_contents.get_specific_cart_product_name_by_id(product2_id)
        checkout_product2_price = self.checkout.cart_contents.get_specific_cart_product_price_by_id(product2_id)
        checkout_product2_quantity = self.checkout.cart_contents.get_specific_cart_product_quantity_by_id(product2_id)
        checkout_product2_total_price = self.checkout.cart_contents.get_specific_cart_product_total_price_by_id(product2_id)
        self.assertEqual(product1_name, checkout_product1_name)
        self.assertEqual(product1_price, checkout_product1_price)
        self.assertEqual(str(product1_quantity), checkout_product1_quantity)
        self.assertEqual(product1_total_price_str, checkout_product1_total_price)
        self.assertEqual(product2_name, checkout_product2_name)
        self.assertEqual(product2_price, checkout_product2_price)
        self.assertEqual(str(product2_quantity), checkout_product2_quantity)
        self.assertEqual(product2_total_price_str, checkout_product2_total_price)
        self.checkout.set_comment_field('This is a test order')
        self.checkout.click_place_order_button()
        name_on_card = self.user1.first_name + ' ' + self.user1.last_name
        card_number = '1234567890123456'
        cvc = '123'
        expiry_month = '12'
        expiry_year = '2028'
        self.payment.set_name_on_card_field(name_on_card)
        self.payment.set_card_number_field(card_number)
        self.payment.set_cvc_field(cvc)
        self.payment.set_expiry_month_field(expiry_month)
        self.payment.set_expiry_year_field(expiry_year)
        is_success_message_displayed = self.payment.click_pay_and_confirm_order_button()
        self.assertTrue(is_success_message_displayed)
        self.payment_done.navbar.click_navbar_item('Delete Account')
        self.assertTrue(self.account_deleted.get_account_deleted_header().is_displayed())
        self.account_deleted.click_continue_button()

    def test_placing_order_with_registration_before_checkout(self):
        self.assertTrue(self.home.get_slider_element().is_displayed())
        self.home.navbar.click_navbar_item('Signup / Login')
        self.login.set_signup_name_field(self.user1.username)
        self.login.set_signup_email_field(self.user1.email)
        self.login.click_signup_submit_button()
        if not self.signup.check_url():
            sleep(1)
        self.signup.select_gender_title(self.user1.title)
        self.signup.set_name_field(self.user1.username)
        self.signup.set_email_field(self.user1.email)
        self.signup.set_password_field(self.user1.password)
        self.signup.select_dob_day_value(self.user1.dob_day)
        self.signup.select_dob_month_value(self.user1.dob_month)
        self.signup.select_dob_year_value(self.user1.dob_year)
        self.signup.click_newsletter_checkbox()
        self.signup.click_opt_in_checkbox()
        self.signup.set_first_name_field(self.user1.first_name)
        self.signup.set_last_name_field(self.user1.last_name)
        self.signup.set_company_field(self.user1.company)
        self.signup.set_address1_field(self.user1.address1)
        self.signup.set_address2_field(self.user1.address2)
        self.signup.select_country_value(self.user1.country)
        self.signup.set_state_field(self.user1.state)
        self.signup.set_city_field(self.user1.city)
        self.signup.set_zipcode_field(self.user1.zipcode)
        self.signup.set_mobile_number_field(self.user1.mobile_number)
        self.signup.click_submit_button()
        self.assertTrue(self.account_created.get_account_created_header().is_displayed())
        self.account_created.click_continue_button()
        self.assertEqual(self.home.navbar.get_logged_in_as_element().text, f'Logged in as {self.user1.username}')
        self.home.navbar.click_navbar_item('Products')
        product1_id = self.products.features_items.get_product_id_by_index(0)
        product1_name = self.products.features_items.get_specific_product_name_by_index(0)
        product1_price = self.products.features_items.get_specific_product_price_by_index(0)
        product1_quantity = 1
        product1_total_price = int(product1_price[product1_price.index(' ') + 1:]) * product1_quantity
        product1_total_price_str = product1_price[0: product1_price.index(' ') + 1] + str(product1_total_price)
        product2_id = self.products.features_items.get_product_id_by_index(1)
        product2_name = self.products.features_items.get_specific_product_name_by_index(1)
        product2_price = self.products.features_items.get_specific_product_price_by_index(1)
        product2_quantity = 1
        product2_total_price = int(product2_price[product2_price.index(' ') + 1:]) * product2_quantity
        product2_total_price_str = product2_price[0: product2_price.index(' ') + 1] + str(product2_total_price)
        self.ac.move_to_element(self.products.features_items.get_specific_product_element_by_index(0)).perform()
        self.products.features_items.click_specific_product_add_to_cart_by_index(0)
        self.cart_modal.click_continue_in_modal()
        self.ac.move_to_element(self.products.features_items.get_specific_product_element_by_index(1)).perform()
        self.products.features_items.click_specific_product_add_to_cart_by_index(1)
        self.cart_modal.click_continue_in_modal()
        self.products.navbar.click_navbar_item('Cart')
        self.assertTrue(self.cart.get_cart_contents_table_element().is_displayed())
        self.cart.click_proceed_to_checkout_button()
        self.assertTrue(self.checkout.get_address_details_header_element().is_displayed())
        self.assertTrue(self.checkout.get_review_order_header_element().is_displayed())
        checkout_product1_name = self.checkout.cart_contents.get_specific_cart_product_name_by_id(product1_id)
        checkout_product1_price = self.checkout.cart_contents.get_specific_cart_product_price_by_id(product1_id)
        checkout_product1_quantity = self.checkout.cart_contents.get_specific_cart_product_quantity_by_id(product1_id)
        checkout_product1_total_price = self.checkout.cart_contents.get_specific_cart_product_total_price_by_id(product1_id)
        checkout_product2_name = self.checkout.cart_contents.get_specific_cart_product_name_by_id(product2_id)
        checkout_product2_price = self.checkout.cart_contents.get_specific_cart_product_price_by_id(product2_id)
        checkout_product2_quantity = self.checkout.cart_contents.get_specific_cart_product_quantity_by_id(product2_id)
        checkout_product2_total_price = self.checkout.cart_contents.get_specific_cart_product_total_price_by_id(product2_id)
        self.assertEqual(product1_name, checkout_product1_name)
        self.assertEqual(product1_price, checkout_product1_price)
        self.assertEqual(str(product1_quantity), checkout_product1_quantity)
        self.assertEqual(product1_total_price_str, checkout_product1_total_price)
        self.assertEqual(product2_name, checkout_product2_name)
        self.assertEqual(product2_price, checkout_product2_price)
        self.assertEqual(str(product2_quantity), checkout_product2_quantity)
        self.assertEqual(product2_total_price_str, checkout_product2_total_price)
        self.checkout.set_comment_field('This is a test order')
        self.checkout.click_place_order_button()
        name_on_card = self.user1.first_name + ' ' + self.user1.last_name
        card_number = '1234567890123456'
        cvc = '123'
        expiry_month = '12'
        expiry_year = '2028'
        self.payment.set_name_on_card_field(name_on_card)
        self.payment.set_card_number_field(card_number)
        self.payment.set_cvc_field(cvc)
        self.payment.set_expiry_month_field(expiry_month)
        self.payment.set_expiry_year_field(expiry_year)
        is_success_message_displayed = self.payment.click_pay_and_confirm_order_button()
        self.assertTrue(is_success_message_displayed)
        self.payment_done.navbar.click_navbar_item('Delete Account')
        self.assertTrue(self.account_deleted.get_account_deleted_header().is_displayed())
        self.account_deleted.click_continue_button()

    def test_placing_order_checkout_after_login(self):
        self.assertTrue(self.home.get_slider_element().is_displayed())
        self.home.navbar.click_navbar_item('Signup / Login')
        self.assertTrue(self.login.get_login_form_header().is_displayed())
        self.login.set_login_email_field(self.user2.email)
        self.login.set_login_password_field(self.user2.password)
        self.login.click_login_submit_button()
        self.assertEqual(self.home.navbar.get_logged_in_as_element().text, f'Logged in as {self.user2.username}')
        self.home.navbar.click_navbar_item('Products')
        product1_id = self.products.features_items.get_product_id_by_index(0)
        product1_name = self.products.features_items.get_specific_product_name_by_index(0)
        product1_price = self.products.features_items.get_specific_product_price_by_index(0)
        product1_quantity = 1
        product1_total_price = int(product1_price[product1_price.index(' ') + 1:]) * product1_quantity
        product1_total_price_str = product1_price[0: product1_price.index(' ') + 1] + str(product1_total_price)
        product2_id = self.products.features_items.get_product_id_by_index(1)
        product2_name = self.products.features_items.get_specific_product_name_by_index(1)
        product2_price = self.products.features_items.get_specific_product_price_by_index(1)
        product2_quantity = 1
        product2_total_price = int(product2_price[product2_price.index(' ') + 1:]) * product2_quantity
        product2_total_price_str = product2_price[0: product2_price.index(' ') + 1] + str(product2_total_price)
        self.ac.move_to_element(self.products.features_items.get_specific_product_element_by_index(0)).perform()
        self.products.features_items.click_specific_product_add_to_cart_by_index(0)
        self.cart_modal.click_continue_in_modal()
        self.ac.move_to_element(self.products.features_items.get_specific_product_element_by_index(1)).perform()
        self.products.features_items.click_specific_product_add_to_cart_by_index(1)
        self.cart_modal.click_continue_in_modal()
        self.products.navbar.click_navbar_item('Cart')
        self.assertTrue(self.cart.get_cart_contents_table_element().is_displayed())
        cart_product1_name = self.cart.cart_contents.get_specific_cart_product_name_by_id(product1_id)
        cart_product1_price = self.cart.cart_contents.get_specific_cart_product_price_by_id(product1_id)
        cart_product1_quantity = self.cart.cart_contents.get_specific_cart_product_quantity_by_id(product1_id)
        cart_product1_total_price = self.cart.cart_contents.get_specific_cart_product_total_price_by_id(product1_id)
        cart_product2_name = self.cart.cart_contents.get_specific_cart_product_name_by_id(product2_id)
        cart_product2_price = self.cart.cart_contents.get_specific_cart_product_price_by_id(product2_id)
        cart_product2_quantity = self.cart.cart_contents.get_specific_cart_product_quantity_by_id(product2_id)
        cart_product2_total_price = self.cart.cart_contents.get_specific_cart_product_total_price_by_id(product2_id)
        self.assertEqual(product1_name, cart_product1_name)
        self.assertEqual(product1_price, cart_product1_price)
        self.assertEqual(str(product1_quantity), cart_product1_quantity)
        self.assertEqual(product1_total_price_str, cart_product1_total_price)
        self.assertEqual(product2_name, cart_product2_name)
        self.assertEqual(product2_price, cart_product2_price)
        self.assertEqual(str(product2_quantity), cart_product2_quantity)
        self.assertEqual(product2_total_price_str, cart_product2_total_price)
        self.cart.click_proceed_to_checkout_button()
        address_delivery_gender_title_firstname_lastname = self.checkout.get_address_delivery_gender_title_firstname_lastname()
        address_delivery_company = self.checkout.get_address_delivery_company()
        address_delivery_address1 = self.checkout.get_address_delivery_address1()
        address_delivery_address2 = self.checkout.get_address_delivery_address2()
        address_delivery_city_state_postcode = self.checkout.get_address_delivery_city_state_postcode()
        address_delivery_country = self.checkout.get_address_delivery_country()
        address_delivery_phone = self.checkout.get_address_delivery_phone()
        address_billing_gender_title_firstname_lastname = self.checkout.get_address_billing_gender_title_firstname_lastname()
        address_billing_company = self.checkout.get_address_billing_company()
        address_billing_address1 = self.checkout.get_address_billing_address1()
        address_billing_address2 = self.checkout.get_address_billing_address2()
        address_billing_city_state_postcode = self.checkout.get_address_billing_city_state_postcode()
        address_billing_country = self.checkout.get_address_billing_country()
        address_billing_phone = self.checkout.get_address_billing_phone()
        self.assertEqual(address_delivery_gender_title_firstname_lastname,f'{self.user2.title}. {self.user2.first_name} {self.user2.last_name}')
        self.assertEqual(address_billing_gender_title_firstname_lastname,f'{self.user2.title}. {self.user2.first_name} {self.user2.last_name}')
        self.assertEqual(address_delivery_company, self.user2.company)
        self.assertEqual(address_billing_company, self.user2.company)
        self.assertEqual(address_delivery_address1, self.user2.address1)
        self.assertEqual(address_billing_address1, self.user2.address1)
        self.assertEqual(address_delivery_address2, self.user2.address2)
        self.assertEqual(address_billing_address2, self.user2.address2)
        self.assertEqual(address_delivery_city_state_postcode,f'{self.user2.city} {self.user2.state} {self.user2.zipcode}')
        self.assertEqual(address_billing_city_state_postcode,f'{self.user2.city} {self.user2.state} {self.user2.zipcode}')
        self.assertEqual(address_delivery_country, self.user2.country)
        self.assertEqual(address_billing_country, self.user2.country)
        self.assertEqual(address_delivery_phone, self.user2.mobile_number)
        self.assertEqual(address_billing_phone, self.user2.mobile_number)
        checkout_product1_name = self.checkout.cart_contents.get_specific_cart_product_name_by_id(product1_id)
        checkout_product1_price = self.checkout.cart_contents.get_specific_cart_product_price_by_id(product1_id)
        checkout_product1_quantity = self.checkout.cart_contents.get_specific_cart_product_quantity_by_id(product1_id)
        checkout_product1_total_price = self.checkout.cart_contents.get_specific_cart_product_total_price_by_id(product1_id)
        checkout_product2_name = self.checkout.cart_contents.get_specific_cart_product_name_by_id(product2_id)
        checkout_product2_price = self.checkout.cart_contents.get_specific_cart_product_price_by_id(product2_id)
        checkout_product2_quantity = self.checkout.cart_contents.get_specific_cart_product_quantity_by_id(product2_id)
        checkout_product2_total_price = self.checkout.cart_contents.get_specific_cart_product_total_price_by_id(product2_id)
        self.assertEqual(product1_name, checkout_product1_name)
        self.assertEqual(product1_price, checkout_product1_price)
        self.assertEqual(str(product1_quantity), checkout_product1_quantity)
        self.assertEqual(product1_total_price_str, checkout_product1_total_price)
        self.assertEqual(product2_name, checkout_product2_name)
        self.assertEqual(product2_price, checkout_product2_price)
        self.assertEqual(str(product2_quantity), checkout_product2_quantity)
        self.assertEqual(product2_total_price_str, checkout_product2_total_price)
        self.checkout.set_comment_field('This is a test order')
        self.checkout.click_place_order_button()
        name_on_card = self.user2.first_name + ' ' + self.user2.last_name
        card_number = '1234567890123456'
        cvc = '123'
        expiry_month = '12'
        expiry_year = '2028'
        self.payment.set_name_on_card_field(name_on_card)
        self.payment.set_card_number_field(card_number)
        self.payment.set_cvc_field(cvc)
        self.payment.set_expiry_month_field(expiry_month)
        self.payment.set_expiry_year_field(expiry_year)
        is_success_message_displayed = self.payment.click_pay_and_confirm_order_button()
        self.assertTrue(is_success_message_displayed)
        self.payment_done.navbar.click_navbar_item('Delete Account')
        self.assertTrue(self.account_deleted.get_account_deleted_header().is_displayed())
        self.account_deleted.click_continue_button()

    def test_remove_products_from_cart(self):
        self.assertTrue(self.home.get_slider_element().is_displayed())
        self.home.navbar.click_navbar_item('Products')
        product1_id = self.products.features_items.get_product_id_by_index(0)
        product1_name = self.products.features_items.get_specific_product_name_by_index(0)
        product2_id = self.products.features_items.get_product_id_by_index(1)
        product2_name = self.products.features_items.get_specific_product_name_by_index(1)
        self.ac.move_to_element(self.products.features_items.get_specific_product_element_by_index(0)).perform()
        self.products.features_items.click_specific_product_add_to_cart_by_index(0)
        self.cart_modal.click_continue_in_modal()
        self.ac.move_to_element(self.products.features_items.get_specific_product_element_by_index(1)).perform()
        self.products.features_items.click_specific_product_add_to_cart_by_index(1)
        self.cart_modal.click_continue_in_modal()
        self.products.navbar.click_navbar_item('Cart')
        self.assertTrue(self.cart.get_cart_contents_table_element().is_displayed())
        cart_products_list = self.cart.cart_contents.get_products_in_cart_elements_list()
        cart_products_names = []
        for ib in range (0, len(cart_products_list)):
            cart_products_names.append(self.cart.cart_contents.get_specific_cart_product_name_by_index(ib))
        cart_product1_name = self.cart.cart_contents.get_specific_cart_product_name_by_id(product1_id)
        cart_product2_name = self.cart.cart_contents.get_specific_cart_product_name_by_id(product2_id)
        self.assertEqual(product1_name, cart_product1_name)
        self.assertEqual(product2_name, cart_product2_name)
        self.cart.click_specific_cart_product_delete_by_id(product1_id)
        sleep(2)
        cart_products_names_after_removal = []
        cart_products_list = self.cart.cart_contents.get_products_in_cart_elements_list()
        for ia in range(0,len(cart_products_list)):
            cart_products_names_after_removal.append(self.cart.cart_contents.get_specific_cart_product_name_by_index(ia))
        self.assertNotIn(product1_name, cart_products_names_after_removal)
        self.wd.refresh()
        cart_products_names_after_refresh = []
        cart_products_list = self.cart.cart_contents.get_products_in_cart_elements_list()
        for iar in range(0, len(cart_products_list)):
            cart_products_names_after_refresh.append(self.cart.cart_contents.get_specific_cart_product_name_by_index(iar))
        self.assertNotIn(product1_name, cart_products_names_after_refresh)

    def test_view_category_products(self):
        base_category1 = 'Women'
        sub_category1 = 'Tops'
        base_category2 = 'Men'
        sub_category2 = 'Tshirts'
        self.assertTrue(self.home.get_slider_element().is_displayed())
        self.assertTrue(self.home.filters_menu.get_categories_element().is_displayed())
        self.home.filters_menu.click_specific_category(base_category1)
        sub_category1_id = self.home.filters_menu.get_specific_subcategory_id(sub_category1, base_category1)
        self.home.filters_menu.click_specific_subcategory(sub_category1, base_category1)
        self.assertEqual(sub_category1_id, self.wd.current_url.removeprefix(f'{self.base_url}category_products/'))
        final_breadcrumb_element = self.category_products.breadcrumbs.get_breadcrumb_element_at_index(-1)
        self.assertTrue(final_breadcrumb_element.is_displayed())
        self.assertEqual(final_breadcrumb_element.text, f'{base_category1} > {sub_category1}')
        page_title = self.category_products.features_items.get_featured_items_header()
        self.assertEqual(page_title.text, f'{base_category1} - {sub_category1} Products'.upper())
        self.category_products.filters_menu.click_specific_category(base_category2)
        sub_category2_id = self.category_products.filters_menu.get_specific_subcategory_id(sub_category2, base_category2)
        self.category_products.filters_menu.click_specific_subcategory(sub_category2, base_category2)
        self.assertEqual(sub_category2_id, self.wd.current_url.removeprefix(f'{self.base_url}category_products/'))

    def test_view_brand_products(self):
        brand1 = 'Madame'
        brand2 = 'Polo'
        self.assertTrue(self.home.get_slider_element().is_displayed())
        self.home.navbar.click_navbar_item('Products')
        self.assertTrue(self.products.filters_menu.get_brands_element().is_displayed())
        self.products.filters_menu.click_specific_brand(brand1)
        self.assertEqual(self.wd.current_url, f'{self.base_url}brand_products/{brand1}')
        final_breadcrumb_element = self.brand_products.breadcrumbs.get_breadcrumb_element_at_index(-1)
        self.assertTrue(final_breadcrumb_element.is_displayed())
        self.assertEqual(final_breadcrumb_element.text, brand1)
        brand_products_list = self.brand_products.features_items.get_features_products_list_items()
        self.assertGreater(len(brand_products_list), 0)
        self.brand_products.filters_menu.click_specific_brand(brand2)
        self.assertEqual(self.wd.current_url, f'{self.base_url}brand_products/{brand2}')
        final_breadcrumb_element = self.brand_products.breadcrumbs.get_breadcrumb_element_at_index(-1)
        self.assertTrue(final_breadcrumb_element.is_displayed())
        self.assertEqual(final_breadcrumb_element.text, brand2)
        brand_products_list = self.brand_products.features_items.get_features_products_list_items()
        self.assertGreater(len(brand_products_list), 0)

    def test_search_products_and_verify_cart_after_login(self):
        target_product_name = 'tshirt'
        self.home.navbar.click_navbar_item('Products')
        self.assertEqual(self.wd.current_url, f'{self.base_url}products')
        category_products_names_list = []
        all_products_list = self.products.features_items.get_features_products_list_items()
        for j in range(0, len(all_products_list)):
            product_name = self.products.features_items.get_specific_product_name_by_index(j)
            if target_product_name in product_name.replace(' ', '').replace('-', '').lower():
                category_products_names_list.append(product_name)
        self.products.set_search_box_value(target_product_name)
        self.products.click_search_submit_button()
        self.assertEqual(self.products.features_items.get_featured_items_header().text, 'SEARCHED PRODUCTS')
        filtered_products_names_list = []
        filtered_products_list = self.products.features_items.get_features_products_list_items()
        for j in range(0, len(filtered_products_list)):
            product_name = self.products.features_items.get_specific_product_name_by_index(j)
            if target_product_name in product_name.replace('-', '').replace(' ', '').lower():
                filtered_products_names_list.append(product_name)
                self.wd.execute_script('arguments[0].scrollIntoView();', filtered_products_list[j])
                self.ac.move_to_element(self.products.features_items.get_specific_product_element_by_index(j)).perform()
                self.products.features_items.click_specific_product_add_to_cart_by_index(j)
                self.cart_modal.click_continue_in_modal()
        self.assertEqual(len(category_products_names_list), len(filtered_products_names_list))
        self.products.navbar.click_navbar_item('Cart')
        self.assertTrue(self.cart.cart_contents.get_cart_contents_table().is_displayed())
        cart_products_list = self.cart.cart_contents.get_products_in_cart_elements_list()
        cart_products_names_list = []
        for cp in range(0, len(cart_products_list)):
            cart_product_name = self.cart.cart_contents.get_specific_cart_product_name_by_index(cp)
            cart_products_names_list.append(cart_product_name)
        self.assertEqual(len(cart_products_list), len(cart_products_names_list))
        self.assertEqual(len(cart_products_names_list), len(filtered_products_names_list))
        self.assertEqual(cart_products_names_list, filtered_products_names_list)
        self.cart.navbar.click_navbar_item('Signup / Login')
        self.assertEqual(self.wd.current_url, f'{self.base_url}login')
        self.login.set_login_email_field(self.user2.email)
        self.login.set_login_password_field(self.user2.password)
        self.login.click_login_submit_button()
        self.assertEqual(self.home.navbar.get_logged_in_as_element().text, f'Logged in as {self.user2.username}')
        self.home.navbar.click_navbar_item('Cart')
        self.assertTrue(self.cart.cart_contents.get_cart_contents_table().is_displayed())
        cart_products_list_after_login = self.cart.cart_contents.get_products_in_cart_elements_list()
        cart_products_names_list_after_login = []
        for cpal in range(0, len(cart_products_list_after_login)):
            cart_products_names_list_after_login.append(self.cart.cart_contents.get_specific_cart_product_name_by_index(cpal))
        self.assertEqual(cart_products_names_list_after_login, cart_products_names_list)

    def test_add_review_on_product(self):
        self.home.navbar.click_navbar_item('Products')
        self.assertEqual(self.wd.current_url, f'{self.base_url}products')
        self.assertTrue(self.products.features_items.get_features_items_element().is_displayed())
        self.products.features_items.click_specific_product_view_button_by_index(0)
        write_review_label = self.product_details.get_write_review_label_element().text
        self.assertEqual(write_review_label, 'WRITE YOUR REVIEW')
        self.product_details.set_write_review_name_field(self.user1.username)
        self.product_details.set_write_review_email_field(self.user1.email)
        self.product_details.set_write_review_review_field('Testing...')
        submit_review_button = self.product_details.get_submit_review_button()
        self.wd.execute_script('arguments[0].scrollIntoView();', submit_review_button)
        self.product_details.click_submit_review_button()
        success_message_element = self.product_details.get_review_submission_success_element()
        self.assertTrue(success_message_element.is_displayed())
        self.assertEqual(success_message_element.text, 'Thank you for your review.')

    def test_add_to_cart_from_recommended_items(self):
        self.wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        recommended_items_title_element = self.home.get_recommended_items_title_element()
        self.assertTrue(recommended_items_title_element.is_displayed())
        self.assertEqual(recommended_items_title_element.text, 'RECOMMENDED ITEMS')
        product_id = self.home.get_specific_recommended_item_id(0)
        self.home.click_specific_recommended_item_add_to_cart_button_by_id(product_id)
        self.cart_modal.click_view_cart_in_modal()
        self.assertTrue(self.cart.cart_contents.get_cart_contents_table().is_displayed())
        cart_product_element = self.cart.cart_contents.get_specific_cart_product_element('id', product_id)
        self.assertTrue(cart_product_element.is_displayed())

    def test_verify_address_details_in_checkout_page(self):
        self.assertTrue(self.home.get_slider_element().is_displayed())
        self.home.navbar.click_navbar_item('Signup / Login')
        self.login.set_signup_name_field(self.user1.username)
        self.login.set_signup_email_field(self.user1.email)
        self.login.click_signup_submit_button()
        if not self.signup.check_url():
            sleep(1)
        self.signup.select_gender_title(self.user1.title)
        self.signup.set_name_field(self.user1.username)
        self.signup.set_email_field(self.user1.email)
        self.signup.set_password_field(self.user1.password)
        self.signup.select_dob_day_value(self.user1.dob_day)
        self.signup.select_dob_month_value(self.user1.dob_month)
        self.signup.select_dob_year_value(self.user1.dob_year)
        self.signup.click_newsletter_checkbox()
        self.signup.click_opt_in_checkbox()
        self.signup.set_first_name_field(self.user1.first_name)
        self.signup.set_last_name_field(self.user1.last_name)
        self.signup.set_company_field(self.user1.company)
        self.signup.set_address1_field(self.user1.address1)
        self.signup.set_address2_field(self.user1.address2)
        self.signup.select_country_value(self.user1.country)
        self.signup.set_state_field(self.user1.state)
        self.signup.set_city_field(self.user1.city)
        self.signup.set_zipcode_field(self.user1.zipcode)
        self.signup.set_mobile_number_field(self.user1.mobile_number)
        self.signup.click_submit_button()
        self.assertTrue(self.account_created.get_account_created_header().is_displayed())
        self.account_created.click_continue_button()
        self.assertEqual(self.home.navbar.get_logged_in_as_element().text, f'Logged in as {self.user1.username}')
        self.home.navbar.click_navbar_item('Products')
        self.ac.move_to_element(self.products.features_items.get_specific_product_element_by_index(0)).perform()
        self.products.features_items.click_specific_product_add_to_cart_by_index(0)
        self.cart_modal.click_continue_in_modal()
        self.ac.move_to_element(self.products.features_items.get_specific_product_element_by_index(1)).perform()
        self.products.features_items.click_specific_product_add_to_cart_by_index(1)
        self.cart_modal.click_continue_in_modal()
        self.products.navbar.click_navbar_item('Cart')
        self.assertTrue(self.cart.get_cart_contents_table_element().is_displayed())
        self.cart.click_proceed_to_checkout_button()
        self.assertTrue(self.checkout.get_address_details_header_element().is_displayed())
        self.assertTrue(self.checkout.get_review_order_header_element().is_displayed())
        address_delivery_gender_title_firstname_lastname = self.checkout.get_address_delivery_gender_title_firstname_lastname()
        address_delivery_company = self.checkout.get_address_delivery_company()
        address_delivery_address1 = self.checkout.get_address_delivery_address1()
        address_delivery_address2 = self.checkout.get_address_delivery_address2()
        address_delivery_city_state_postcode = self.checkout.get_address_delivery_city_state_postcode()
        address_delivery_country = self.checkout.get_address_delivery_country()
        address_delivery_phone = self.checkout.get_address_delivery_phone()
        address_billing_gender_title_firstname_lastname = self.checkout.get_address_billing_gender_title_firstname_lastname()
        address_billing_company = self.checkout.get_address_billing_company()
        address_billing_address1 = self.checkout.get_address_billing_address1()
        address_billing_address2 = self.checkout.get_address_billing_address2()
        address_billing_city_state_postcode = self.checkout.get_address_billing_city_state_postcode()
        address_billing_country = self.checkout.get_address_billing_country()
        address_billing_phone = self.checkout.get_address_billing_phone()
        self.assertEqual(address_delivery_gender_title_firstname_lastname,f'{self.user1.title}. {self.user1.first_name} {self.user1.last_name}')
        self.assertEqual(address_billing_gender_title_firstname_lastname,f'{self.user1.title}. {self.user1.first_name} {self.user1.last_name}')
        self.assertEqual(address_delivery_company, self.user1.company)
        self.assertEqual(address_billing_company, self.user1.company)
        self.assertEqual(address_delivery_address1, self.user1.address1)
        self.assertEqual(address_billing_address1, self.user1.address1)
        self.assertEqual(address_delivery_address2, self.user1.address2)
        self.assertEqual(address_billing_address2, self.user1.address2)
        self.assertEqual(address_delivery_city_state_postcode,f'{self.user1.city} {self.user1.state} {self.user1.zipcode}')
        self.assertEqual(address_billing_city_state_postcode,f'{self.user1.city} {self.user1.state} {self.user1.zipcode}')
        self.assertEqual(address_delivery_country, self.user1.country)
        self.assertEqual(address_billing_country, self.user1.country)
        self.assertEqual(address_delivery_phone, self.user1.mobile_number)
        self.assertEqual(address_billing_phone, self.user1.mobile_number)
        self.checkout.navbar.click_navbar_item('Delete Account')
        self.assertTrue(self.account_deleted.get_account_deleted_header().is_displayed())
        self.account_deleted.click_continue_button()

    def test_download_invoice_after_purchase(self):
        self.assertTrue(self.home.get_slider_element().is_displayed())
        self.home.navbar.click_navbar_item('Products')
        product1_id = self.products.features_items.get_product_id_by_index(0)
        product1_name = self.products.features_items.get_specific_product_name_by_index(0)
        product1_price = self.products.features_items.get_specific_product_price_by_index(0)
        product1_quantity = 1
        product1_total_price = int(product1_price[product1_price.index(' ') + 1:]) * product1_quantity
        product1_total_price_str = product1_price[0: product1_price.index(' ') + 1] + str(product1_total_price)
        product2_id = self.products.features_items.get_product_id_by_index(1)
        product2_name = self.products.features_items.get_specific_product_name_by_index(1)
        product2_price = self.products.features_items.get_specific_product_price_by_index(1)
        product2_quantity = 1
        product2_total_price = int(product2_price[product2_price.index(' ') + 1:]) * product2_quantity
        product2_total_price_str = product2_price[0: product2_price.index(' ') + 1] + str(product2_total_price)
        self.ac.move_to_element(self.products.features_items.get_specific_product_element_by_index(0)).perform()
        self.products.features_items.click_specific_product_add_to_cart_by_index(0)
        self.cart_modal.click_continue_in_modal()
        self.ac.move_to_element(self.products.features_items.get_specific_product_element_by_index(1)).perform()
        self.products.features_items.click_specific_product_add_to_cart_by_index(1)
        self.cart_modal.click_continue_in_modal()
        self.products.navbar.click_navbar_item('Cart')
        self.assertTrue(self.cart.get_cart_contents_table_element().is_displayed())
        self.cart.click_proceed_to_checkout_button()
        self.checkout_modal.click_register_login_in_modal()
        self.login.set_signup_name_field(self.user1.username)
        self.login.set_signup_email_field(self.user1.email)
        self.login.click_signup_submit_button()
        if not self.signup.check_url():
            sleep(1)
        self.signup.select_gender_title(self.user1.title)
        self.signup.set_name_field(self.user1.username)
        self.signup.set_email_field(self.user1.email)
        self.signup.set_password_field(self.user1.password)
        self.signup.select_dob_day_value(self.user1.dob_day)
        self.signup.select_dob_month_value(self.user1.dob_month)
        self.signup.select_dob_year_value(self.user1.dob_year)
        self.signup.click_newsletter_checkbox()
        self.signup.click_opt_in_checkbox()
        self.signup.set_first_name_field(self.user1.first_name)
        self.signup.set_last_name_field(self.user1.last_name)
        self.signup.set_company_field(self.user1.company)
        self.signup.set_address1_field(self.user1.address1)
        self.signup.set_address2_field(self.user1.address2)
        self.signup.select_country_value(self.user1.country)
        self.signup.set_state_field(self.user1.state)
        self.signup.set_city_field(self.user1.city)
        self.signup.set_zipcode_field(self.user1.zipcode)
        self.signup.set_mobile_number_field(self.user1.mobile_number)
        self.signup.click_submit_button()
        self.assertTrue(self.account_created.get_account_created_header().is_displayed())
        self.account_created.click_continue_button()
        self.assertEqual(self.home.navbar.get_logged_in_as_element().text, f'Logged in as {self.user1.username}')
        self.home.navbar.click_navbar_item('Cart')
        self.cart.click_proceed_to_checkout_button()
        self.assertTrue(self.checkout.get_address_details_header_element().is_displayed())
        self.assertTrue(self.checkout.get_review_order_header_element().is_displayed())
        checkout_product1_name = self.checkout.cart_contents.get_specific_cart_product_name_by_id(product1_id)
        checkout_product1_price = self.checkout.cart_contents.get_specific_cart_product_price_by_id(product1_id)
        checkout_product1_quantity = self.checkout.cart_contents.get_specific_cart_product_quantity_by_id(product1_id)
        checkout_product1_total_price = self.checkout.cart_contents.get_specific_cart_product_total_price_by_id(product1_id)
        checkout_product2_name = self.checkout.cart_contents.get_specific_cart_product_name_by_id(product2_id)
        checkout_product2_price = self.checkout.cart_contents.get_specific_cart_product_price_by_id(product2_id)
        checkout_product2_quantity = self.checkout.cart_contents.get_specific_cart_product_quantity_by_id(product2_id)
        checkout_product2_total_price = self.checkout.cart_contents.get_specific_cart_product_total_price_by_id(product2_id)
        self.assertEqual(product1_name, checkout_product1_name)
        self.assertEqual(product1_price, checkout_product1_price)
        self.assertEqual(str(product1_quantity), checkout_product1_quantity)
        self.assertEqual(product1_total_price_str, checkout_product1_total_price)
        self.assertEqual(product2_name, checkout_product2_name)
        self.assertEqual(product2_price, checkout_product2_price)
        self.assertEqual(str(product2_quantity), checkout_product2_quantity)
        self.assertEqual(product2_total_price_str, checkout_product2_total_price)
        self.checkout.set_comment_field('This is a test order')
        self.checkout.click_place_order_button()
        name_on_card = self.user1.first_name + ' ' + self.user1.last_name
        card_number = '1234567890123456'
        cvc = '123'
        expiry_month = '12'
        expiry_year = '2028'
        self.payment.set_name_on_card_field(name_on_card)
        self.payment.set_card_number_field(card_number)
        self.payment.set_cvc_field(cvc)
        self.payment.set_expiry_month_field(expiry_month)
        self.payment.set_expiry_year_field(expiry_year)
        is_success_message_displayed = self.payment.click_pay_and_confirm_order_button()
        self.assertTrue(is_success_message_displayed)
        self.payment_done.click_download_invoice_button()
        expected_filename = 'invoice.txt'
        downloaded_file_path = os.path.join(self.download_path, expected_filename)
        is_file_downloaded = False
        timeout = 30
        start_time = time()
        while not os.path.exists(downloaded_file_path) or time() - start_time < timeout:
            if os.path.exists(downloaded_file_path):
                is_file_downloaded = True
                break
            sleep(1)
        self.assertTrue(is_file_downloaded)
        self.payment_done.click_continue_button()
        self.payment_done.navbar.click_navbar_item('Delete Account')
        self.assertTrue(self.account_deleted.get_account_deleted_header().is_displayed())
        self.account_deleted.click_continue_button()

    def test_verify_scroll_up_using_arrow_button_and_scroll_down(self):
        self.assertTrue(self.home.get_slider_element().is_displayed())
        self.wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.assertEqual(self.home.subscription.get_footer_element_header().text, 'SUBSCRIPTION')
        self.home.scroll_up_button.click_scroll_up_button()
        sleep(1)
        page_scroll_position = self.wd.execute_script('return window.pageYOffset;')
        self.assertEqual(page_scroll_position, 0)
        slider_item_second_header = self.home.get_active_slider_item_second_header()
        slider_item_second_header_text = slider_item_second_header.text
        self.assertEqual(slider_item_second_header_text, 'Full-Fledged practice website for Automation Engineers')

    def test_verify_scroll_up_without_arrow_button_and_scroll_down(self):
        self.assertTrue(self.home.get_slider_element().is_displayed())
        self.wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.assertEqual(self.home.subscription.get_footer_element_header().text, 'SUBSCRIPTION')
        self.wd.execute_script("window.scrollTo(0,0);")
        sleep(1)
        page_scroll_position = self.wd.execute_script('return window.pageYOffset;')
        self.assertEqual(page_scroll_position, 0)
        slider_item_second_header = self.home.get_active_slider_item_second_header()
        slider_item_second_header_text = slider_item_second_header.text
        self.assertEqual(slider_item_second_header_text, 'Full-Fledged practice website for Automation Engineers')

    def tearDown(self):
        # print("Entered 'tearDown()'")
        self.wd.quit()
        if check_existence_of_user_via_api(self.user2):
            delete_user_via_api(self.user2)

        if os.path.exists(f'{self.download_path}\\invoice.txt'):
            os.remove(f'{self.download_path}\\invoice.txt')
        # print("Exiting 'tearDown()'")
