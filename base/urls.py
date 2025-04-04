from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name="landing"),
    path('login/', views.login_view, name="login"),
    path('register/', views.register_view, name="register"),
    path('home/', views.home, name="home"),
    path('chatbot/', views.chatbot, name="chatbot"),
    path('logout/', views.logout_view, name="logout")
    
]