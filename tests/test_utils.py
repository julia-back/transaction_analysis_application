from src import utils
from unittest.mock import patch, Mock
from datetime import datetime
import pandas as pd
import requests


# def test_get_greeting_by_date_night():
#     with patch("datetime.now") as mock_now:
#         mock_now.return_value.hour.return_value = 5
#         assert utils.get_greeting_by_date() == "Доброй ночи"
#
#
# # def test_get_greeting_by_date_morning():
#     patch("datetime.datetime.now.hour", return_value=8)
#     assert utils.get_greeting_by_date() == "Доброе утро"
#
#
# def test_get_greeting_by_date_day():
#     patch("datetime.datetime.now.hour", return_value=14)
#     utils.get_greeting_by_date() == "Добрый день"
#
#
# def test_get_greeting_by_date():
#     patch("datetime.datetime.now.hour", return_value=19)
#     utils.get_greeting_by_date() == "Добрый вечер"


# @patch("pd.read_excel")
# def test_excel_file(mock_read):
#     mock_read.return_value = pd.DataFrame({"1": [1, 2, 3], "2": [2, 3, 4]})
#     assert utils.read_excel_file("") == pd.DataFrame({"1": [1, 2, 3], "2": [2, 3, 4]})


# @patch("requests.get")
# def test_get_currency_rates_api(mock_get):
#     mock_get.return_value.
#
#
#
#
