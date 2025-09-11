from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BaseElement:
    def __init__(self, wd:WebDriver):
        self.wd = wd
        self.wait = WebDriverWait(self.wd, 10)

    def find_element(self, locator_type, element_locator:str, start_element:WebElement = None):
        if start_element:
            return start_element.find_element(locator_type, element_locator)
        return self.wait.until(EC.presence_of_element_located((locator_type, element_locator)))
