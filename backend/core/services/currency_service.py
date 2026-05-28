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
        converted = {}

        usd_rate = exchange_rate['USD']['sale']
        eur_rate = exchange_rate['EUR']['sale']


        if currency == 'USD':
            converted['UAH'] = round(price * usd_rate, 2)
            converted['EUR'] = round(converted['UAH'] // eur_rate, 2)

        elif currency == 'EUR':
            converted['UAH'] = round(price * eur_rate, 2)
            converted['USD'] = round(converted['UAH'] // usd_rate)

        elif currency == 'UAH':
            converted['USD'] = round(price // usd_rate)
            converted['EUR'] = round(price // eur_rate)

        return converted
