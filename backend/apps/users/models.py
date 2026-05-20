from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from core.models import BaseModel

from apps.users.managers import CustomUserManager
from apps.users.roles_and_account_type import AccountType, Role


class CustomUserModel(AbstractBaseUser, PermissionsMixin, BaseModel):
    class Meta:
        db_table = 'auth_user'
        ordering = ['id']

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=7, choices=Role)
    previous_role = models.CharField(max_length=7, blank=True, null=True, choices=Role, default=None)
    account_type = models.CharField(max_length=7, choices=AccountType, default=AccountType.BASIC)

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()



class ProfileModel(BaseModel):
    class Meta:
        db_table = 'profile'

    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    user = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE, related_name='profile')


