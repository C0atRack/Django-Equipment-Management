from django.views.generic import *
from django.contrib.auth.views import LoginView, LogoutView

# Create your views here.
class Stub(TemplateView):
    template_name = "equipment_app/stub.html"

class Index(TemplateView):
    template_name = "equipment_app/index.html"

class Logout(LogoutView):
    next_page = "index"