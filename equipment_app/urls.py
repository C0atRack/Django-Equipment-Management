from django.urls import path
from . import views


urlpatterns = [
    path('stub', views.Stub.as_view(), name="stub"),
    path('', views.Index.as_view(), name="index"),

    #Authentication Views
    path('login', views.Login.as_view(), name="login"),
    path('logout', views.Logout.as_view(), name="logout"),
    path("equipment_list", views.EquipmentList.as_view(), name="equipment-list"),
    path("equipment_detail/<int:pk>", views.EquipmentDetail.as_view(), name="equipment-detail"),
    path('equipment_create/', views.EquipmentCreation.as_view(), name="equipment-creation"),
    path('equipment_edit/<int:pk>', views.EquipmentUpdate.as_view(), name="equipment-update"),
    path('equipment_delete/<int:pk>', views.EquipmentDelete.as_view(), name="equipment-delete"),
    path('equipment_detail/<int:pk>', views.Stub.as_view(), name="equipment-detail"),
]