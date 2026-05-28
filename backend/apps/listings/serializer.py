from rest_framework import serializers
from rest_framework.request import Request

from apps.cars.serializer import CarDetailSerializer
from apps.listings.models import ListingModel, ListingStatsModel
from apps.users.roles_and_account_type import AccountType


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
            'price_converted',
            'exchange_rate',
            'status',
            'is_clean',
            'edit_attempts',
        )


class ListingDetailSerializer(serializers.ModelSerializer):
    car = CarDetailSerializer(read_only=True)
    stats = serializers.SerializerMethodField()

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
            'price_converted',
            'exchange_rate',
            'status',
            'is_clean',
            'edit_attempts',
            'stats'
        )

    def get_stats(self, obj):
        request: Request = self.context.get('request')

        if not request:
            return None

        if request.user.account_type != AccountType.PREMIUM:
            return None

        try:
            return ListingStatsSerializer(obj.stats).data
        except ListingStatsModel.DoesNotExist:
            return None


class ListingCreateUpdateDeleteSerializer(serializers.ModelSerializer):
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
