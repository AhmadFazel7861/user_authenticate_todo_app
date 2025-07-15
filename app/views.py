from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from .forms import UserForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from .models import Todo
from django.contrib.auth.decorators import login_required

@login_required
def todo_list(req):
    if req.method == "POST":
        task = req.POST.get('task')
        edit_task_name = req.POST.get('edit_task_name')

        if task:
            if edit_task_name:
                # This is an update operation
                try:
                    get_todo = Todo.objects.get(user=req.user, todo_name=edit_task_name)
                    get_todo.todo_name = task
                    get_todo.save()
                except Todo.DoesNotExist:
                    pass
            else:
                # This is a create operation
                Todo.objects.create(user=req.user, todo_name=task)
        return redirect('todo')

    todo = Todo.objects.filter(user=req.user)
    edit_task = req.GET.get('edit')  # task name to be edited
    return render(req, 'app/todo.html', {'todo': todo, 'update_task_name': edit_task})

def register(req):
    if req.method == "POST":
        form = UserForm(req.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserForm()    
    context = {'register':form}   
    return render(req,'app/signup.html', context=context)     

def user_login(req):
    if req.method == 'POST':
        form = LoginForm(req, data=req.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(req, username=username, password=password)
            if user is not None:
                login(req, user)
                return redirect('todo')
    else:
        form = LoginForm()
    context = {'log': form}
    return render(req, 'app/login.html', context)

def user_logout(req):
    auth.logout(req)
    return redirect('login')

def delete_task(req, name):
    get_todo = Todo.objects.get(user=req.user, todo_name=name)
    get_todo.delete()
    return redirect('todo')

def update_task(request, name):
    if request.method == "POST":
        task = request.POST.get('task')
        if task:
            try:
                get_todo = Todo.objects.get(user=request.user, todo_name=name)
                get_todo.todo_name = task
                get_todo.save()
            except Todo.DoesNotExist:
                pass
        return redirect('todo')
    else:
        return redirect(f'/todo/?edit={name}')
