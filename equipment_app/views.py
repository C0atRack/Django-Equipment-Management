from typing import Any
import datetime
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.http.request import HttpRequest as HttpRequest
from django.urls import reverse
from django.views.generic import *
from django.views.generic.detail import SingleObjectMixin
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

class EquipmentCheckout(LoginNeeded, UpdateView, BootstrapThemeMixin):
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
    template_name = "equipment_app/login.html"
    
    def get_default_redirect_url(self):
        return self.request.user.employee.get_absolute_url()

class Logout(LogoutView, BootstrapThemeMixin):
    template_name = "equipment_app/logout_success.html"

class Register(CreateView, BootstrapThemeMixin):
    template_name = "equipment_app/employee_register.html"
    manager_version = False
    form_class = EmployeeForm
    
    def get_success_url(self) -> str:
        return reverse("login")

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
    
class EmployeePermUpdate(ManagerNeeded, UpdateView, BootstrapThemeMixin):
    template_name = "equipment_app/equipment_form.html"
    form_class = EmployeeForm_Manager
    model = Employee

    def form_valid(self, form):
        Perm = Permission.objects.get(codename="can_edit")
        EmployeeUser: User = self.object.AffUser
        print(form.cleaned_data["is_manager"])
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

class EquipmentDetail(DetailView,  BootstrapThemeMixin):
    model = EquipmentModel
    template_name = "equipment_app/equipment_detail.html"


class EquipmentCheckIn(UpdateView, LoginRequiredMixin, BootstrapThemeMixin):
    model = EquipmentModel
    form_class = EquipmentCheckin
    template_name = "equipment_app/equipment_form.html"

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()

    def form_valid(self, form):
        #Unset fields
        self.object.CheckedOutTo = None
        self.object.CheckOutLocation = ""
        return super().form_valid(form)
    
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        ReqUser: User = self.request.user
        # If an employee is attempting to check in equipment
        if (self.object.CheckedOutTo == None):
            # If the equipment is not checked out
            return HttpResponseRedirect(reverse("unauthorized"))
        elif (ReqUser.employee != None):
            # If the employee is not a manager (Can force check in all equipment)
            if(not ReqUser.has_perm(Permission.objects.get(codename="can_edit"))):
                if self.object.CheckedOutTo.AffUser != ReqUser:
                    return HttpResponseRedirect(reverse("unauthorized"))
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['ActionText'] = f"Turning in {self.object}"
        context['SubActionText'] = f"Please return {self.object} to: {self.object.CheckInLocation}"
        return context