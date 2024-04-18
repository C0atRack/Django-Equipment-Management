from django.contrib.auth.models import User
from django.test import TestCase

from equipment_app.models import EquipmentModel, Employee

from datetime import datetime

class TestEquipmentUrls(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.equipment = EquipmentModel.objects.create(Name="Test" , SerialNumber=1234 , ModelNumber=1234 , AssetTag=1234 , Category="Test Equipment" , Img="uploads/test_equipment.png" , Description="Test Equipment", ManualLink="http://example.com" , CheckInLocation="Test Check in location" , CalDueDate=datetime.today(), WaranteeExpires=datetime.today() , CheckedOutTo=None , CheckOutDate=None, CheckOutLocation=None , AccessoryOf=None        )
        return super().setUpClass()
    
    def test_CRUD_urls(self):
        self.assertEqual(self.equipment.get_absolute_url(), f"/equipment/{self.equipment.id}")
        self.assertEqual(self.equipment.get_edit_absolute_url(), f"/equipment/edit/{self.equipment.id}")
        self.assertEqual(self.equipment.get_delete_absolute_url(), f"/equipment/delete/{self.equipment.id}")
    
    def test_availibility_check(self):
        emp = Employee()
        self.equipment.CheckedOutTo = emp
        self.assertFalse(self.equipment.is_availible())
        self.equipment.CheckedOutTo = None
        self.assertTrue(self.equipment.is_availible())
    
    def test_checkX_urls(self):
        self.assertEqual(self.equipment.get_checkout_url(), f"/equipment/checkout/{self.equipment.id}")
        self.assertEqual(self.equipment.get_checkin_url(), f"/equipment/checkin/{self.equipment.id}")

class TestEmployeeUrls(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user:User = User.objects.create(first_name="Test", last_name="Name", email="testname@example.com", username="testname@example.com")
        cls.employee = Employee.objects.create(AffUser = cls.user)
        return super().setUpClass()
    
    def test_urls(self):
        self.assertEqual(self.employee.get_absolute_url(), f"/user/profile/{self.employee.id}")
        self.assertEqual(self.employee.get_perm_url(), f"/user/profile/{self.employee.id}/perm")
    
    def test_str(self):
        self.assertEqual(str(self.employee), "Test Name : testname@example.com")