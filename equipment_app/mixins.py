from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponseRedirect
from django.views.generic.base import ContextMixin
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse

class BootstrapThemeMixin(ContextMixin):
    #Override get_context_data to tack on the user-theme 
    @staticmethod
    def AddUserThemeCookie(request: HttpRequest, context: dict[str: Any]):
        #theme-toggler.js will set a cookie called user-theme to tell use which theme to use when rendering the clients HTML view
        if "user-theme" in request.COOKIES:
            context["theme"] = request.COOKIES["user-theme"]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        # Add the theme to the context
        context = super().get_context_data(**kwargs)
        self.AddUserThemeCookie(self.request, context)
        return context
    
class ManagerNeeded(PermissionRequiredMixin):
    permission_required = ["equipment_app.can_edit"]
    
    # Redirect all manager needed logins to the login page
    def get_login_url(self) -> str:
        return reverse("login")
    
    # Redirect all unauthorized requests to the unauthorized page for all classes that subclass this one
    def handle_no_permission(self) -> HttpResponseRedirect:
        return HttpResponseRedirect(redirect_to=reverse("unauthorized"))
    
class LoginNeeded(LoginRequiredMixin):
    # Subclass LoginRequiredMixin in order to have each login required view redirect to the same login url
    def get_login_url(self) -> str:
        return reverse("login")