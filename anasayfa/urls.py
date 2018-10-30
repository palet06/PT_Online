from django.contrib import admin
from django.urls import path
from . import views


app_name = "anasayfa"

urlpatterns = [
    path('cv/',views.ilkay,name = "ilkay"),
    path('hizmetler/',views.hizmetler,name = "hizmetler"),

]