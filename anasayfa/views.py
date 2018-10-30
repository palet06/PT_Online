from django.shortcuts import render,HttpResponse
from django import forms


# Create your views here.
def index(request):
    return render(request,"index.html")
def ilkay(request):
    return render(request,"ilkay.html")

def hizmetler(request):
    return render(request,"hizmetler.html")