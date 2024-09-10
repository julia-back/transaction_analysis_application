import datetime
import json
import os

import dotenv
import pandas as pd
import requests


def get_greeting_by_date() -> str:
    """
    Возвращает приветствие в зависимости от текущего времени.
    """
    date_now = datetime.datetime.now()
    if date_now.hour < 6:
        greeting = "Доброй ночи"
    elif date_now.hour < 12:
        greeting = "Доброе утро"
    elif date_now.hour < 18:
        greeting = "Добрый день"
    else:
        greeting = "Добрый вечер"
    return greeting


def read_excel_file(file_path: str) -> pd.DataFrame:
    """
    Считывает json-данные из файла. Принимает путь до файла. Возвращает дата фрейм.
    """
    df = pd.read_excel(file_path)
    return df


def filter_by_date(df: pd.DataFrame, date_str: str) -> pd.DataFrame:
    """
    Принимает датафрейм и строку с датой для фильтрации
    Фильтрует дата фрейм по дате с начала месяца по текущую дату
    Возвращает датафрейм с операциями в заданный период и с преобразованными значениям даты операции в формат datetime
    """
    date_end = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    date_start = datetime.datetime(date_end.year, date_end.month, 1, 00, 00, 00)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    filter_df = df.loc[(df["Дата операции"] >= date_start) & (df["Дата операции"] <= date_end)]
    return filter_df


def filter_by_expenses(df: pd.DataFrame) -> pd.DataFrame:
    """
    Принимает датафрейм. Возвращает датафрейм с расходами (отрицательными суммами операций).
    """
    filter_df = df.loc[df["Сумма операции"] < 0]
    return filter_df


def get_info_by_cards(df: pd.DataFrame) -> list[dict]:
    """
    Принимает датафрейм. Возвращает список словарей с информаций по каждой карте:
    номер карты, общая сумма расходов, кешбэк
    """
    cards_list = df["Номер карты"].unique().tolist()
    cards_list = [x for x in cards_list if str(x) != "nan"]
    sum_operations_by_cards = df.groupby("Номер карты").agg({"Сумма операции": "sum"}).to_dict()
    result = []
    for card in cards_list:
        cards_sum_cashback = dict()
        cards_sum_cashback["last_digits"] = card.replace("*", "")
        cards_sum_cashback["total_spent"] = ((str(round(sum_operations_by_cards.get("Сумма операции")
                                                        .get(card), 2))).replace("-", ""))
        cards_sum_cashback["cashback"] = ((str(round(sum_operations_by_cards.get("Сумма операции")
                                                     .get(card) / 100, 2))).replace("-", ""))
        result.append(cards_sum_cashback)
    return result


def get_top_5_operations_by_summ(df: pd.DataFrame) -> list[dict]:
    """Получает из датафрейма топ 5 операций по сумме"""
    sort_df = df.sort_values("Сумма операции с округлением", ascending=False)
    top_5_df = sort_df.head(5)
    result = []
    for index, row in top_5_df.iterrows():
        dict_for_row = dict()
        dict_for_row["date"] = row["Дата платежа"]
        dict_for_row["amount"] = round(float(row["Сумма операции"]), 2)
        dict_for_row["category"] = row["Категория"]
        dict_for_row["description"] = row["Описание"]
        result.append(dict_for_row)
    return result


def read_json_file(file_path: str) -> dict:
    """Читает json-файл"""
    with open(file_path) as file:
        file_info = json.load(file)
    return file_info


def get_currency_rates_api(rates: list) -> list[dict]:
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
        dict_rete["rate"] = round(float(quotes), 2)
        result.append(dict_rete)
    return result


def get_stock_prices(stocks: list) -> list[dict]:
    """Получает стоимость акций"""
    dotenv.load_dotenv()
    api_key = os.getenv("API_KEY_STOCK_PRICES")
    result = []
    for stock in stocks:
        url = f"https://financialmodelingprep.com/api/v3/profile/{stock}?apikey={api_key}"
        response = requests.get(url).json()
        dict_stocks = dict()
        dict_stocks["stock"] = stock
        dict_stocks["price"] = round(float(response[0].get("price")), 2)
        result.append(dict_stocks)
    return result


# Логи
# Вспомогательные функции, необходимые для работы функции страницы «Главная», используют библиотеку
# logging
