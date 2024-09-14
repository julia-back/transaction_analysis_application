import os

import utils
from config import DATA_PATH
from reports import spending_by_category
from services import cashback_categories
from views import home_page


def main():
    """Основная функция вызова"""
    # При необходимости прочитать другой файл, поместите свой Excel-файл в директорию data
    # и измените название файла ниже
    # Чтобы изменить список для вывода курса валют и цен акций, измените коды валют и акций
    # в файле user_settings.json
    file = os.path.join(DATA_PATH, "operations.xlsx")
    # Вывод главной страницы с приветствием, сводной информацией о картах, топ-5 транзакций,
    # курсов валют и стоимостью акций, при необходимости измените дату для изменения
    # периода анализа транзакций
    print(home_page(file, "2021-12-31 16:44:00"))

    # При необходимости прочитать другой файл, поместите свой Excel-файл в директорию data
    # и измените название файла ниже
    operations_list = utils.get_list_expenses(os.path.join(DATA_PATH, "operations.xlsx"))
    # Вывод категорий с общей величиной расходов для выбора наиболее выгодной категории
    # кешбэка, при необходимости измените год (YYYY) и месяц (MM) для анализа
    print(cashback_categories(operations_list, 2021, 12))

    # При необходимости прочитать другой файл, поместите свой Excel-файл в директорию data
    # и измените название файла ниже
    df = utils.read_excel_file(os.path.join(DATA_PATH, "operations.xlsx"))
    df_expenses = utils.filter_by_expenses(df)
    # Вывод транзакций по выбранной категории за последние 90 дней от выбранной даты или
    # текущей даты по умолчанию (в формате pd.DataFrame)
    # При необходимости введите другую категорию в точности так, как она указана в
    # вашем файле
    # Опционально введите дату (по умолчанию период будет считаться с текущей даты)
    # Отчет в json-формате по умолчанию будет записан в файл report.json в директории data
    # При необходимости записи данных в другой файл, передайте путь до файла в декоратор
    # в модуле reports.py
    print(spending_by_category(df_expenses, "ЖКХ", date="2021.12.31"))


if __name__ == "__main__":
    main()
