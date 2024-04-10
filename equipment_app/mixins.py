from typing import Any
from django.http import HttpRequest
from django.views.generic.base import ContextMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse

class BootstrapThemeMixin(ContextMixin):
    #Override get_context_data to tack on the user-theme 
    @staticmethod
    def AddUserThemeCookie(request: HttpRequest, context: dict[str: Any]):
        if "user-theme" in request.COOKIES:
            context["theme"] = request.COOKIES["user-theme"]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        self.AddUserThemeCookie(self.request, context)
        return context
    
class ManagerNeeded(PermissionRequiredMixin):
    permission_required = ["equipment_app.can_edit"]
    
    def get_login_url(self) -> str:
        return reverse("login")