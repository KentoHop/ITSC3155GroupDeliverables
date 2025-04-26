from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from .models import User, TodoItem


# Health Score
def healthScore(request):
    return render(request, 'healthscore.html')

# Suggestions
def suggestions(request):
    return render(request, 'suggestions.html')


# to do list
@login_required(login_url='login')
def toDoList(request):
    todos = TodoItem.objects.filter(user=request.user).order_by('-created_at') # `order_by` to sort the tasks by creation date
    return render(request, 'HealthScore/templates/todolist.html',{'todos': todos})

# add todo   
@login_required(login_url='login')
def addTodo(request):
    if request.method == 'POST':
        title = request.POST.get('title','Untitled task') # default title
        description = request.POST.get('description')
        todo = TodoItem(user=request.user, title=title, description=description)
        todo.save()
        messages.success(request, 'Task added successfully')
        return redirect('to-do-list')
    return render(request, 'HealthScore/templates/todolist.html')

# update todo
@login_required(login_url='login')
def updateTodo(request, pk):
    todo = get_object_or_404(TodoItem, id=pk, user=request.user) # Get the todo item with the given primary key and ensure it belongs to the current user
    if request.method == 'POST':
        todo.title = request.POST.get('title')
        todo.description = request.POST.get('description')
        todo.completed = 'completed' in request.POST
        todo.save()
        messages.success(request, 'Task updated successfully')
        return redirect('to-do-list')
    return render(request, 'HealthScore/templates/updatetodo.html', {'todo': todo})

# delete todo
@login_required(login_url='login')
def deleteTodo(request, pk):
    todo = get_object_or_404(TodoItem, id=pk, user=request.user) # Get the todo item with the given primary key and ensure it belongs to the current user
    if request.method == 'POST':
        todo.delete()
        messages.success(request, 'Task deleted successfully')
        return redirect(request.META.get('HTTP_REFERER', 'to-do-list'))
    return render(request, 'HealthScore/templates/deletetodo.html', {'todo': todo})

