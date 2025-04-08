from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from .models import User

# Create your views here.

def landing(request):
    return render(request, 'base/landing.html')

def loginPage(request):
    page = 'login'

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home/')  # Redirect to the homepage after successful login
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
            return redirect('login')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page = 'register'

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def home(request):
    return render(request, 'base/home.html')

def healthScore(request):
    return render(request, 'base/healthscore.html')

def toDoList(request):
    return render(request, 'base/todolist.html')

def suggestions(request):
    return render(request, 'base/suggestions.html')

def chatbot(request):
    return render(request, 'base/chatbot.html')

def profile(request):
    return render(request, 'base/profile.html')

def settings(request):    
    return render(request, 'base/settings.html')


# todo list
@login_required(login_url='login')
def todo(request):
    return render(request, 'base/todolist.html')