from django.urls import path
from . import views  # Ensure correct import

urlpatterns = [
    path('', views.start_page, name='index'),  # Change 'index' to 'start_page'
    path('home/', views.home, name='home'),  # Ensure 'home' view is included
]