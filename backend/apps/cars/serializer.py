from rest_framework import serializers

from apps.cars.models import BrandModel, CarModel


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = (
            'id',
            'name',
            'brand'
        )

class BrandSerializer(serializers.ModelSerializer):
    models = CarSerializer(many=True)

    class Meta:
        model = BrandModel
        fields = (
            'id',
            'brand'
        )

