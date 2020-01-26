import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class RegistrationPage(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.wait = WebDriverWait(self.driver, 4)



    def test01_empty_field_should_not_filter(self):
        self.driver.get("https://whatsdown.tscode.net/")
        elem = self.driver.find_element_by_name('phrase')
        elem.send_keys(Keys.RETURN)
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "table-flex")))
        assert "Jarosławski" in self.driver.page_source

    def test02_pea_in_search_should_return_two_records_in_buried(self):
        self.driver.get("https://whatsdown.tscode.net/")
        elem = self.driver.find_element_by_name('phrase')
        elem.send_keys("PEA")
        elem.send_keys(Keys.RETURN)
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "table-flex")))
        assert "Jan" and "Filip" in self.driver.page_source

    def test03_pea_in_filter_should_return_one_record(self):
        self.driver.get("https://whatsdown.tscode.net/")
        elem = self.driver.find_element_by_name('phrase')
        elem.send_keys("PEA")
        elem.send_keys(Keys.RETURN)
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "filter-text")))
        elem = self.driver.find_element_by_class_name("filter-text")
        elem.send_keys("2.0")
        elem.send_keys(Keys.RETURN)
        assert "Filip" in self.driver.page_source

    def test04_empty_filter_field_should_not_change_search_results(self):
        self.driver.get("https://whatsdown.tscode.net/")
        elem = self.driver.find_element_by_name('phrase')
        elem.send_keys(Keys.RETURN)
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "filter-text")))
        elem = self.driver.find_element_by_class_name("filter-text")
        elem.send_keys(Keys.RETURN)
        assert "Jarosławski" in self.driver.page_source

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
