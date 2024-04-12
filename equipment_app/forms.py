from django.forms import ModelForm, Textarea, TextInput, DateInput, Select, URLInput, BooleanField, CheckboxInput
from django.contrib.auth.forms import UserCreationForm
from .models import *

class EquipmentForm(ModelForm):
    class Meta:
        model = EquipmentModel
        fields = '__all__'
        exclude = ["CheckedOutTo","CheckOutDate","CheckOutLocation"]
        widgets = {
            "Name" : TextInput(attrs={"class" : "form-control"}),
            "SerialNumber" : TextInput(attrs={"class" : "form-control"}),
            "ModelNumber" : TextInput(attrs={"class" : "form-control"}),
            "AssetTag" : TextInput(attrs={"class" : "form-control"}),
            "Category" : Select(attrs={"class" : "form-select"}),
            "Description" : Textarea(attrs={"class" : "form-control"}),
            "ManualLink" : URLInput(attrs={"class" : "form-control"}),
            "CheckInLocation" : TextInput(attrs={"class" : "form-control"}),
            # https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/date
            "CalDueDate" : DateInput(attrs={"class" : "form-control", "type": "date"}),
            "WaranteeExpires" : DateInput(attrs={"class" : "form-control", "type": "date"}),
            "AccessoryOf" : Select(attrs={"class" : "form-select"})
        }

class EquipmentCheckout(ModelForm):
    class Meta:
        model = EquipmentModel
        fields = ["CheckOutLocation"]
        widgets = {
            "CheckOutLocation" : Textarea(attrs={"class" : "form-control", "label-text" : "Check out location:"}),
        }

class EmployeeCreationForm(UserCreationForm):
    is_manager = BooleanField(label="Is a manager:", required=True, widget=CheckboxInput())
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password1", "password2"]
