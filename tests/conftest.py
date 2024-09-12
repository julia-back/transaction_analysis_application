import pytest
import pandas as pd


@pytest.fixture
def json_response():
    return {
    "greeting": "Добрый день",
    "cards": [
        {
            "last_digits": "7197",
            "total_spent": "24576.63",
            "cashback": "245.77"
        },
        {
            "last_digits": "5091",
            "total_spent": "15193.33",
            "cashback": "151.93"
        },
        {
            "last_digits": "4556",
            "total_spent": "3775.7",
            "cashback": "37.76"
        }
    ],
    "top_transactions": [
        {
            "date": "30.12.2021",
            "amount": 174000.0,
            "category": "Пополнения",
            "description": "Пополнение через Газпромбанк"
        },
        {
            "date": "23.12.2021",
            "amount": 28001.94,
            "category": "Переводы",
            "description": "Перевод Кредитная карта. ТП 10.2 RUR"
        },
        {
            "date": "23.12.2021",
            "amount": -28001.94,
            "category": "Переводы",
            "description": "Перевод Кредитная карта. ТП 10.2 RUR"
        },
        {
            "date": "31.12.2021",
            "amount": -20000.0,
            "category": "Переводы",
            "description": "Константин Л."
        },
        {
            "date": "23.12.2021",
            "amount": 20000.0,
            "category": "Другое",
            "description": "Иван С."
        }
    ],
    "currency_rates": [
        {
            "currency": "USD",
            "rate": 91.45
        },
        {
            "currency": "EUR",
            "rate": 100.75
        }
    ],
    "stock_prices": [
        {
            "stock": "AAPL",
            "price": 222.66
        },
        {
            "stock": "AMZN",
            "price": 184.52
        },
        {
            "stock": "GOOGL",
            "price": 151.16
        },
        {
            "stock": "MSFT",
            "price": 423.04
        },
        {
            "stock": "TSLA",
            "price": 228.13
        }
    ]
}
