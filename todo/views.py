from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages

from .models import User, Todo
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


def index(request: HttpRequest) -> HttpResponse:
    todos = Todo.objects.filter(public=True)
    todos = sorted(todos, key=lambda x: (x.deadline < timezone.now(), x.deadline, x.done))

    if request.session.get('username'):
        messages.success(request, f'歡迎回來！ {request.session["username"]}')
    
    return render(request, 'index.html', {'todo_list': todos})

def public_todo(request: HttpRequest) -> HttpResponse:
    todos = Todo.objects.filter(public=True)
    todos = sorted(todos, key=lambda x: (x.deadline < timezone.now(), x.deadline, x.done))
    return render(request, 'public_todo.html', {'todo_list': todos})

def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next', '/')
        try:
            user = User.objects.get(username=username, password=password)
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            return redirect(next_url)
        except User.DoesNotExist:
            messages.warning(request, '帳號或密碼錯誤')
            return render(request, 'login.html', {'next': next_url})

    next_url = request.GET.get('next', '/')
    return render(request, 'login.html', {'next': next_url})

def logout_view(request: HttpRequest) -> HttpResponse:
    request.session.flush()
    messages.info(request, '已登出成功!')
    return redirect('/')

def my_todo_list(request: HttpRequest) -> HttpResponse:
    if not request.session.get('user_id'):
        messages.warning(request, '請先登入')
        return redirect(f'/login/?next={request.path}')
    user_id = request.session['user_id']
    todos = Todo.objects.filter(owner=request.session['user_id'])
    todos = sorted(todos, key=lambda x: (x.deadline < timezone.now(), x.deadline, x.done))

    return render(request, 'todo_list.html', {'todo_list': todos})

def create_todo(request: HttpRequest) -> HttpResponse:
    if not request.session.get('user_id'):
        messages.warning(request, '請先登入')
        return redirect(f'/login/?next={request.path}')
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
        messages.warning(request, '請先登入')
        return redirect(f'/login/?next={request.path}')

    user_id = request.session['user_id']
    todos = Todo.objects.filter(owner_id=user_id)
    datas = {
        'user': User.objects.get(id=user_id),
        'todo_list': Todo.objects.filter(owner_id=user_id),
        'done_todos': todos.filter(owner_id=user_id, done=True),
        'running_todos': todos.filter(owner_id=user_id, done=False),
    }
    return render(request, 'profile.html', datas)


def mark_todo_done(request: HttpRequest, todo_id: int) -> HttpResponse:
    if not request.session.get('user_id'):
        messages.warning(request, '請先登入')
        return redirect(f'/login/?next={request.path}')
    
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
    
def delete_todo(request: HttpRequest, todo_id: int) -> HttpResponse:
    if not request.session.get('user_id'):
        messages.warning(request, '請先登入')
        return redirect(f'/login/?next={request.path}')
    
    if request.method == 'POST':
        try:
            user_id = request.session['user_id']
            todo = Todo.objects.get(id=todo_id, owner_id=user_id)
            todo.delete()
        except Todo.DoesNotExist:
            pass  # is todo not exist or not owned by user, ignore
    
    return redirect('/todo/mine/')

def edit_todo(request: HttpRequest, todo_id: int) -> HttpResponse:
    if not request.session.get('user_id'):
        messages.warning(request, '請先登入')
        return redirect(f'/login/?next={request.path}')
    
    user_id = request.session['user_id']
    try:
        todo = Todo.objects.get(id=todo_id, owner_id=user_id)
    except Todo.DoesNotExist:
        messages.error(request, '找不到該待辦事項')
        return redirect('/todo/mine/')
    
    if request.method == 'POST':
        content = request.POST.get('content')
        deadline = request.POST.get('deadline')
        public = bool(request.POST.get('public'))
        
        todo.content = content
        todo.deadline = deadline
        todo.public = public
        todo.save()
        
        messages.success(request, '待辦事項已更新')
        return redirect('/todo/mine/')
    
    return render(request, 'edit_todo.html', {'todo': todo})

def api_todo_status(request: HttpRequest, todo_id: int) -> HttpResponse:
    try:
        todo = Todo.objects.get(id=todo_id)
        
        if todo.public:
            return JsonResponse({
                'id': todo.id,
                'done': todo.done,
            })
        else:
            if request.session.get('user_id') != todo.owner_id:
                return HttpResponse(status=403)
            return JsonResponse({
                'id': todo.id,
                'done': todo.done,
            })

    except Todo.DoesNotExist:
        return HttpResponse(status=404)