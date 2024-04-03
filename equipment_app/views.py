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
    template_name = "equipment_app/equipmentform.html"

    def get_success_url(self) -> str:
        return reverse("index")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.save()
        return super().form_valid(form)

class Logout(LogoutView):
    next_page = "index"