from functools import wraps

import pandas as pd
from datetime import datetime, timedelta
import os
from config import DATA_PATH


def write_to_json_file(file_path: str = os.path.join(DATA_PATH, "report.json")):
    """Записывает результат функции в json-файл, принимает пусть до файла опционально"""
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            if type(result) is pd.DataFrame:
                result_json = result.to_json(orient="records", indent=4, force_ascii=False)
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(result_json, )
            return result
        return inner
    return wrapper


@write_to_json_file()
def spending_by_category(expenses: pd.DataFrame, category: str, date: str = datetime.now()) -> pd.DataFrame:
    """
    Считает траты по категориям за последние 3 месяца
    Принимает датафрейм с транзакциями, название категории и опционально дату в формате YYYY.MM.DD
    Если дата не передана, то берется текущая дата
    """
    if type(date) is str:
        date = datetime.strptime(date, "%Y.%m.%d")
    date_start = date - timedelta(days=90)
    expenses.loc[:, "Дата операции"] = pd.to_datetime(expenses["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    expenses = expenses[(expenses["Дата операции"] >= date_start) & (expenses["Дата операции"] <= date)]
    expenses = expenses[expenses["Категория"] == category]
    # category_sum = expenses.groupby("Категория", as_index=False).agg({"Сумма операции с округлением": "sum"})
    # result = pd.DataFrame({"category": category, "expenses": category_sum.loc[:, "Сумма операции с округлением"]})
    return expenses


# Функция сервиса «Траты по категории» использует библиотеку
# logging
