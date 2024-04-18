import PIL.Image
from django.test import TransactionTestCase
from equipment_app.forms import EquipmentForm

from datetime import datetime

import PIL

class EquipmentFormTest(TransactionTestCase):

    serialized_rollback = True

    def test_form_verify_valid(self):
        date = datetime.today()
        data : dict = {
            'Name': "Test", 
            'SerialNumber' : "1234", 
            'ModelNumber' : "1234",
            'AssetTag' : '1234',
            'Category' : 'Test Equipment',
            'Description' : 'Description',
            'ManualLink' : 'http://example.com',
            'CheckInLocation' : 'Checkin location',
            'CalDueDate' : date,
            'WaranteeExpires' : date,
        }
        testform = EquipmentForm(data=data)
        print(testform.errors)
        self.assertTrue(testform.is_valid())
