import selenium.common
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class BaseElement:
    def __init__(self, wd:WebDriver):
        self.wd = wd
        self.wait = WebDriverWait(self.wd, 10)


    def is_page_loaded(self):
        page_ready_state = self.wd.execute_script("return document.readyState;")
        return page_ready_state == 'complete'

    def is_page_displayed(self):
        if self.is_page_loaded():
            page_body_element = self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))
            return page_body_element.is_displayed()
        return False

    def find_element(self, locator_type, element_locator:str, start_element:WebElement = None):
        try:
            if start_element:
                return start_element.find_element(locator_type, element_locator)
            if self.is_page_displayed():
                return self.wait.until(EC.presence_of_element_located((locator_type, element_locator)))
        except selenium.common.TimeoutException as e:
            print(f'Timeout Exception: {e.msg}')
        except selenium.common.NoSuchElementException as e:
            print(f'Element could not be found exception: {e.msg}')
