from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.RepairHome, name='Repairhome'),
    path('search/', views.Search, name='search'),
    path('form/', views.Form, name='form'),
    path('product/<str:repair_id>',views.Product, name='product'),

]