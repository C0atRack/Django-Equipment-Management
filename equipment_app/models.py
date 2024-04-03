from django.db import models

class Employee(models.Model):
    pass


class EquipmentModel(models.Model):

    EQUIPMENT_CATEGORIES = {
        'Accessory' : "Assessory",
        'Test Equipment' : 'Test Equipment',
        'Consumable' : 'Consumable',
    }

    SerialNumber = models.CharField(max_length=200, null=False)
    ModelNumber = models.CharField(max_length=200, null=False)
    AssetTag = models.CharField(max_length=200, null=False)
    Category = models.CharField(choices=EQUIPMENT_CATEGORIES)
    Img = models.ImageField(upload_to="uploads/")
    Description = models.TextField(max_length=5000, null=False)
    ManualLink = models.URLField(max_length=1000)

    CalDueDate = models.DateField()
    WaranteeExpires = models.DateField()

    CheckedOutTo = models.ForeignKey(Employee, null=True, on_delete=models.DO_NOTHING)
    CheckOutDate = models.DateField()
    CheckOutLocation = models.CharField(max_length=200)

    AccessoryOf = models.ForeignKey('self', on_delete=models.SET_NULL)
        


