import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep


class BuriedAndFuneralsPage(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.wait = WebDriverWait(self.driver, 4)

    def test01_login_should_redirect_to_dashboard(self):
        self.driver.get("https://whatsdown.tscode.net/login")
        elem = self.driver.find_element_by_name("username")
        elem.send_keys("funex")
        elem = self.driver.find_element_by_name("password")
        elem.send_keys("funex")
        elem = self.driver.find_element_by_class_name("button")
        elem.click()
        sleep(2)
        assert "Welcome FUNerals" in self.driver.page_source

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
