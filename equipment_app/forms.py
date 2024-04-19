from typing import Any
from django.forms import ModelForm, Textarea, TextInput, DateInput, Select, URLInput, BooleanField, CheckboxInput, ChoiceField
from django.contrib.auth.forms import UserCreationForm

from haystack.forms import SearchForm
from haystack.query import EmptySearchQuerySet, SearchQuerySet

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


class EquipmentCheckin(ModelForm):
    TurnedIn = BooleanField(label="Confirm Check In:", required=True, widget=CheckboxInput(attrs={"class" : "form-check-input"}))
    class Meta:
        model = EquipmentModel
        fields = []
        exclude = '__all__'

class EquipmentSearchForm(SearchForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices=[("Any", "Any")] + list(EquipmentModel.EQUIPMENT_CATEGORIES)
        self.fields['EquCategory'] = ChoiceField(label="Equipment Category: ", choices=choices, required=False, initial="Any")

    def search(self):
        sqs = super().search()
        
        if not self.is_valid():
            return self.no_query_found()
        
        if (Category := self.cleaned_data['EquCategory']):
            if(Category != "Any"):
                sqs = sqs.filter(equipment_type=self.cleaned_data['EquCategory'])

        return sqs