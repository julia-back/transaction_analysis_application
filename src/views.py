import json
from src import utils
from config import PATH, DATA_PATH
import os


def home_page(date_str: str) -> json:
    """
    Принимает строку с датой в формате YYYY-MM-DD HH:MM:SS
    Возвращает JSON-ответ
    """
    greeting = utils.get_greeting_by_date(date_str)

    df = utils.read_excel_file(os.path.join(DATA_PATH, "operations.xlsx"))
    filter_df = utils.filter_by_date(df, date_str)
    info_by_cards = utils.get_info_by_cards(filter_df)
    top_5 = utils.get_top_5_operations_by_summ(filter_df)

    user_settings = utils.read_json_file(os.path.join(PATH, "user_settings.json"))
    #currency_rates = utils.get_currency_rates_api(user_settings.get("user_currencies"))
    #stock_prices = utils.get_stock_prices(user_settings.get("user_stocks"))
    return stock_prices


print(home_page("2021-12-31 16:44:00"))
