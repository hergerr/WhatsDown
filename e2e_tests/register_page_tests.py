import unittest
from selenium import webdriver
from time import sleep


class RegistrationPage(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_user_registration(self):
        driver = self.driver
        driver.get("https://whatsdown.tscode.net/signup-user")
        elem = driver.find_element_by_name("username")
        elem.send_keys("new_user")
        elem = driver.find_element_by_name("password")
        elem.send_keys("new_password")
        elem = driver.find_element_by_name("confirm")
        elem.send_keys("new_password")
        elem = driver.find_element_by_name("name")
        elem.send_keys("New User")
        elem = driver.find_element_by_name("county")
        elem.send_keys("Wrocław")
        elem = driver.find_element_by_name("locality")
        elem.send_keys("Wrocław")
        elem = driver.find_element_by_name("phone")
        elem.send_keys("132 123 123")
        elem = driver.find_element_by_name("price")
        elem.send_keys("400")
        elem = driver.find_element_by_class_name("button")
        elem.click()
        assert "New funeral agency created" in driver.page_source

    def test_user_removal(self):
        driver = self.driver
        driver.get("https://whatsdown.tscode.net/login")
        elem = driver.find_element_by_name("username")
        elem.send_keys("admin")
        elem = driver.find_element_by_name("password")
        elem.send_keys("admin")
        elem = driver.find_element_by_class_name("button")
        elem.click()
        funeral_home_menu = driver.find_element_by_xpath("//*[contains(text(),'Funeral Home')]")
        funeral_home_menu.click()
        delete_fun_home_button = driver.find_element_by_xpath("//tbody//tr[last()]//span[@class='fa fa-trash glyphicon icon-trash']")
        delete_fun_home_button.click()
        alert = driver.switch_to.alert
        alert.accept()
        sleep(4)
        assert "new_user" not in driver.page_source

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
