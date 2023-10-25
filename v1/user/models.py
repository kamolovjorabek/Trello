from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from v1.user.managers import UserManager
from v1.home.models import DefaultAbstract
# Create your models here.


class User(AbstractBaseUser, PermissionsMixin, DefaultAbstract):
    phone = models.CharField(max_length=13, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.first_name

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ('first_name', 'last_name')


class WorkerCode(DefaultAbstract):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    worker_code = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        unique_together = ('user',)

