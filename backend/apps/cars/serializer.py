from rest_framework import serializers

from apps.cars.models import BrandModel, CarModel


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = (
            'id',
            'name',
        )

class BrandSerializer(serializers.ModelSerializer):
    models = CarSerializer(many=True)

    class Meta:
        model = BrandModel
        fields = (
            'id',
            'brand',
            'models'
        )

    def create(self, validated_data: dict):
        models = validated_data.pop('models')
        brand = BrandModel.objects.create(**validated_data)
        for model in models:
            CarModel.objects.create(brand=brand, **model)
        return brand

class CarRequestSerializer(serializers.Serializer):
    brand = serializers.CharField(max_length=255)
    models = CarSerializer(many=True)


