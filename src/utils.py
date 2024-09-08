import datetime
import os

import pandas as pd
import json
import requests
import dotenv


def get_greeting_by_date(date_str: str) -> str:
    """
    Принимает строку с датой в формате YYYY-MM-DD HH:MM:SS
    Возвращает приветствие в зависимости от времени
    """
    # date_now = datetime.datetime.now()
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    if date.hour < 6:
        greeting = "Доброй ночи"
    elif date.hour < 12:
        greeting = "Доброе утро"
    elif date.hour < 18:
        greeting = "Добрый день"
    else:
        greeting = "Добрый вечер"
    return greeting


def read_excel_file(file_path: str) -> pd.DataFrame:
    """
    Считывает json-данные из файла
    Принимает путь до файла
    Возвращает дата фрейм
    """
    df = pd.read_excel(file_path)
    return df


def filter_by_date(df: pd.DataFrame, date_str: str) -> pd.DataFrame:
    """
    Фильтрует дата фрейм по дате с начала месяца по текущую дату
    Принимает датафрейм и строку с текущей датой
    Возвращает датафрейм с операциями в заданный период и с преобразованными значениям даты операции в формат datetime
    """
    date_end = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    date_start = datetime.datetime(date_end.year, date_end.month, 1, 00, 00, 00)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    filter_df = df.loc[(df["Дата операции"] >= date_start) & (df["Дата операции"] <= date_end)]
    return filter_df


####################################################################################
def get_info_by_cards(df: pd.DataFrame) -> list[dict]:
    """
    Принимает датафрейм. Возвращает список словарей с информаций по каждой карте:
    номер карты, общая сумма расходов, кешбэк
    """
    groups_cards = df.groupby("Номер карты").agg({"Сумма операции": "sum",
                                                  "Кэшбэк": "sum"})
    pass
    return groups_cards


##############################################################
def get_top_5_operations_by_summ(df: pd.DataFrame) -> dict:
    """получает из датафрейма топ 5 операций по сумме"""
    pass


def read_json_file(file_path):
    """Читает json-файл"""
    with open(file_path) as file:
        file_info = json.load(file)
    return file_info


def get_currency_rates_api(rates: list):
    """Получение курса валют"""
    dotenv.load_dotenv()
    api_key = os.getenv("API_KEY_CURRENCY")
    headers = {"apikey": api_key}
    result = []
    for rate in rates:
        source = rate
        currencies = "RUB"
        url = f"https://api.apilayer.com/currency_data/live?source={source}&currencies={currencies}"
        response = requests.get(url, headers=headers).json()
        quotes = response.get("quotes").get(f"{rate}RUB")
        dict_rete = dict()
        dict_rete["currency"] = rate
        dict_rete["rate"] = quotes
        result.append(dict_rete)
    return result


def get_stock_prices(stocks: list):
    """Получает стоимость акций"""
    dotenv.load_dotenv()
    api_key = os.getenv("API_KEY_STOCK_PRICES")
    result = []
    for stock in stocks:
        url = (f"https://www.alphavantage.co/query?"
               f"function=TIME_SERIES_DAILY&symbol={stock}&apikey={api_key}&outputsize=compact")
        response = requests.get(url)
        stock_info = response.json()
        dict_stocks = dict()
        dict_stocks["stock"] = stock
        dict_stocks["price"] = round(stock_info.get("Time Series (Daily)").get("2024-09-06").get("1. open"), 2)
        result.append(dict_stocks)
    return result


# Запрос по курсу валют
# Запрос по цене акций
# Логи
# pandas
# Вспомогательные функции, необходимые для работы функции страницы «Главная», используют библиотеку
# json
# .
# Вспомогательные функции, необходимые для работы функции страницы «Главная», используют API.
# Вспомогательные функции, необходимые для работы функции страницы «Главная», используют библиотеку
# datetime
# .
# Вспомогательные функции, необходимые для работы функции страницы «Главная», используют библиотеку
# logging
# .
# Вспомогательные функции, необходимые для работы функции страницы «Главная», используют библиотеку
# pandas
# .
