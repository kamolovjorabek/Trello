from django.contrib import admin
from v1.home.models import Board, Column, Task, WorkerMessage, ActivWorker
# Register your models here.


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'user', 'created_at', 'update_at')


@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'board', 'created_at', 'update_at')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'created_at', 'update_at')


@admin.register(WorkerMessage)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'board', 'inviter', 'added', 'created_at')


@admin.register(ActivWorker)
class ActivWorkerAdmin(admin.ModelAdmin):
    list_display = ('id', 'board', 'inviter')

