from django.contrib.auth import get_user_model
from django.db import models

from core.constants.choices import RegionChoices
from core.models import BaseModel

from apps.users.roles_and_account_type import Role

UserModel = get_user_model()

AVAILABLE_ROLES = [
    (Role.ADMIN, 'Admin'),
    (Role.MANAGER, 'Manager'),
    (Role.SELLER, 'Seller'),
]

class DealerModel(BaseModel):
    class Meta:
        db_table = 'dealers'

    name = models.CharField(max_length=255)
    region = models.CharField(max_length=30, choices=RegionChoices)
    address = models.CharField(max_length=255, null=True, blank=True)


class DealerStaffModel(models.Model):
    class Meta:
        db_table = 'dealer_staff'

    dealer = models.ForeignKey(DealerModel, on_delete=models.CASCADE, related_name='staff')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='dealer_roles')
    role = models.CharField(max_length=7, choices=AVAILABLE_ROLES)

