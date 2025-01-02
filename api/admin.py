from django.contrib import admin
from .models import CustomUser, Task
# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'date_joined', 'is_staff', 'is_active']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'created', 'is_done']
