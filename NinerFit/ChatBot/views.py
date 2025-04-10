from django.shortcuts import render, redirect
from django.http import JsonResponse
from openai import OpenAI
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone
from django.contrib.auth.decorators import login_required


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

# Create your views here.
@login_required
def chatbot(request):
    chats = Chat.objects.filter(user=request.user)
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html', {'chats': chats})
 
 
def logout_view(request):
    logout(request)
    return redirect('../')