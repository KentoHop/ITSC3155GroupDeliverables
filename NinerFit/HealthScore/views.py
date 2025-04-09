from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from .models import User


# Create your views here.
def healthScore(request):
    return render(request, 'HealthScore/templates/healthscore.html')

def toDoList(request):
    return render(request, 'HealthScore/templates/todolist.html')

def suggestions(request):
    return render(request, 'HealthScore/templates/suggestions.html')

