import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class BuriedAndFuneralsPage(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.wait = WebDriverWait(self.driver, 4)
        self.driver.get("https://whatsdown.tscode.net/login")
        elem = self.driver.find_element_by_name("username")
        elem.send_keys("funex")
        elem = self.driver.find_element_by_name("password")
        elem.send_keys("funex")
        elem = self.driver.find_element_by_class_name("button")
        elem.click()
        sleep(2)

    def test01_login_should_redirect_to_dashboard(self):
        assert "Welcome FUNerals" in self.driver.page_source

    def test02_should_display_two_buried_and_header_row(self):
        elem = self.driver.find_element_by_xpath("//div[@class='navbar-list']//a[contains(text(), 'Buried')]")
        elem.click()
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "table-flex")))
        elem = self.driver.find_elements_by_css_selector("tr")
        assert len(elem) == 3

    def test03_should_display_three_funerals_and_header_row(self):
        elem = self.driver.find_element_by_xpath("//div[@class='navbar-list']//a[contains(text(), 'Funerals')]")
        elem.click()
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "table-flex")))
        elem = self.driver.find_elements_by_css_selector("tr")
        assert len(elem) == 4

    def test04_should_logout_and_block_access_to_user_dashboard(self):
        elem = self.driver.find_element_by_xpath("//div[@class='navbar-list']//a[contains(text(), 'Logout')]")
        elem.click()
        assert "Dashboard" and "Funerals" and "Buried" not in self.driver.page_source

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
