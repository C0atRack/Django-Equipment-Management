from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.select import Select

from equipment_manager.settings import BASE_DIR

from datetime import datetime

class EquipmentCreateTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.selenium.quit()
        super().tearDownClass()

    def test_equipment_create(self):
        self.selenium.get(f"{self.live_server_url}/equipment_list")
        self.selenium.find_element(By.ID, "add_equipment").click()
        self.selenium.find_element(By.ID, "id_Name").send_keys("Test Equipment")
        self.selenium.find_element(By.ID, "id_SerialNumber").send_keys("1234")
        self.selenium.find_element(By.ID, "id_ModelNumber").send_keys("1234")
        self.selenium.find_element(By.ID, "id_AssetTag").send_keys("1234")
        options = Select(self.selenium.find_element(By.ID, "id_Category"))
        options.select_by_visible_text("Test Equipment")

        self.selenium.find_element(By.CSS_SELECTOR, "input[type='file']").send_keys((BASE_DIR / "testing_data"/ "test_equipment.png").__str__())
        self.selenium.find_element(By.ID, "id_Description").send_keys("Test description")
        self.selenium.find_element(By.ID, "id_ManualLink").send_keys("https://example.site")
        self.selenium.find_element(By.ID, "id_CheckInLocation").send_keys("Test location")
        for name in ["CalDueDate", "WaranteeExpires"]:
            elem = self.selenium.find_element(By.NAME, name)
            elem.send_keys(datetime.today().strftime("%Y-%m-%d"))
        self.selenium.find_element(By.ID, "submit").click()
        


