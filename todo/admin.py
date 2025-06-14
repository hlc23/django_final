from django.contrib import admin

from . import models
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)

class TodoAdmin(admin.ModelAdmin):
    list_display = ('owner', 'content', 'deadline', 'public', 'done', 'done_at', 'created_at')

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Todo, TodoAdmin)
