from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request, 'base/login.html')

def home(request):
    return render(request, 'base/home.html')