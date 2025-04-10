from django.urls import path
from .views import profile, ChangePasswordView

urlpatterns = [
    path('', profile, name='profile'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
]
