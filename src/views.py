import json
import os

from config import PATH
from src import utils


def home_page(file_path, date_str: str) -> json:
    """
    Принимает строку с датой в формате YYYY-MM-DD HH:MM:SS
    Возвращает JSON-ответ
    """
    greeting = str(utils.get_greeting_by_date())
    total_df = utils.read_excel_file(file_path)
    filter_df_by_date = utils.filter_by_date(total_df, date_str)
    df_expenses = utils.filter_by_expenses(filter_df_by_date)
    info_by_cards = utils.get_info_by_cards(df_expenses)
    top_5 = utils.get_top_5_operations_by_summ(filter_df_by_date)
    user_settings = utils.read_json_file(os.path.join(PATH, "user_settings.json"))
    currency_rates = utils.get_currency_rates_api(user_settings.get("user_currencies"))
    stock_prices = utils.get_stock_prices(user_settings.get("user_stocks"))
    total_dict = dict()
    total_dict["greeting"] = greeting
    total_dict["cards"] = info_by_cards
    total_dict["top_transactions"] = top_5
    total_dict["currency_rates"] = currency_rates
    total_dict["stock_prices"] = stock_prices
    json_response = json.dumps(total_dict, ensure_ascii=False, indent=4)
    return json_response
