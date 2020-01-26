import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep


class RegistrationAndLoginPage(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test01_user_registration_should_be_succesful(self):
        self.driver.get("https://whatsdown.tscode.net/signup-user")
        elem = self.driver.find_element_by_name("username")
        elem.send_keys("new_user")
        elem = self.driver.find_element_by_name("password")
        elem.send_keys("new_password")
        elem = self.driver.find_element_by_name("confirm")
        elem.send_keys("new_password")
        elem = self.driver.find_element_by_name("name")
        elem.send_keys("New User")
        elem = self.driver.find_element_by_name("county")
        elem.send_keys("Wrocław")
        elem = self.driver.find_element_by_name("locality")
        elem.send_keys("Wrocław")
        elem = self.driver.find_element_by_name("phone")
        elem.send_keys("132 123 123")
        elem = self.driver.find_element_by_name("price")
        elem.send_keys("400")
        elem = self.driver.find_element_by_class_name("button")
        elem.click()
        sleep(2)
        assert "New funeral agency created" in self.driver.page_source

    def test02_registration_should_fail_because_of_existing_same_user(self):
        self.driver.get("https://whatsdown.tscode.net/signup-user")
        elem = self.driver.find_element_by_name("username")
        elem.send_keys("new_user")
        elem = self.driver.find_element_by_name("password")
        elem.send_keys("new_password")
        elem = self.driver.find_element_by_name("confirm")
        elem.send_keys("new_password")
        elem = self.driver.find_element_by_name("name")
        elem.send_keys("New User")
        elem = self.driver.find_element_by_name("county")
        elem.send_keys("Wrocław")
        elem = self.driver.find_element_by_name("locality")
        elem.send_keys("Wrocław")
        elem = self.driver.find_element_by_name("phone")
        elem.send_keys("132 123 123")
        elem = self.driver.find_element_by_name("price")
        elem.send_keys("400")
        elem = self.driver.find_element_by_class_name("button")
        elem.click()
        sleep(2)
        assert "This user already exists" in self.driver.page_source

    def test03_login_as_new_user_should_fail_because_of_wrong_password(self):
        self.driver.get("https://whatsdown.tscode.net/login")
        elem = self.driver.find_element_by_name("username")
        elem.send_keys("new_user")
        elem = self.driver.find_element_by_name("password")
        elem.send_keys("wrong_new_password")
        elem = self.driver.find_element_by_class_name("button")
        elem.click()
        sleep(2)
        assert "Wrong password" in self.driver.page_source

    def test05_login_as_new_user_should_fail_because_of_wrong_username(self):
        self.driver.get("https://whatsdown.tscode.net/login")
        elem = self.driver.find_element_by_name("username")
        elem.send_keys("wrong_new_user")
        elem = self.driver.find_element_by_name("password")
        elem.send_keys("wrong_new_password")
        elem = self.driver.find_element_by_class_name("button")
        elem.click()
        sleep(2)
        assert "No such username" in self.driver.page_source

    def test06_login_as_new_user_should_be_succesful(self):
        self.driver.get("https://whatsdown.tscode.net/login")
        # elem = self.driver.find_element_by_xpath("//div[@class='navbar-list']//a[contains(text(),'Login')]")
        # elem.click()
        elem = self.driver.find_element_by_name("username")
        elem.send_keys("new_user")
        elem = self.driver.find_element_by_name("password")
        elem.send_keys("new_password")
        elem = self.driver.find_element_by_class_name("button")
        elem.click()
        sleep(2)
        assert "Welcome New User" in self.driver.page_source

    def test07_user_removal(self):
        self.driver.get("https://whatsdown.tscode.net/login")
        elem = self.driver.find_element_by_name("username")
        elem.send_keys("admin")
        elem = self.driver.find_element_by_name("password")
        elem.send_keys("admin")
        elem = self.driver.find_element_by_class_name("button")
        elem.click()
        funeral_home_menu = self.driver.find_element_by_xpath("//*[contains(text(),'Funeral Home')]")
        funeral_home_menu.click()
        delete_fun_home_button = self.driver.find_element_by_xpath(
            "//tbody//tr[last()]//span[@class='fa fa-trash glyphicon icon-trash']")
        delete_fun_home_button.click()
        alert = self.driver.switch_to.alert
        alert.accept()
        sleep(2)
        assert "new_user" not in self.driver.page_source

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
