from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.chatbot, name='chatbot'),  # This should match the main `urls.py`
    path('logout', views.logout_view, name='logout'),
]