from django.shortcuts import render, redirect
from django.http import JsonResponse
from openai import OpenAI

your_api = '' #insert own api key here
client = OpenAI(api_key=your_api)

# Function to interact with OpenAI ChatGPT
def ask_openai(message):
    response = client.chat.completions.create(
        model="gpt-4",  # Use "gpt-4-turbo" if needed after development done
        messages=[{"role": "user", "content": message}],
        max_tokens=150,
        temperature=0.7
    )
    answer = response.choices[0].message.content.strip()
    return answer

# Create your views here.
def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def logout(request):
    return redirect('login')