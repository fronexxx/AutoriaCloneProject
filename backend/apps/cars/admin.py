from django.contrib import admin

from .models import BrandModel, CarModel

admin.site.register(CarModel)
admin.site.register(BrandModel)
