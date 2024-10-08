import datetime
from unittest.mock import patch

import pandas as pd
import pytest

from src import utils


@pytest.mark.parametrize(
    "value, expected", [(5, "Доброй ночи"), (7, "Доброе утро"), (14, "Добрый день"), (20, "Добрый вечер")]
)
@patch("datetime.datetime")
def test_get_greeting_by_date_night(mock_datetime, value, expected):
    mock_datetime.now.return_value.hour = value
    assert utils.get_greeting_by_date() == expected


@patch("pandas.read_excel")
def test_read_excel_file(mock_read):
    mock_read.return_value = pd.DataFrame({"1": [1, 2, 3], "2": [2, 3, 4]})
    testing_df = pd.DataFrame({"1": [1, 2, 3], "2": [2, 3, 4]})
    df_by_func = utils.read_excel_file("")
    pd.testing.assert_frame_equal(testing_df, df_by_func)


def test_filter_by_date(df):
    df_func = utils.filter_by_date(df, "2021-12-31 17:00:00")
    df_expected = pd.DataFrame(
        {
            "Дата операции": [
                datetime.datetime(2021, 12, 31, 16, 44, 00),
                datetime.datetime(2021, 12, 27, 15, 56, 23),
            ],
            "Статус": ["OK", "OK"],
            "Сумма операции": [-372.00, -569.94],
        }
    )
    pd.testing.assert_frame_equal(df_func, df_expected)


def test_filter_by_expenses(df):
    df_func = utils.filter_by_expenses(df)
    df_expected = pd.DataFrame(
        {
            "Дата операции": ["31.12.2021 16:44:00", "27.12.2021 15:56:23", "11.11.2021 15:25:03"],
            "Статус": ["OK", "OK", "OK"],
            "Сумма операции": [-372.00, -569.94, -224.00],
        }
    )
    pd.testing.assert_frame_equal(df_func, df_expected)


def test_get_info_by_cards(df_cards):
    assert utils.get_info_by_cards(df_cards) == [
        {"last_digits": "7197", "total_spent": "8854.0", "cashback": "88.54"},
        {"last_digits": "4556", "total_spent": "227.43", "cashback": "2.27"},
    ]


def test_get_top_5_operations_by_summ(df_top_5):
    assert utils.get_top_5_operations_by_summ(df_top_5) == [
        {"date": "21.09.2021", "amount": -8798.0, "category": "ЖКХ", "description": "ЖКУ Квартира"},
        {"date": "28.09.2021", "amount": 4000.0, "category": "Переводы", "description": "Дмитрий Р."},
        {"date": "24.09.2021", "amount": -110.0, "category": "Аптеки", "description": "Аптека Вита"},
        {"date": "30.12.2021 17:50:17", "amount": 2.96, "category": "Бонусы", "description": "Проценты на остаток"},
    ]


@patch("builtins.open")
@patch("json.load")
def test_read_json_file(mock_load, mock_open):
    mock_load.return_value = {1: 2}
    assert utils.read_json_file("") == {1: 2}


@patch("requests.get")
def test_get_currency_rate_api(mock_get):
    mock_get.return_value.json.return_value = {
        "success": True,
        "timestamp": 1726169104,
        "source": "USD",
        "quotes": {"USDRUB": 89.202471},
    }
    assert utils.get_currency_rates_api(["USD"]) == [{"currency": "USD", "rate": 89.2}]


@patch("requests.get")
def test_get_stock_prices(mock_get):
    mock_get.return_value.json.return_value = [{"symbol": "AMZN", "price": 186.92,}]
    assert utils.get_stock_prices(["AMZN"]) == [{"stock": "AMZN", "price": 186.92}]


@patch("src.utils.read_excel_file")
def test_get_list_expenses(mock_read, df_cards):
    mock_read.return_value = df_cards
    assert utils.get_list_expenses("") == [
        {"Номер карты": "*7197", "Сумма операции": -8798.0},
        {"Номер карты": "*7197", "Сумма операции": -56.0},
        {"Номер карты": "*4556", "Сумма операции": -138.0},
        {"Номер карты": "*4556", "Сумма операции": -89.43},
    ]
