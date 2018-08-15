from django.urls import path
from . import views


urlpatterns = [
    path('', views.zakup_list, name='zakup_list'),
    path('zakup/edit/', views.zakup_nowy, name="zakup_nowy"),
    path('zakup/<int:pk>/', views.zakup_detail, name='zakup_detail'),
]
