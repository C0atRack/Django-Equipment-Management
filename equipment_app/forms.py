from django.forms import ModelForm, Textarea, TextInput, DateInput, Select, URLInput
from .models import *

class EquipmentForm(ModelForm):
    class Meta:
        model = EquipmentModel
        fields = '__all__'
        exclude = ["CheckedOutTo","CheckOutDate","CheckOutLocation"]
        widgets = {
            "SerialNumber" : TextInput(attrs={"class" : "form-control"}),
            "ModelNumber" : TextInput(attrs={"class" : "form-control"}),
            "AssetTag" : TextInput(attrs={"class" : "form-control"}),
            "Category" : Select(attrs={"class" : "form-select"}),
            "Description" : Textarea(attrs={"class" : "form-control"}),
            "ManualLink" : URLInput(attrs={"class" : "form-control"}),
            # https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/date
            "CalDueDate" : DateInput(attrs={"class" : "form-control", "type": "date"}),
            "WaranteeExpires" : DateInput(attrs={"class" : "form-control", "type": "date"}),
            "AccessoryOf" : Select(attrs={"class" : "form-select"})
        }