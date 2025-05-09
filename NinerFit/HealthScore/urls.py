from django.urls import path
from . import views
from Authentication.views import login, register, logout

urlpatterns = [
    path('to-do-list/', views.toDoList, name="to-do-list"),
    path('addtodo/', views.addTodo, name='addtodo'),
    path('updatetodo/<int:pk>/', views.updateTodo, name='updatetodo'),
    path('deletetodo/<int:pk>/', views.deleteTodo, name='deletetodo'),
]