from django.urls import path
from . import views


urlpatterns = [
    path('', views.zakup_main, name='zakup_main'),
    #path('zakup/last/', views.zakup_last, name='zakup_last'),
    path('zakup/<int:pk>/', views.zakup_detail, name='zakup_detail'),
    #path('zakup/podsumowanie/', views.zakup_month, name='zakup_month'),
    #path('zakup/edit/', views.zakup_nowy, name="zakup_nowy"),
    #path('zakup/podsumowanie/', views.zakup_month, name='zakup_month'),
    path('zakup/day_detail/', views.zakup_day_detail, name='zakup_day_detail'),
    path('zakup/month_details/', views.zakup_month_detail, name='zakup_month_detail'),
    path('zakup/delete/<int:pk>/', views.zakup_delete, name='zakup_delete'),
]
