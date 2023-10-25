from django.contrib import admin
from v1.user.models import User, WorkerCode
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'email', 'password', 'first_name',
                    'last_name', 'created_at', 'update_at')


@admin.register(WorkerCode)
class WorkerCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'worker_code')
