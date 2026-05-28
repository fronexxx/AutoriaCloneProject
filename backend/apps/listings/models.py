from django.contrib.auth import get_user_model
from django.db import models

from core.constants.choices import CurrencyChoices, RegionChoices, StatusChoices
from core.models import BaseModel

from apps.cars.models import CarModel
from apps.dealers.models import DealerModel

UserModel = get_user_model()



class ListingModel(BaseModel):
    class Meta:
        db_table = 'listings'
        ordering  = ['id']

    title = models.CharField(max_length=20)
    description = models.TextField()
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='listings')
    car = models.ForeignKey(CarModel, on_delete=models.PROTECT)
    price = models.FloatField()
    price_converted = models.JSONField(default=dict)
    currency = models.CharField(max_length=3, choices=CurrencyChoices)
    exchange_rate = models.JSONField(blank=True, null=True)
    region = models.CharField(max_length=30, choices=RegionChoices)
    status = models.CharField(max_length=10, choices=StatusChoices, default=StatusChoices.PENDING)
    edit_attempts = models.IntegerField(default=0)
    is_clean = models.BooleanField(default=True)

    dealer = models.ForeignKey(DealerModel, on_delete=models.SET_NULL, null=True, blank=True,  related_name='listings')

class ListingStatsModel(models.Model):
    class Meta:
        db_table = 'listing_stats'

    views_total = models.IntegerField(default=0)
    views_daily = models.IntegerField(default=0)
    views_weekly = models.IntegerField(default=0)
    views_monthly = models.IntegerField(default=0)
    avg_price_region = models.FloatField(null=True, blank=True)
    avg_price_country = models.FloatField(null=True, blank=True)
    listing = models.OneToOneField(ListingModel, on_delete=models.CASCADE, related_name='stats')

