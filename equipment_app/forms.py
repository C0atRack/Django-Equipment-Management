from typing import Any
from django.forms import ModelForm, Textarea, TextInput, DateInput, Select, URLInput, BooleanField, CheckboxInput, Form
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

class EmployeeForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password1", "password2"]

class EmployeeForm_Manager(ModelForm):
    is_manager = BooleanField(label="Is a manager:", required=False, widget=CheckboxInput(attrs={"class" : "form-check-input"}))
    class Meta:
        model = Employee
        fields = []
        exclude = '__all__'


class EquipmentCheckin(Form):
    TurnedIn = BooleanField(label="Confirm Check In:", required=True, widget=CheckboxInput(attrs={"class" : "form-check-input"}))