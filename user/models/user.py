from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .role import Role
from user.managers import UserManager
from django.contrib.auth.models import PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    class Status(models.IntegerChoices):
        ACTIVE = 1, 'Active'
        BLOCKED = 2, 'Blocked'
        INVITED = 3, 'Invited'

    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=255, null=True, blank=True)

    password = models.CharField(max_length=255)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, default=3)
    status = models.IntegerField(choices=Status.choices, default=Status.ACTIVE)
    email_verified = models.BooleanField(default=False)
    avatar_url = models.URLField(blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    class Meta:
        db_table = 'user'


