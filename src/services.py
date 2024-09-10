import json
import os
from datetime import datetime

import utils
from config import DATA_PATH


def get_list_transactions(file_path: str) -> list[dict]:
    df = utils.read_excel_file(file_path)
    list_data = df.to_dict(orient="records")
    return list_data


def cashback_categories(data: list[dict], year: str | int, month: str | int) -> json:
    """
    Считает размер кешбэка для каждой категории
    Принимает данные с транзакциями в формате списка словарей, год, месяц для расчета.
    Возвращает json-ответ со словарем категорий и размером кешбэка
    """
    data_by_date = []
    if year in range(1999, datetime.now().year):
        for operation in data:
            date = datetime.strptime(operation.get("Дата операции"), "%d.%m.%Y %H:%M:%S")
            if date.year == year and date.month == month:
                data_by_date.append(operation)
    categories = set()
    for operation in data_by_date:
        if operation.get("Категория").lower() not in ["пополнения", "переводы", "другое"]:
            categories.add(operation.get("Категория"))
    total_dict = dict()
    for category in categories:
        cashback_category = 0
        for operation in data_by_date:
            if operation.get("Категория") == category:
                cashback_category += float(operation.get("Сумма операции с округлением")) / 100
        total_dict[category] = round(cashback_category)
    sort_list = sorted(total_dict.items(), key=lambda x: x[1], reverse=True)
    sort_dict = dict(sort_list)
    result = json.dumps(sort_dict, indent=4, ensure_ascii=False)
    return result


if __name__ == "__main__":
    operations_list = get_list_transactions(os.path.join(DATA_PATH, "operations.xlsx"))
    print(cashback_categories(operations_list, 2021, 12))


# Функция сервиса «Выгодные категории повышенного кешбэка» использует библиотеку
# logging
