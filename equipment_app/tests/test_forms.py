import PIL.Image
from io import BytesIO
from django.test import TransactionTestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from equipment_app.forms import EquipmentForm

from datetime import datetime

import PIL

class EquipmentFormTest(TransactionTestCase):

    serialized_rollback = True

    def test_form_verify_valid(self):
        Img = PIL.Image.new("RGB", (100,100))
        ImgOut = BytesIO()
        Img.save(ImgOut, "PNG")
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
        uploadfiles = {'Img' : SimpleUploadedFile("TestImg.png", ImgOut.getvalue())}
        testform = EquipmentForm(data=data, files=uploadfiles)
        print(testform.errors)
        self.assertTrue(testform.is_valid())
