from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Employee(models.Model):
    AffUser = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="User")
    
    def __str__(self) -> str:
        return f"{self.AffUser.first_name} {self.AffUser.last_name} : {self.AffUser.email}"
    
    def get_absolute_url(self):
        return reverse("profile", kwargs={"pk": self.pk})
    
    def get_perm_url(self):
        return reverse("update-perms", kwargs={"pk": self.pk})
    

class EquipmentModel(models.Model):

    EQUIPMENT_CATEGORIES = (
        ('Accessory', "Assessory"),
        ('Test Equipment', 'Test Equipment'),
        ('Consumable', 'Consumable'),
    )

    Name = models.CharField("Equipment Name", max_length=200, blank=False)
    SerialNumber = models.CharField("Serial Number", max_length=200, blank=False)
    ModelNumber = models.CharField("Model Number", max_length=200, blank=False)
    AssetTag = models.CharField("Asset Tag", max_length=200, blank=False)
    Category = models.CharField("Equipment Category", max_length=100, choices=EQUIPMENT_CATEGORIES)
    Img = models.ImageField("Photo", upload_to="uploads/")
    Description = models.TextField("Description", max_length=5000, blank=False)
    ManualLink = models.URLField("Link to Manual", max_length=1000, blank=True)
    CheckInLocation = models.CharField("Check In Location", max_length=200, blank=False)

    CalDueDate = models.DateField("Date for Calibration",)
    WaranteeExpires = models.DateField("Date Warentee Expires")

    CheckedOutTo = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL)
    CheckOutDate = models.DateField(null = True, blank=True)
    CheckOutLocation = models.CharField("Checkout Location", max_length=200, null = True, blank=True)

    AccessoryOf = models.ForeignKey('self', null=True, blank=True,on_delete=models.SET_NULL, verbose_name="Accessory Of")

    def __str__(self) -> str:
        return self.Name
        
    def get_absolute_url(self):
        return reverse('equipment-detail', args=[str(self.id)])
    
    def get_edit_absolute_url(self):
        return reverse('equipment-update', args=[str(self.id)])
    
    def get_delete_absolute_url(self):
        return reverse('equipment-delete', args=[str(self.id)])
    
    def get_checkout_url(self):
        return reverse('equipment-checkout', args=[str(self.id)])

    def is_availible(self):
        return self.CheckedOutTo == None
    
    class Meta:
        ordering = ['-AssetTag']
        permissions = (("can_edit", "Is the Employee allowed to edit details about the equipment"),)


