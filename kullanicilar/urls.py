from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views


app_name = "kullanicilar"

urlpatterns = [
    url(r'^kayit/',views.kayit,name = "kayit"),
    url(r'^giris/',views.giris,name = "giris"),
    url(r'^cikis/',views.cikis,name = "cikis"),
    url(r'^profil/',views.profil_goruntule,name = "profil_goruntule"),
    url(r'^sifre/',views.sifre,name = "sifre"),
    url(r'^profilegitmen/',views.profilegitmen,name = "profilegitmen"),
    url(r'^pt_al/',views.pt_al,name = "pt_al"),
    #path('uretim/',views.uretim,name = "uretim"),
]