from typing import Any
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import *
from django.contrib.auth.views import LoginView, LogoutView

from .forms import *
from .models import *

# Create your views here.
class Stub(TemplateView):
    template_name = "equipment_app/stub.html"

class Index(TemplateView):
    template_name = "equipment_app/index.html"

#Equipment Creation View
class EquipmentCreation(CreateView):
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
        context['creating'] = True
        return context
    
#Equipment Creation View
class EquipmentUpdate(UpdateView):
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
        context['creating'] = False
        print(f"Context: {context}")
        return context


class Logout(LogoutView):
    next_page = "index"

class EquipmentList(ListView):
    paginate_by = 15
    model = EquipmentModel
    template_name = "equipment_app/equipment_list.html"