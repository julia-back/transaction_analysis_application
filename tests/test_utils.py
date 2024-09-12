import pytest
import requests
from src import utils
from unittest.mock import patch, Mock
import pandas as pd
import pandas


@pytest.mark.parametrize("value, expected", [(5, "Доброй ночи"), (7, "Доброе утро"),
                                             (14, "Добрый день"), (20, "Добрый вечер")])
@patch("datetime.datetime")
def test_get_greeting_by_date_night(mock_datetime, value, expected):
    mock_datetime.now.return_value.hour = value
    assert utils.get_greeting_by_date() == expected


@patch("pandas.read_excel")
def test_read_excel_file(mock_read):
    mock_read.return_value = pd.DataFrame({"1": [1, 2, 3], "2": [2, 3, 4]})
    testing_df = pd.DataFrame({"1": [1, 2, 3], "2": [2, 3, 4]})
    df_by_func = utils.read_excel_file("")
    pandas.testing.assert_frame_equal(testing_df, df_by_func)


@patch("requests.get")
def test_get_currency_rate_api(mock_get):
    mock_get.return_value.json.return_value = {'success': True,
                                               'timestamp': 1726169104,
                                               'source': 'USD',
                                               'quotes': {'USDRUB': 89.202471}}
    assert utils.get_currency_rates_api(["USD"]) == [{'currency': 'USD', 'rate': 89.2}]


@patch("requests.get")
def test_get_stock_prices(mock_get):
    mock_get.return_value.json.return_value = [{'symbol': 'AMZN', 'price': 186.92,
                                                'beta': 1.146, 'volAvg': 42978151,
                                                'mktCap': 1962047464000, 'lastDiv': 0,
                                                'range': '118.35-201.2', 'changes': 2.42,
                                                'companyName': 'Amazon.com, Inc.',
                                                'currency': 'USD', 'cik': '0001018724',
                                                'isin': 'US0231351067', 'cusip': '023135106',
                                                'exchange': 'NASDAQ Global Select',
                                                'exchangeShortName': 'NASDAQ', 'industry': 'Specialty Retail',
                                                'website': 'https://www.amazon.com',
                                                'description': 'Amazon.com, Inc. engages in the retail sale of '
                                                               'consumer products and subscriptions through online '
                                                               'and physical stores in North America and '
                                                               'internationally. The company operates through '
                                                               'three segments: North America, International, '
                                                               'and Amazon Web Services (AWS). Its products offered '
                                                               'through its stores include merchandise and content '
                                                               'purchased for resale; and products offered by '
                                                               'third-party sellers The company also manufactures '
                                                               'and sells electronic devices, including Kindle, Fire '
                                                               'tablets, Fire TVs, Rings, Blink, eero, and Echo; '
                                                               'and develops and produces media content. '
                                                               'In addition, it offers programs that enable '
                                                               'sellers to sell their products in its stores; '
                                                               'and programs that allow authors, musicians, '
                                                               'filmmakers, Twitch streamers, skill and app '
                                                               'developers, and others to publish and sell content. '
                                                               'Further, the company provides compute, storage, '
                                                               'database, analytics, machine learning, and other '
                                                               'services, as well as fulfillment, advertising, '
                                                               'and digital content subscriptions. Additionally, '
                                                               'it offers Amazon Prime, a membership program. The '
                                                               'company serves consumers, sellers, developers, '
                                                               'enterprises, content creators, and advertisers. '
                                                               'Amazon.com, Inc. was incorporated in 1994 and is '
                                                               'headquartered in Seattle, Washington.',
                                                'ceo': 'Mr. Andrew R. Jassy', 'sector': 'Consumer Cyclical',
                                                'country': 'US', 'fullTimeEmployees': '1525000',
                                                'phone': '206 266 1000', 'address': '410 Terry Avenue North',
                                                'city': 'Seattle', 'state': 'WA', 'zip': '98109-5210',
                                                'dcfDiff': 123.24349, 'dcf': 62.39651108209757,
                                                'image': 'https://financialmodelingprep.com/image-stock/AMZN.png',
                                                'ipoDate': '1997-05-15', 'defaultImage': False, 'isEtf': False,
                                                'isActivelyTrading': True, 'isAdr': False, 'isFund': False}]
    assert utils.get_stock_prices(["AMZN"]) == [{'stock': 'AMZN', 'price': 186.92}]
