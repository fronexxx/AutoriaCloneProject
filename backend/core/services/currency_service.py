import requests


class CurrencyService:
    API_URL = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=11'

    @staticmethod
    def get_exchange_rates():
        response = requests.get(CurrencyService.API_URL)
        data = response.json()

        rates = {}

        for item in data:
            ccy = item['ccy']

            if ccy in ['USD', 'EUR']:
                rates[ccy] = {
                    'buy': float(item['buy']),
                    'sale': float(item['sale'])
                }

        return rates

    @staticmethod
    def convert_price(price, currency, exchange_rate):

        usd_rate = exchange_rate['USD']['sale']
        eur_rate = exchange_rate['EUR']['sale']

        if currency == "USD":
            usd = price
            uah = round(price * usd_rate, 2)
            eur = round(uah / eur_rate, 2)

        elif currency == "EUR":
            eur = price
            uah = round(price * eur_rate, 2)
            usd = round(uah / usd_rate, 2)

        else:  # UAH
            uah = price
            usd = round(price / usd_rate, 2)
            eur = round(price / eur_rate, 2)

        return {
            "USD": usd,
            "EUR": eur,
            "UAH": uah,
        }
