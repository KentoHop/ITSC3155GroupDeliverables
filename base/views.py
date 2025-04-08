from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from openai import OpenAI

from .models import User, Chat

'''
Views are separated based on section.

Ctrl+F to search for one of the following:
- ### Authentification ###
- ### Home ###
- ### Chatbot ###
- 
'''

### Authentification ###
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

def registerPage(request):
    page = 'register'

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logout_view(request):
    logout(request)
    return redirect('../')

### Home ###

def home(request):
    return render(request, 'base/home.html')



### Chatbot ###
#set open AI API
your_api = '' #insert own api key here
client = OpenAI(api_key=your_api)

# Function to interact with OpenAI ChatGPT
def ask_openai(message):
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Use "gpt-4-turbo" if needed after development
        messages=[
            {"role": "system", "content": "You are a counselor supporting users trying to improve their mental health. If a user expresses a serious crisis, provide emergency contact resources such as 911."},
            {"role": "user", "content": message},
        ],
        max_tokens=150,
        temperature=0.7
    )
    answer = response.choices[0].message.content.strip()
    return answer

@login_required
def chatbot(request):
    chats = Chat.objects.filter(user=request.user)
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'base/chatbot.html', {'chats': chats})


### Health Score ###
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