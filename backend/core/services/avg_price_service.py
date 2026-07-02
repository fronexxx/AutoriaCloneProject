from django.db.models import Avg, FloatField
from django.db.models.fields.json import KeyTextTransform
from django.db.models.functions import Cast

from core.constants.choices import StatusChoices

from apps.listings.models import ListingModel, ListingStatsModel


class AveragePriceService:

    @staticmethod
    def _update_stats(queryset, field_name):
        average = (
            queryset
            .annotate(
                usd_price=Cast(
                    KeyTextTransform("USD", "price_converted"),
                    FloatField()
                )
            )
            .aggregate(
                average=Avg("usd_price")
            )["average"]
        )
        average = round(average, 2) if average is not None else None
        stats = []

        for listing in queryset.select_related('stats'):
            setattr(listing.stats, field_name, average)
            stats.append(listing.stats)

        ListingStatsModel.objects.bulk_update(
            stats,
            [field_name]
        )

    @staticmethod
    def update_average_prices(listing):
        region_queryset = ListingModel.objects.filter(
            car__brand = listing.car.brand,
            car__name = listing.car.name,
            region = listing.region,
            status = StatusChoices.ACTIVE
        )

        country_queryset = ListingModel.objects.filter(
            car__brand = listing.car.brand,
            car__name = listing.car.name,
            status = StatusChoices.ACTIVE
        )

        AveragePriceService._update_stats(
            region_queryset,
            'avg_price_region'
        )

        AveragePriceService._update_stats(
            country_queryset,
            'avg_price_country'
        )


        