from django.urls import path
from . import views


urlpatterns = [
    path('', views.zakup_list, name='zakup_list'),
    path('add/', views.zakup_nowy, name="zakup_add"),
    path('<int:pk>/', views.zakup_detail, name='zakup_detail'),
]
