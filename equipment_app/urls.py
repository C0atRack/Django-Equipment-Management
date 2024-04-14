from django.urls import path
from . import views


urlpatterns = [
    path('stub', views.Stub.as_view(), name="stub"),
    path('', views.Index.as_view(), name="index"),

    #Authentication Views
    path('login', views.Login.as_view(), name="login"),
    path('logout', views.Logout.as_view(), name="logout"),
    path('user/profile/<int:pk>', views.EmployeeDetail.as_view(), name="profile"),
    path('user/profile/<int:pk>/perm', views.EmployeePermUpdate.as_view(), name="update-perms"),
    path('register', views.Register.as_view(), name="register"),
    path('unauthorized', views.UnauthorizedView.as_view(), name="unauthorized"),
    path("equipment/list", views.EquipmentList.as_view(), name="equipment-list"),
    path("equipment/<int:pk>", views.EquipmentDetail.as_view(), name="equipment-detail"),
    path('equipment/create/', views.EquipmentCreation.as_view(), name="equipment-creation"),
    path('equipment/edit/<int:pk>', views.EquipmentUpdate.as_view(), name="equipment-update"),
    path('equipment/delete/<int:pk>', views.EquipmentDelete.as_view(), name="equipment-delete"),
    path('equipment/checkout/<int:pk>', views.EquipmentCheckout.as_view(), name="equipment-checkout"),
    path('equipment/checkin/<int:pk>', views.EquipmentCheckIn.as_view(), name="equipment-checkin"),
]