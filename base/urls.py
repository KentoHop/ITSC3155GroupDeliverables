from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name="landing"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('home/', views.home, name="home"),
    path('health-score/', views.healthScore, name="health-score"),
    path('to-do-list/', views.toDoList, name="to-do-list"),
    path('suggestions/', views.suggestions, name="suggestions"),
    path('chatbot/', views.chatbot, name="chatbot"),
    path('profile/', views.profile, name="profile"),
    path('settings/', views.settings, name="settings"),
]