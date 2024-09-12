from src import views
from tests.conftest import json_response, df
from unittest.mock import patch, Mock
import pandas as pd


# def test_home_page(json_response, df):
#     mock_greeting = Mock(return_value="Добрый день")
#     views.utils.get_greeting_by_date = mock_greeting
#     #mock_read_file = Mock(return_value=df)
#     assert views.home_page("", "2021-12-31 16:44:00") == json_response
