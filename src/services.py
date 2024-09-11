import json
from datetime import datetime
import logging
import os
from config import LOGS_PATH


logger = logging.getLogger(f"{__name__}.py")
handler = logging.FileHandler(os.path.join(LOGS_PATH, "logs.txt"), mode="a")
formatter = logging.Formatter("%(asctime)s %(levelname)s: %(name)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def cashback_categories(data: list[dict], year: str | int, month: str | int) -> json:
    """
    Считает размер кешбэка для каждой категории
    Принимает данные с транзакциями в формате списка словарей, год, месяц для расчета.
    Возвращает json-ответ со словарем категорий и размером кешбэка
    """
    logger.info("Start")
    data_by_date = []
    if year in range(1999, datetime.now().year):
        for operation in data:
            date = datetime.strptime(operation.get("Дата операции"), "%d.%m.%Y %H:%M:%S")
            if date.year == year and date.month == month:
                data_by_date.append(operation)
    else:
        logger.warning(f"Year is not in period 1999-{datetime.now().year}. Received all transactions")
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
    logger.info("Successful finish")
    return result
