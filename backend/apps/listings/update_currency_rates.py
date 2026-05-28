from config.celery import app
from core.services.currency_service import CurrencyService

from apps.listings.models import ListingModel


@app.task
def update_currency_rates():
    listings = ListingModel.objects.all()
    rates = CurrencyService.get_exchange_rates()

    for listing in listings:
        converted_price = CurrencyService.convert_price(
            price=listing.price,
            currency=listing.currency,
            exchange_rate=rates
        )

        listing.exchange_rate = rates
        listing.price_converted = converted_price

        listing.save()

