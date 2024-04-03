from django.urls import path
from . import views


urlpatterns = [
    path('stub', views.Stub.as_view(), name="stub"),
    path('', views.Index.as_view(), name="index"),
    
    #Authentication Views
    path('logout', views.Logout.as_view(), name="logout"),
]