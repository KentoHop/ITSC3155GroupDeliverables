from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Start Page View
def start_page(request):
    return render(request, 'main/start.html')

# Home Page View (only accessible to logged-in users)
@login_required
def home(request):
    return render(request, 'main/home.html')
