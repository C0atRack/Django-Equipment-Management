from django.test import TransactionTestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage

from equipment_app.forms import EquipmentForm
from equipment_app.models import EquipmentModel
from equipment_manager.settings import STORAGES

from datetime import datetime
from io import BytesIO
import PIL
import hashlib

class EquipmentFormTest(TransactionTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        Img = PIL.Image.new("RGB", (100,100))
        ImgOut = BytesIO()
        Img.save(ImgOut, "PNG")
        cls.imgData = ImgOut.getvalue()
        cls.date =  datetime.now()
        

    serialized_rollback = True

    def test_form_verify_valid(self):
        data : dict = {
            'Name': "Test", 
            'SerialNumber' : "1234", 
            'ModelNumber' : "1234",
            'AssetTag' : '1234',
            'Category' : 'Test Equipment',
            'Description' : 'Description',
            'ManualLink' : 'http://example.com',
            'CheckInLocation' : 'Checkin location',
            'CalDueDate' : self.date,
            'WaranteeExpires' : self.date,
        }
        uploadfiles = {'Img' : SimpleUploadedFile("TestImg.png", self.imgData)}
        testform = EquipmentForm(data=data, files=uploadfiles)
        self.assertTrue(testform.is_valid())

    def test_form_verify_creation(self):
        data : dict = {
            'Name': "Test", 
            'SerialNumber' : "1234", 
            'ModelNumber' : "1234",
            'AssetTag' : '1234',
            'Category' : 'Test Equipment',
            'Description' : 'Description',
            'ManualLink' : 'http://example.com',
            'CheckInLocation' : 'Checkin location',
            'CalDueDate' : self.date,
            'WaranteeExpires' : self.date,
        }
        uploadfiles = {'Img' : SimpleUploadedFile("TestImg.png", self.imgData)}
        testform = EquipmentForm(data=data, files=uploadfiles)
        testEqu : EquipmentModel = testform.save()

        # Lookup and verify the equipment was written correctly
        self.assertEqual(testEqu.Name,  "Test",)
        self.assertEqual(testEqu.SerialNumber,  "5678",)
        self.assertEqual(testEqu.ModelNumber,  "9101112")
        self.assertEqual(testEqu.AssetTag,  '1314151')
        self.assertEqual(testEqu.Category,  'Test Equipment')
        self.assertEqual(testEqu.Description,  'Description')
        self.assertEqual(testEqu.ManualLink,  'http://example.com')
        self.assertEqual(testEqu.CheckInLocation,  'Checkin location')
        self.assertEqual(testEqu.CalDueDate.strftime("%Y-%m-%d"),  self.date.strftime("%Y-%m-%d"))
        self.assertEqual(testEqu.WaranteeExpires.strftime("%Y-%m-%d"),  self.date.strftime("%Y-%m-%d"))
        # Verify the image we saved is the same as the image data we sent
        writtenImg = default_storage.open(str(testEqu.Img.file))
        writtenMD5 = hashlib.file_digest(writtenImg, 'md5').hexdigest()

        uploadedMD5 = hashlib.md5()
        uploadedMD5.update(self.imgData)


        self.assertEqual(writtenMD5, uploadedMD5.hexdigest())
        


    def test_form_missing_img(self):
        data : dict = {
            'Name': "Test", 
            'SerialNumber' : "1234", 
            'ModelNumber' : "1234",
            'AssetTag' : '1234',
            'Category' : 'Test Equipment',
            'Description' : 'Description',
            'ManualLink' : 'http://example.com',
            'CheckInLocation' : 'Checkin location',
            'CalDueDate' : self.date,
            'WaranteeExpires' : self.date,
        }
        testform = EquipmentForm(data=data)
        self.assertFalse(testform.is_valid())

