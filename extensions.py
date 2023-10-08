import requests
import json
from config import keys

class ConvertionException(Exception):
    pass

class ConvertValues:
    @staticmethod
    def get_price(quote, base, amount):
        if quote == base:
            raise ConvertionException(f'Нельзя переводить в одну и ту же валюту {quote}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Валюта {quote} недоступна')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Валюта {base} недоступна')

        try:
            amount = int(amount)
        except ValueError:
            raise ConvertionException(f'Неверное количество "{amount}"')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        return total_base
