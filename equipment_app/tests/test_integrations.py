from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from equipment_manager.settings import BASE_DIR
from django.contrib.auth.models import User, Permission
from django.urls import reverse
import re

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
        


class SignUpTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.selenium.maximize_window()
        # Matches when the url is http://localhost:<port>/user/profile/number
        cls.urlRegex = re.compile("http(s?)\:\/\/(([a-zA-Z\.])+((\.[a-zA-Z\.])+)?)((\:[0-9]+)?)\/user\/profile\/\d+")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.selenium.save_full_page_screenshot(f"Integration_User_Signup.png")
        cls.selenium.quit()
        super().tearDownClass()

    def test_equipment_create(self):
        targetUrl = reverse("index")
        self.selenium.get(f"{self.live_server_url}{targetUrl}")
        self.selenium.find_element(By.ID, "signupLink").click()
        self.selenium.find_element(By.ID, "id_first_name").send_keys("Hello")
        self.selenium.find_element(By.ID, "id_last_name").send_keys("World")
        self.selenium.find_element(By.ID, "id_email").send_keys("world@hello.net")
        password = "E@mp3leP@ssw0rd!"
        for id in range(1,3): 
            self.selenium.find_element(By.ID, f"id_password{id}").send_keys(password)
        self.selenium.find_element(By.ID, "register_submit").click()
        print(self.selenium.current_url)

        WebDriverWait(self.selenium, timeout=10).until(lambda check: self.urlRegex.match(self.selenium.current_url) )
        
        
        
        
        


