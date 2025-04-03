from django.urls import path
from .views import chatbot
 
urlpatterns = [
    path('', chatbot, name='chatbot'),  # This should match the main `urls.py`
]