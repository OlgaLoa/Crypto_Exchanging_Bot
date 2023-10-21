import json  # импортируем модуль для работы с JSON
import requests  # импортируем модуль для работы с HTTP-запросами
from config import keys  # импортируем из файла config.py словарь с кодами валют

class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote:str, base:str, amount:str):

        if quote == base:
            raise APIException(f"невозможно перевести одинаковую валюту {base}.")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f"не удалось обработать валюту: {quote}")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f"не удалось обработать валюту: {base}")

        # если введено не число
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"не удалось обработать количество: {amount}")

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
        total_base = (json.loads(r.content)[keys[base]]) * float(amount)
        return total_base
