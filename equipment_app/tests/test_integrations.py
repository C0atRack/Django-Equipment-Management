from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from equipment_manager.settings import BASE_DIR
from equipment_app.models import *

from decouple import config

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
        cls.width: int = config("BROWSER_WIDTH", default=0, cast=int)
        cls.height: int = config("BROWSER_HEIGHT", default=0, cast=int)
        cls.click_navbar = False
        if(cls.width and cls.height):
            cls.selenium.set_window_size(width=cls.width, height=cls.height)
            cls.click_navbar = True
        else:
            #fullscreen
            cls.selenium.maximize_window()
    
    def screenShot(self, testname: str):
        mobileText: str = f"_mobile_{self.width}x{self.height}" if self.click_navbar else ""
        self.selenium.save_full_page_screenshot(f"Integration_{testname}{mobileText}.png")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.selenium.quit()
        super().tearDownClass()

    def login(self, username: str, password: str):
        self.findAndScrollToElement(By.ID, "id_username").send_keys(username)
        self.findAndScrollToElement(By.ID, "id_password").send_keys(password)
        self.findAndScrollToElement(By.ID, "login_button").click()

    def openNavBarDropdown(self):
        self.selenium.find_element(By.XPATH, '//button[@class="navbar-toggler"]').click()

    def findAndScrollToElement(self, by: str, selector: str) -> WebElement:
        elem = self.selenium.find_element(by, selector)
        # Smooth scrolling messes up the click action IF it's found
        if(elem):
            self.selenium.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'end'})", elem)
        return elem
        


class EquipmentCreateTest(EqBaseTest):
    fixtures = [str(BASE_DIR / "testing_data" / "fixtures" / "equipment_create.json")]
    
    serialized_rollback = True

    def test_equipment_create(self):
        self.selenium.get(f"{self.live_server_url}/login")
        self.login("test@example.com", "niwL5nZeBTZa64M")

        BlankNumber = "1234"
        targetUrl = reverse("equipment-list")
        self.selenium.get(f"{self.live_server_url}{targetUrl}")
        self.findAndScrollToElement(By.ID, "add_equipment").click()
        self.findAndScrollToElement(By.ID, "id_Name").send_keys("Test Equipment")
        self.findAndScrollToElement(By.ID, "id_SerialNumber").send_keys(BlankNumber)
        self.findAndScrollToElement(By.ID, "id_ModelNumber").send_keys(BlankNumber)
        self.findAndScrollToElement(By.ID, "id_AssetTag").send_keys(BlankNumber)
        options = Select(self.selenium.find_element(By.ID, "id_Category"))
        options.select_by_visible_text("Test Equipment")

        self.findAndScrollToElement(By.CSS_SELECTOR, "input[type='file']").send_keys((BASE_DIR / "testing_data"/ "test_equipment.png").__str__())
        self.findAndScrollToElement(By.ID, "id_Description").send_keys("Test description")
        self.findAndScrollToElement(By.ID, "id_ManualLink").send_keys("https://example.site")
        self.findAndScrollToElement(By.ID, "id_CheckInLocation").send_keys("Test location")
        for name in ["CalDueDate", "WaranteeExpires"]:
            elem = self.findAndScrollToElement(By.NAME, name)
            elem.send_keys(datetime.today().strftime("%Y-%m-%d"))
        self.findAndScrollToElement(By.ID, "submit").click()
        self.findAndScrollToElement(By.ID, "edit_button")
        self.screenShot("Equipment_Create")
        
