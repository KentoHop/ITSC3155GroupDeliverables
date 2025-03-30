from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name="landing"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('home/', views.home, name="home"),
    path('health-score/', views.healthScore, name="health-score"),
]