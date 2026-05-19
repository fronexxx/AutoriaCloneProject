from django.db import models


class Role(models.TextChoices):
    BUYER = 'buyer', 'Покупець',
    SELLER = 'seller', 'Продавець',
    MANAGER = 'manager', 'Менеджер',
    ADMIN = 'admin', 'Адміністратор'


class AccountType(models.TextChoices):
    BASIC = 'basic', 'Базовий',
    PREMIUM = 'premium', 'Преміум'