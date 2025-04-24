from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.start_page, name='start'),
    path('home/', views.home, name='home'),
    path('health_score/', views.health_score_view, name='health_score'),
    path('logout/', LogoutView.as_view(next_page='start'), name='logout'),
    path('calorie_detail/', views.calorie_detail, name='calorie_detail'),
    path('water_detail/', views.water_detail, name='water_detail'),
    path('sleep_detail/', views.sleep_detail, name='sleep_detail'),
    path('usda/search/', views.usda_food_search, name='usda_food_search'),
    path('suggestions/', views.suggestion, name='suggestions'),
]