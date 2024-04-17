from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys

from equipment_manager.settings import BASE_DIR
from equipment_app.models import *
from django.urls import reverse
from time import sleep

import re

from datetime import datetime

class EqBaseTest(StaticLiveServerTestCase):

    #This has to be here AND in each inherited class. DO NOT REMOVE
    serialized_rollback = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.selenium.delete_all_cookies()
    
    @classmethod
    def tearDownClass(cls) -> None:
        cls.selenium.quit()
        super().tearDownClass()

    def login(self, username: str, password: str):
        self.selenium.find_element(By.ID, "id_username").send_keys(username)
        self.selenium.find_element(By.ID, "id_password").send_keys(password)
        self.selenium.find_element(By.ID, "login_button").click()

class EquipmentCreateTest(EqBaseTest):
    fixtures = [str(BASE_DIR / "testing_data" / "fixtures" / "equipment_create.json")]
    
    serialized_rollback = True

    def test_equipment_create(self):
        self.selenium.get(f"{self.live_server_url}/login")
        self.login("test@example.com", "niwL5nZeBTZa64M")

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
        self.selenium.save_full_page_screenshot("Integration_Equipment_Create.png")
        
class EquipmentModifyTest(EqBaseTest):
    fixtures = [str(BASE_DIR / "testing_data" / "fixtures" / "modify.json")]
    
    #serialized_rollback = True

    def test_equipment_create(self):
        self.assertEqual(EquipmentModel.objects.all().count(), 1)
        self.selenium.get(f"{self.live_server_url}/login")
        self.login("test@example.com", "niwL5nZeBTZa64M")

        BlankNumber = "1235"
        targetUrl = reverse("equipment-list")
        self.selenium.get(f"{self.live_server_url}{targetUrl}")
        self.selenium.find_element(By.XPATH, '//a[@aria-label="Edit Test\'s information"]').click()
        namefield = self.selenium.find_element(By.ID, "id_Name")
        namefield.clear()
        namefield.send_keys("Test Equipment Modify")

        fileElem = self.selenium.find_element(By.CSS_SELECTOR, "input[type='file']")
        fileElem.clear()
        #fileElem.send_keys((BASE_DIR / "testing_data"/ "test_equipment_new.png").__str__())
        print(fileElem)

        serialfield = self.selenium.find_element(By.ID, "id_SerialNumber")
        serialfield.clear()
        serialfield.send_keys(BlankNumber)

        modelNumField = self.selenium.find_element(By.ID, "id_ModelNumber")
        modelNumField.clear()
        modelNumField.send_keys(BlankNumber)

        assetTagField = self.selenium.find_element(By.ID, "id_AssetTag")
        assetTagField.clear()
        assetTagField.send_keys(BlankNumber)


        self.selenium.find_element(By.CSS_SELECTOR, "input[type='file']").send_keys((BASE_DIR / "testing_data"/ "test_equipment_new.png").__str__())

        descField = self.selenium.find_element(By.ID, "id_Description")
        descField.clear()
        descField.send_keys("New test description")


        manualLink = self.selenium.find_element(By.ID, "id_ManualLink")\
        # I cannot use clear since the url field does not work with selenium
        manualLink.send_keys(Keys.CONTROL + "a")
        manualLink.send_keys(Keys.DELETE)
        manualLink.send_keys("https://new.example.site")

        self.selenium.find_element(By.ID, "id_CheckInLocation").send_keys("Test location NEW")
        for name in ["CalDueDate", "WaranteeExpires"]:
            elem = self.selenium.find_element(By.NAME, name)
            elem.clear()
            elem.send_keys(datetime.today().strftime("%Y-%m-%d"))
        self.selenium.find_element(By.ID, "submit").click()
        obj = EquipmentModel.objects.all().first()
        print(obj.Img)
        self.assertEqual(obj.SerialNumber, "1235")
        self.selenium.save_full_page_screenshot("Integration_Equipment_Modify.png")

