from django.contrib.auth.models import UserManager as Manager

from apps.users.roles_and_account_type import Role


class CustomUserManager(Manager):
    def create_user(self, email = ..., password = ..., **extra_fields):
        role = extra_fields.get('role', Role.BUYER)

        if not email:
            raise ValueError('Email must be provided...')

        if not password:
            raise ValueError('Password must be provided')

        if role == Role.ADMIN:
            extra_fields.setdefault('is_superuser', True)
            extra_fields.setdefault('is_staff', True)
        elif role == Role.MANAGER:
            extra_fields.setdefault('is_superuser', False)
            extra_fields.setdefault('is_staff', True)
        else:
            extra_fields.setdefault('is_superuser', False)
            extra_fields.setdefault('is_staff', False)

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email = ..., password = ..., **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', Role.ADMIN)

        if extra_fields['is_active'] is not True:
            raise ValueError('Superuser must be is_active')
        if extra_fields['is_staff'] is not True:
            raise ValueError('Superuser must be is_staff')
        if extra_fields['is_superuser'] is not True:
            raise ValueError('Superuser must be is_superuser')
        if extra_fields['role'] != 'admin':
            raise ValueError('Superuser must be admin')

        user = self.create_user(email=email, password=password, **extra_fields)
        return user




