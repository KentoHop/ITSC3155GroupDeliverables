from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm
from django import forms
from .models import TodoItem

from .models import User

class UserCreationForm(AdminUserCreationForm):
    class Meta:
        model = User
        fields = ('email', )

class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', )
        
class todoForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ('title', 'description', 'completed')