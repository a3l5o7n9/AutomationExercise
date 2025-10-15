import selenium.common.exceptions
# from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class BaseElement:
    def __init__(self, wd:WebDriver):
        self.wd = wd
        self.wait = WebDriverWait(self.wd, 10)

    def is_page_loaded(self):
        try:
            page_ready_state = self.wd.execute_script("return document.readyState;")
            return page_ready_state == 'complete'
        except selenium.common.exceptions.TimeoutException as e:
            raise

    def is_page_displayed(self):
        try:
            if self.is_page_loaded():
                page_body_element = self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))
                return page_body_element.is_displayed()
        except selenium.common.exceptions.TimeoutException as e:
            raise

    def find_element(self, locator_type, element_locator:str, start_element:WebElement = None):
        if start_element:
            # print("Entered if start_element")
            return start_element.find_element(locator_type, element_locator)
        if self.is_page_displayed():
            # print("Entered if 'is_page_displayed()'")
            try:
                target_element = self.wait.until(EC.presence_of_element_located((locator_type, element_locator)))
                return target_element
                # return self.wd.find_element(locator_type, element_locator)
            except selenium.common.TimeoutException as e:
                print('Target element does not appear in DOM!')
                print(element_locator)
                raise