class EquipmentModifyTest(EqBaseTest):
    fixtures = [str(BASE_DIR / "testing_data" / "fixtures" / "modify.json")]
    
    serialized_rollback = True
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.urlRegex = re.compile("http(s?)\:\/\/(([a-zA-Z\.])+((\.[a-zA-Z\.])+)?)((\:[0-9]+)?)\/equipment\/\d+")
    

    def test_equipment_modify(self):
        self.assertEqual(EquipmentModel.objects.all().count(), 1)
        self.selenium.get(f"{self.live_server_url}/login")
        self.login("test@example.com", "niwL5nZeBTZa64M")

        BlankNumber = "1235"
        targetUrl = reverse("equipment-list")
        self.selenium.get(f"{self.live_server_url}{targetUrl}")
        self.findAndScrollToElement(By.XPATH, '//a[@aria-label="Edit Test\'s information"]').click()
        namefield = self.findAndScrollToElement(By.ID, "id_Name")
        namefield.clear()
        namefield.send_keys("Test Equipment Modify")

        self.findAndScrollToElement(By.CSS_SELECTOR, "input[type='file']").send_keys((BASE_DIR / "testing_data"/ "test_equipment_new.png").__str__())

        serialfield = self.findAndScrollToElement(By.ID, "id_SerialNumber")
        serialfield.clear()
        serialfield.send_keys(BlankNumber)

        modelNumField = self.findAndScrollToElement(By.ID, "id_ModelNumber")
        modelNumField.clear()
        modelNumField.send_keys(BlankNumber)

        assetTagField = self.findAndScrollToElement(By.ID, "id_AssetTag")
        assetTagField.clear()
        assetTagField.send_keys(BlankNumber)



        descField = self.findAndScrollToElement(By.ID, "id_Description")
        descField.clear()
        descField.send_keys("New test description")


        manualLink = self.findAndScrollToElement(By.ID, "id_ManualLink")\
        # I cannot use clear since the url field does not work with selenium
        manualLink.send_keys(Keys.CONTROL + "a")
        manualLink.send_keys(Keys.DELETE)
        manualLink.send_keys("https://new.example.site")

        self.findAndScrollToElement(By.ID, "id_CheckInLocation").send_keys("Test location NEW")
        for name in ["CalDueDate", "WaranteeExpires"]:
            elem = self.findAndScrollToElement(By.NAME, name)
            elem.send_keys(Keys.CONTROL + "a")
            elem.send_keys(Keys.DELETE)
            elem.send_keys(datetime.today().strftime("%Y-%m-%d"))
        self.findAndScrollToElement(By.ID, "submit").click()
        WebDriverWait(self.selenium, timeout=10).until(lambda check: self.urlRegex.match(self.selenium.current_url) )
        obj = EquipmentModel.objects.all().first()
        self.assertEqual(obj.SerialNumber, "1235")
        self.screenShot("Equipment_Modify")

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
        if(self.click_navbar):
            self.openNavBarDropdown()
        self.findAndScrollToElement(By.ID, "signupLink").click()
        self.findAndScrollToElement(By.ID, "id_first_name").send_keys("Hello")
        self.findAndScrollToElement(By.ID, "id_last_name").send_keys("World")
        email = "world@hello.net"
        self.findAndScrollToElement(By.ID, "id_email").send_keys(email)
        password = "E@mp3leP@ssw0rd!"
        for id in range(1,3): 
            self.findAndScrollToElement(By.ID, f"id_password{id}").send_keys(password)
        self.findAndScrollToElement(By.ID, "register_submit").click()
        #Wait for the url to match before proceeding
        WebDriverWait(self.selenium, timeout=10).until(lambda check: self.loginRegex.match(self.selenium.current_url) )

        #Try to log 
        self.login(email, password)

        WebDriverWait(self.selenium, timeout=10).until(lambda check: self.profileRegex.match(self.selenium.current_url) )
        self.screenShot("User_Signup")


    def test_bad_password(self):
        targetUrl = reverse("index")
        self.selenium.get(f"{self.live_server_url}{targetUrl}")
        if(self.click_navbar):
            self.openNavBarDropdown()
        self.findAndScrollToElement(By.ID, "signupLink").click()
        self.findAndScrollToElement(By.ID, "id_first_name").send_keys("Hello")
        self.findAndScrollToElement(By.ID, "id_last_name").send_keys("World")
        email = "world@hello.net"
        self.findAndScrollToElement(By.ID, "id_email").send_keys(email)
        password = "1234"
        for id in range(1,3): 
            self.findAndScrollToElement(By.ID, f"id_password{id}").send_keys(password)
        self.findAndScrollToElement(By.ID, "register_submit").click()

        self.assertIsNotNone(self.findAndScrollToElement(By.XPATH, '//ul[@class="errorlist"]'))
        self.screenShot("User_Signup_bad_pass")

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
        if(self.click_navbar):
            self.openNavBarDropdown()
        self.findAndScrollToElement(By.XPATH, "//a[@href='/equipment/list']").click()
        self.findAndScrollToElement(By.XPATH, '//a[@aria-label="View Test information"]').click()
        self.findAndScrollToElement(By.XPATH, '//a[@aria-label="Check out Test"]').click()
        self.login("test@example.com", "niwL5nZeBTZa64M")

        self.findAndScrollToElement(By.ID, "id_CheckOutLocation").send_keys("Test Checkout Location")
        self.findAndScrollToElement(By.ID, "submit").click()

        WebDriverWait(self.selenium, timeout=10).until(lambda check: self.urlRegex.match(self.selenium.current_url) )

        self.assertIsNotNone(self.findAndScrollToElement(By.XPATH, '//a[@aria-label="Check Test in"]'))
        self.assertFalse(EquipmentModel.objects.get(id=1).is_availible())
        self.screenShot("CheckOut")

        
class CheckInTest(EqBaseTest):
    fixtures = [str(BASE_DIR / "testing_data" / "fixtures" / "checkin.json")]

    serialized_rollback = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.urlRegex = re.compile("http(s?)\:\/\/(([a-zA-Z\.])+)((\:[0-9]+)?)\/equipment\/\d+")

    def test_checkin_from_list(self):
        self.selenium.get(f"{self.live_server_url}")
        loginLink = self.findAndScrollToElement(By.ID, "loginLink")
        if(self.click_navbar):
            self.openNavBarDropdown()
            WebDriverWait(driver=self.selenium, timeout=10).until(lambda x: loginLink.is_displayed())
        loginLink.click()
        self.login("test@example.com", "niwL5nZeBTZa64M")
        equList = self.findAndScrollToElement(By.XPATH, "//a[@href='/equipment/list']")
        if(self.click_navbar):
            self.openNavBarDropdown()
            WebDriverWait(driver=self.selenium, timeout=10).until(lambda x: equList.is_displayed())
        equList.click()
        self.findAndScrollToElement(By.XPATH, '//a[@aria-label="View Test information"]').click()
        self.findAndScrollToElement(By.XPATH, '//a[@aria-label="Check Test in"]').click()
        self.findAndScrollToElement(By.ID, "id_TurnedIn").click()
        self.findAndScrollToElement(By.ID, "submit").click()

        #Verify with the DB the equipment is not checked out
        self.assertIsNone(EquipmentModel.objects.get(id=1).CheckedOutTo)
        #Verify the view now says checkout
        self.assertIsNotNone(self.findAndScrollToElement(By.XPATH, '//a[@aria-label="Check out Test"]'))
        #Verify that the database says the object isn't checked out
        self.assertTrue(EquipmentModel.objects.get(id=1).is_availible())

        self.screenShot("CheckIn")

