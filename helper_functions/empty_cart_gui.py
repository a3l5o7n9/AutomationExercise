# from selenium.webdriver.firefox.webdriver import WebDriver
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
import selenium.common.exceptions
from object_classes.user import User
from page_classes.cart import Cart
from page_classes.home import Home
from page_classes.login import Login


def empty_cart(base_url, user:User = None):
    # print("Entered 'empty_cart()'")
    options = Options()
    options.add_argument("--headless")
    ecwd = WebDriver(options)
    ecwd.set_page_load_timeout(30)
    ec_home = Home(ecwd, base_url)
    ec_login = Login(ecwd, base_url)
    ec_cart = Cart(ecwd, base_url)
    try:
        ecwd.get(base_url)
        if user:
            ecwd.get(f'{base_url}login')
            ec_login.set_login_email_field(user.email)
            ec_login.set_login_password_field(user.password)
            ec_login.click_login_submit_button()
        if ec_home.get_slider_element():
            ec_home.navbar.click_navbar_item('Cart')
            is_cart_empty = ec_cart.get_empty_cart_element().is_displayed()
            cart_products_list = []
            while not is_cart_empty:
                cart_products_list = ec_cart.cart_contents.get_products_in_cart_elements_list()
                if len(cart_products_list) == 0:
                    break
                ec_cart.click_specific_cart_product_delete_by_index(0)
                ecwd.refresh()
                is_cart_empty = ec_cart.get_empty_cart_element().is_displayed()
                if not is_cart_empty:
                    cart_products_list = ec_cart.cart_contents.get_products_in_cart_elements_list()
                    if len(cart_products_list) == 0:
                        is_cart_empty = True
    except selenium.common.exceptions.TimeoutException as e:
        print('Site failed to load properly')
        raise
    finally:
        ecwd.quit()
        # print("Exiting 'empty_cart()'")
