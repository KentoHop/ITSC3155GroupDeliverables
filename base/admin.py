from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .forms import UserCreationForm, UserChangeForm
from .models import User

admin.site.register(User)

class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = [
        "email",
    ]