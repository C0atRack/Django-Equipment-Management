from typing import Any
import datetime
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.http.request import HttpRequest as HttpRequest
from django.urls import reverse
from django.views.generic import *
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import Permission, User

from .forms import *
from .models import *
from .mixins import *

# Create your views here.
class Stub(TemplateView, BootstrapThemeMixin):
    template_name = "equipment_app/stub.html"

class Index(TemplateView, BootstrapThemeMixin):
    template_name = "equipment_app/index.html"

class UnauthorizedView(TemplateView, BootstrapThemeMixin):
    template_name = "equipment_app/unauthorized.html"

#Equipment Creation View
class EquipmentCreation(CreateView, ManagerNeeded, BootstrapThemeMixin):
    form_class = EquipmentForm
    template_name = "equipment_app/equipment_form.html"
    model = EquipmentModel

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['ActionText'] = "Adding Equipment"
        return context
    
    
#Equipment Creation View
class EquipmentUpdate(UpdateView, ManagerNeeded, BootstrapThemeMixin):
    form_class = EquipmentForm
    template_name = "equipment_app/equipment_form.html"
    model = EquipmentModel

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['ActionText'] = f"Modifying {self.object}"
        return context

class EquipmentDelete(DeleteView, ManagerNeeded, BootstrapThemeMixin):
    model = EquipmentModel
    template_name = "equipment_app/equipment_delete.html"

    def get_success_url(self) -> str:
        return reverse("index")

class EquipmentCheckout(UpdateView, BootstrapThemeMixin):
    form_class = EquipmentCheckout
    model = EquipmentModel
    template_name = "equipment_app/equipment_form.html"
    def get_success_url(self) -> str:
        return self.object.get_absolute_url()
    
    def form_valid(self, form: EquipmentCheckout):
        object:EquipmentModel = self.object
        object.CheckedOutTo = Employee.objects.filter(AffUser=self.request.user).first()
        object.CheckOutDate = datetime.date.today()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['ActionText'] = f"Checking out {self.object}"
        return context
    

class Login(LoginView, BootstrapThemeMixin):
    next_page = "index"
    template_name = "equipment_app/login.html"

class Logout(LogoutView, BootstrapThemeMixin):
    template_name = "equipment_app/logout_success.html"

class Register(CreateView, BootstrapThemeMixin):
    template_name = "equipment_app/employee_register.html"
    manager_version = False
    form_class = EmployeeForm
    
    def get_success_url(self) -> str:
        return self.object.employee.get_absolute_url()

    def form_valid(self, form):
        NewUser: User= form.save()
        NewUser.username = NewUser.email
        NewEmployee = Employee()
        NewEmployee.AffUser = NewUser
        NewEmployee.save()
        return super().form_valid(form)
    
class EmployeeDetail(DeleteView, BootstrapThemeMixin):
    template_name = "equipment_app/employee_detail.html"
    model = Employee

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['employee_user'] = self.object.AffUser
        context['aff_equipment'] = EquipmentModel.objects.filter(CheckedOutTo=self.object)
        return context
    
class EmployeePermUpdate(UpdateView, BootstrapThemeMixin, ManagerNeeded):
    template_name = "equipment_app/equipment_form.html"
    form_class = EmployeeForm_Manager
    model = Employee

    def form_valid(self, form):
        Perm = Permission.objects.get(codename="can_edit")
        EmployeeUser: User = self.request.user
        if form.cleaned_data["is_manager"]:
            EmployeeUser.user_permissions.add(Perm)
        else:
            EmployeeUser.user_permissions.remove(Perm)
        return super().form_valid(form)
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['ActionText'] = f"Editing {self.object.AffUser.first_name} {self.object.AffUser.last_name}'s permissions"
        return context

    
class EquipmentList(ListView, BootstrapThemeMixin):
    paginate_by = 15
    model = EquipmentModel
    template_name = "equipment_app/equipment_list.html"

class EquipmentDetail(DetailView, BootstrapThemeMixin):
    model = EquipmentModel
    template_name = "equipment_app/equipment_detail.html"