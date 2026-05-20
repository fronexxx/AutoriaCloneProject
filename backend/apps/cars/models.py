from django.db import models

from core.models import BaseModel


class BrandModel(models.Model):
    class Meta:
        db_table = 'car_brands'

    brand = models.CharField(max_length=255, unique=True)

class CarModel(BaseModel):
    class Meta:
        db_table = 'cars'
        ordering = ['id']

    name = models.CharField(max_length=255)
    brand = models.ForeignKey(BrandModel, on_delete=models.CASCADE, related_name='models')

