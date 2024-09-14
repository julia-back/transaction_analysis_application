import json
import logging
import os
from datetime import datetime, timedelta
from functools import wraps

import pandas as pd

from config import DATA_PATH, LOGS_PATH

logging.basicConfig(
    level=logging.DEBUG,
    filename=os.path.join(LOGS_PATH, "logs.log"),
    filemode="a",
    format="%(asctime)s %(levelname)s: %(name)s - %(message)s",
)
logger = logging.getLogger(f"{__name__}.py")


def write_to_json_file(file_path: str = os.path.join(DATA_PATH, "report.json")):
    """Записывает результат функции в json-файл, принимает пусть до файла опционально"""

    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            logger.info("Start decorator")
            result = func(*args, **kwargs)
            if type(result) is pd.DataFrame:
                result.to_json(path_or_buf=file_path, orient="records", indent=4, force_ascii=False)
            elif type(result) is json:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(result)
            else:
                logger.error("Type data is not supported")
            logger.info("Successful finish decorator")
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
    logger.info("Start func")
    if type(date) is str:
        date = datetime.strptime(date, "%Y.%m.%d").replace(hour=23, minute=59, second=59)
    date_start = date - timedelta(days=90)
    expenses.loc[:, "Дата операции"] = pd.to_datetime(expenses["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    expenses = expenses[(expenses["Дата операции"] >= date_start) & (expenses["Дата операции"] <= date)]
    expenses = expenses[expenses["Категория"] == category]
    # category_sum = expenses.groupby("Категория", as_index=False).agg({"Сумма операции с округлением": "sum"})
    # result = pd.DataFrame({"category": category, "expenses": category_sum.loc[:, "Сумма операции с округлением"]})
    logger.info("Successful finish func")
    return expenses