class SignUpTest(EqBaseTest):

    serialized_rollback = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.loginRegex = re.compile("http(s?)\:\/\/(([a-zA-Z\.])+((\.[a-zA-Z\.])+)?)((\:[0-9]+)?)\/login")
        # Matches when the url is http://localhost:<port>/user/profile/<number>
        cls.profileRegex = re.compile("http(s?)\:\/\/(([a-zA-Z0-9\.])+((\.[a-zA-Z0-9\.])+)?)((\:[0-9]+)?)\/user\/profile\/\d+")

    def test_signup(self):
        targetUrl = reverse("index")
        self.selenium.get(f"{self.live_server_url}{targetUrl}")
        self.selenium.find_element(By.ID, "signupLink").click()
        self.selenium.find_element(By.ID, "id_first_name").send_keys("Hello")
        self.selenium.find_element(By.ID, "id_last_name").send_keys("World")
        email = "world@hello.net"
        self.selenium.find_element(By.ID, "id_email").send_keys(email)
        password = "E@mp3leP@ssw0rd!"
        for id in range(1,3): 
            self.selenium.find_element(By.ID, f"id_password{id}").send_keys(password)
        self.selenium.find_element(By.ID, "register_submit").click()
        #Wait for the url to match before proceeding
        WebDriverWait(self.selenium, timeout=10).until(lambda check: self.loginRegex.match(self.selenium.current_url) )

        #Try to log 
        self.login(email, password)

        WebDriverWait(self.selenium, timeout=10).until(lambda check: self.profileRegex.match(self.selenium.current_url) )
        self.selenium.save_full_page_screenshot("Integration_User_Signup.png")


    def test_bad_password(self):
        targetUrl = reverse("index")
        self.selenium.get(f"{self.live_server_url}{targetUrl}")
        self.selenium.find_element(By.ID, "signupLink").click()
        self.selenium.find_element(By.ID, "id_first_name").send_keys("Hello")
        self.selenium.find_element(By.ID, "id_last_name").send_keys("World")
        email = "world@hello.net"
        self.selenium.find_element(By.ID, "id_email").send_keys(email)
        password = "1234"
        for id in range(1,3): 
            self.selenium.find_element(By.ID, f"id_password{id}").send_keys(password)
        self.selenium.find_element(By.ID, "register_submit").click()

        self.assertIsNotNone(self.selenium.find_element(By.XPATH, '//ul[@class="errorlist"]'))
        self.selenium.save_full_page_screenshot("Integration_User_Signup_bad_pass.png")

class CheckOutTest(EqBaseTest):
    fixtures = [str(BASE_DIR / "testing_data" / "fixtures" / "checkout.json")]
        
    serialized_rollback = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.urlRegex = re.compile("http(s?)\:\/\/(([a-zA-Z\.])+((\.[a-zA-Z\.])+)?)((\:[0-9]+)?)\/equipment\/\d+")


    def test_checkout(self):
        targetUrl = reverse("index")
        self.selenium.get(f"{self.live_server_url}{targetUrl}")
        self.selenium.find_element(By.XPATH, "//a[@href='/equipment/list']").click()
        self.selenium.find_element(By.XPATH, '//a[@aria-label="View Test information"]').click()
        self.selenium.find_element(By.XPATH, '//a[@aria-label="Check out Test"]').click()
        self.login("test@example.com", "niwL5nZeBTZa64M")

        self.selenium.find_element(By.ID, "id_CheckOutLocation").send_keys("Test Checkout Location")
        self.selenium.find_element(By.ID, "submit").click()

        WebDriverWait(self.selenium, timeout=10).until(lambda check: self.urlRegex.match(self.selenium.current_url) )

        self.assertIsNotNone(self.selenium.find_element(By.XPATH, '//a[@aria-label="Check Test in"]'))
        self.selenium.save_full_page_screenshot("Integration_CheckOut.png")

        
class CheckInTest(EqBaseTest):
    fixtures = [str(BASE_DIR / "testing_data" / "fixtures" / "checkin.json")]

    serialized_rollback = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.urlRegex = re.compile("http(s?)\:\/\/(([a-zA-Z\.])+)((\:[0-9]+)?)\/equipment\/\d+")

    def test_checkin_from_list(self):
        self.selenium.get(f"{self.live_server_url}")
        self.selenium.find_element(By.ID, "loginLink").click()
        self.login("test@example.com", "niwL5nZeBTZa64M")
        self.selenium.find_element(By.XPATH, "//a[@href='/equipment/list']").click()
        self.selenium.find_element(By.XPATH, '//a[@aria-label="View Test information"]').click()
        self.selenium.find_element(By.XPATH, '//a[@aria-label="Check Test in"]').click()
        self.selenium.find_element(By.ID, "id_TurnedIn").click()
        self.selenium.find_element(By.ID, "submit").click()

        #Verify with the DB the equipment is not checked out
        self.assertIsNone(EquipmentModel.objects.get(id=1).CheckedOutTo)
        #Verify the view now says checkout
        self.assertIsNotNone(self.selenium.find_element(By.XPATH, '//a[@aria-label="Check out Test"]'))

        self.selenium.save_full_page_screenshot("Integration_CheckIn.png")
