from rest_framework import serializers

from apps.cars.serializer import CarDetailSerializer, CarSerializer
from apps.listings.models import ListingModel, ListingStatsModel


class ListingSerializer(serializers.ModelSerializer):
    car = CarDetailSerializer(read_only=True)

    class Meta:
        model = ListingModel
        fields = (
            'id',
            'title',
            'description',
            'car',
            'price',
            'currency',
            'region',
            'dealer',
            'owner',
            'exchange_rate',
            'status',
            'is_clean',
            'edit_attempts'
        )

class ListingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingModel
        fields = (
            'title',
            'description',
            'car',
            'price',
            'currency',
            'region',
        )

    @staticmethod
    def validate_price(value):
        if value <= 0:
            raise serializers.ValidationError('Price must be grater that 0')
        return value


class ListingStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingStatsModel
        fields = (
            'views_total',
            'views_daily',
            'views_weekly',
            'views_monthly',
            'avg_price_region',
            'avg_price_country',
            'listing',
        )
        read_only_fields = (
            'views_total',
            'views_daily',
            'views_weekly',
            'views_monthly',
            'avg_price_region',
            'avg_price_country',
            'listing'
        )
