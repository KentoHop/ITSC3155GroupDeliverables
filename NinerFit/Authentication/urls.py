from django.urls import path
from . import views
from Authentication.views import login, register, logout

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
]