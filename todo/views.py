from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .models import User, Todo
from django.utils import timezone
from .forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            User.objects.create(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def index(request):
    todos = Todo.objects.filter(public=True).order_by('deadline')
    return render(request, 'index.html', {'todo_list': todos})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username, password=password)
            request.session['user_id'] = user.id
            return redirect('/')
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': '帳號或密碼錯誤'})
    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()
    return redirect('/')

def my_todo_list(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    user_id = request.session['user_id']
    todos = Todo.objects.filter(owner_id=user_id)
    return render(request, 'todo_list.html', {'todo_list': todos})

def create_todo(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    if request.method == 'POST':
        content = request.POST.get('content')
        deadline = request.POST.get('deadline')
        public = bool(request.POST.get('public'))
        Todo.objects.create(
            owner_id=request.session['user_id'],
            content=content,
            deadline=deadline,
            public=public,
            created_at=timezone.now()
        )
        return redirect('/todo/mine/')
    return render(request, 'form.html')

def profile(request: HttpRequest) -> HttpResponse:
    if not request.session.get('user_id'):
        return redirect('/login/')

    user_id = request.session['user_id']
    todos = Todo.objects.filter(owner_id=user_id)
    datas = {
        'user': User.objects.get(id=user_id),
        'todo_list': Todo.objects.filter(owner_id=user_id),
        'done_todos': todos.filter(owner_id=user_id, done=True),
        'running_todos': todos.filter(owner_id=user_id, done=False),
    }
    return render(request, 'profile.html', datas)


def mark_todo_done(request, todo_id):
    if not request.session.get('user_id'):
        return redirect('/login/')
    
    if request.method == 'POST':
        try:
            user_id = request.session['user_id']
            todo = Todo.objects.get(id=todo_id, owner_id=user_id)
            todo.done = True
            todo.done_at = timezone.now()
            todo.save()
        except Todo.DoesNotExist:
            pass  # if todo does not exist or not owned by user, ignore
    
    return redirect('/todo/mine/')
    
def delete_todo(request, todo_id):
    if not request.session.get('user_id'):
        return redirect('/login/')
    
    if request.method == 'POST':
        try:
            user_id = request.session['user_id']
            todo = Todo.objects.get(id=todo_id, owner_id=user_id)
            todo.delete()
        except Todo.DoesNotExist:
            pass  # is todo not exist or not owned by user, ignore
    
    return redirect('/todo/mine/')
