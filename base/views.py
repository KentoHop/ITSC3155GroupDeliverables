from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render

from .models import User

# Create your views here.

def landing(request):
    return render(request, 'base/landing.html')

def loginPage(request):
    page = 'login'

    if request.method == 'POST':
        email = request.POST.get('email')
        user = authenticate(request, email=email)
        if user is not None:
            login(request, user)
            return redirect('/home/')
        else:
            # Return an 'invalid login' error message.
            return redirect('/login/')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def registerPage(request):
    page = 'register'

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def home(request):
    return render(request, 'base/home.html')

def healthScore(request):
    return render(request, 'base/healthscore.html')