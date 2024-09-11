import json
import pandas as pd
from datetime import datetime, timedelta
import utils
import os
from config import DATA_PATH


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
    category_sum = expenses.groupby("Категория", as_index=False).agg({"Сумма операции с округлением": "sum"})
    result = pd.DataFrame({"category": category, "amount": category_sum.loc[:, "Сумма операции с округлением"]})
    return result


if __name__ == "__main__":
    df = utils.read_excel_file(os.path.join(DATA_PATH, "operations.xlsx"))
    df_expenses = utils.filter_by_expenses(df)
    print(spending_by_category(df_expenses, "ЖКХ", "2021.12.31"))


# Функция сервиса «Траты по категории» использует библиотеку
# logging
