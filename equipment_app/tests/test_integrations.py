from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.select import Select

from selenium.webdriver.remote.webelement import WebElement

from PIL import Image

class BaselineTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.selenium.quit()
        super().tearDownClass()

    def test_homepage(self):
        self.selenium.get(self.live_server_url)

    def test_login(self):
        self.selenium.get(f"{self.live_server_url}/equipment_list")
        self.selenium.find_element(By.ID, "add_equipment").click()
        self.selenium.find_element(By.ID, "id_Name").send_keys("Test Equipment")
        self.selenium.find_element(By.ID, "id_SerialNumber").send_keys("1234")
        self.selenium.find_element(By.ID, "id_ModelNumber").send_keys("1234")
        self.selenium.find_element(By.ID, "id_AssetTag").send_keys("1234")
        options = Select(self.selenium.find_element(By.ID, "id_Category"))
        options.select_by_visible_text("Test Equipment")
        (self.selenium.find_elements(By.ID, "id_Img"): WebElement).send_keys("./testing_data/test_equipment.png")
        #print(fileinput)
        


