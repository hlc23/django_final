"""
URL configuration for django_final project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('todo/public/', views.public_todo, name='public_todo'),
    path('todo/mine/', views.my_todo_list, name='my_todo'),
    path('todo/create/', views.create_todo, name='create_todo'),
    path('todo/<int:todo_id>/edit/', views.edit_todo, name='edit_todo'),
    path('todo/<int:todo_id>/done/', views.mark_todo_done, name='mark_todo_done'),
    path('todo/<int:todo_id>/delete/', views.delete_todo, name='delete_todo'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    
    path('api/todo/<int:todo_id>/status/', views.api_todo_status, name='todo_status'),
]
