from django.core.management.base import BaseCommand

from apps.users.models import CustomUserModel
from apps.users.roles_and_account_type import AccountType, Role


class Command(BaseCommand):

    def handle(self, *args, **options):

        if not CustomUserModel.objects.filter(email="admin@test.com").exists():
            CustomUserModel.objects.create_superuser(
                email="admin@test.com",
                password="admin123",
            )

        if not CustomUserModel.objects.filter(email="manager@test.com").exists():
            CustomUserModel.objects.create_user(
                email="manager@test.com",
                password="manager123",
                role=Role.MANAGER,
                account_type=AccountType.PREMIUM,
                is_active=True,
            )

        if not CustomUserModel.objects.filter(email="premium@test.com").exists():
            CustomUserModel.objects.create_user(
                email="premium@test.com",
                password="premium123",
                role=Role.SELLER,
                account_type=AccountType.PREMIUM,
                is_active=True,
            )

        if not CustomUserModel.objects.filter(email="basic@test.com").exists():
            CustomUserModel.objects.create_user(
                email="basic@test.com",
                password="basic123",
                role=Role.SELLER,
                account_type=AccountType.BASIC,
                is_active=True,
            )

        if not CustomUserModel.objects.filter(email="buyer@test.com").exists():
            CustomUserModel.objects.create_user(
                email="buyer@test.com",
                password="buyer123",
                role=Role.BUYER,
                account_type=AccountType.BASIC,
                is_active=True,
            )

        self.stdout.write(
            self.style.SUCCESS("Test users created successfully")
        )