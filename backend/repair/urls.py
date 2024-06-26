from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.RepairHometest, name='Repairhome'),
    path('search/', views.Search, name='search'),
    path('form/', views.Form, name='form'),
    path('updatestatus/<str:repair_id>/<str:status>', views.UpdateStatus, name='completeform'),
    path('completeform/<str:repair_id>/<str:condition>', views.CompleteForm, name='completeform'),
    path('updateform/<str:repair_id>', views.UpdateForm, name='updateform'),
    path('product/<str:repair_id>',views.Product, name='product'),
    path('print/<str:repair_id>',views.Print, name='pdf'),
    path('login/',views.Login, name='login'),


]