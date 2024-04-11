from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.select import Select

from equipment_manager.settings import BASE_DIR
from django.contrib.auth.models import User, Permission
from django.urls import reverse

from datetime import datetime

class EquipmentCreateTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.selenium.maximize_window()
        cls.user = User.objects.create_user(username="test", password="test")
        cls.user.user_permissions.add(Permission.objects.get(codename="can_edit"))
        cls.selenium.get(f"{cls.live_server_url}/login")
        cls.selenium.find_element(By.ID, "id_username").send_keys("test")
        cls.selenium.find_element(By.ID, "id_password").send_keys("test")
        cls.selenium.find_element(By.ID, "login_button").click()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.selenium.save_full_page_screenshot(f"Integration_Equipment_Create.png")
        cls.selenium.quit()
        super().tearDownClass()

    def test_equipment_create(self):
        BlankNumber = "1234"
        targetUrl = reverse("equipment-list")
        self.selenium.get(f"{self.live_server_url}{targetUrl}")
        self.selenium.find_element(By.ID, "add_equipment").click()
        self.selenium.find_element(By.ID, "id_Name").send_keys("Test Equipment")
        self.selenium.find_element(By.ID, "id_SerialNumber").send_keys(BlankNumber)
        self.selenium.find_element(By.ID, "id_ModelNumber").send_keys(BlankNumber)
        self.selenium.find_element(By.ID, "id_AssetTag").send_keys(BlankNumber)
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
        self.selenium.find_element(By.ID, "edit_button")
        


