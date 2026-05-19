from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from core.models import BaseModel


class CustomUserModel(AbstractBaseUser, PermissionsMixin, BaseModel):
    class Meta:
        db_table = 'auth_user'

    class Role(models.TextChoices):
        BUYER = 'buyer', 'Покупець',
        SELLER = 'seller', 'Продаввець',
        MANAGER = 'manager', 'Менеджер',
        ADMIN = 'admin', 'Адміністратор',

    class AccountType(models.TextChoices):
        BASIC = 'basic', 'Базовий',
        PREMIUM = 'premium', 'Преміум'

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=7, choices=Role, default=Role.BUYER)
    account_type = models.CharField(max_length=7, choices=AccountType, default=AccountType.BASIC)

    USERNAME_FIELD = 'email'

