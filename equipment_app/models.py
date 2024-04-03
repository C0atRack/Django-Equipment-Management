from django.db import models

class Employee(models.Model):
    pass


class EquipmentModel(models.Model):

    EQUIPMENT_CATEGORIES = (
        ('Accessory', "Assessory"),
        ('Test Equipment', 'Test Equipment'),
        ('Consumable', 'Consumable'),
    )

    SerialNumber = models.CharField(max_length=200, blank=False)
    ModelNumber = models.CharField(max_length=200, blank=False)
    AssetTag = models.CharField(max_length=200, blank=False)
    Category = models.CharField(max_length=100, choices=EQUIPMENT_CATEGORIES)
    Img = models.ImageField(upload_to="uploads/")
    Description = models.TextField(max_length=5000, blank=False)
    ManualLink = models.URLField(max_length=1000, blank=True)

    CalDueDate = models.DateField()
    WaranteeExpires = models.DateField()

    CheckedOutTo = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL)
    CheckOutDate = models.DateField(null = True, blank=True)
    CheckOutLocation = models.CharField(max_length=200, null = True, blank=True)

    AccessoryOf = models.ForeignKey('self', null=True, blank=True,on_delete=models.SET_NULL)
        


