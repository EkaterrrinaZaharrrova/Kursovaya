import datetime
from typing import Any
from unittest.mock import patch

import pandas as pd
import pytest

from src.requests_api import external_request_api_currency
from src.services import simple_search
from src.views import greetings, top_transactions


@pytest.mark.parametrize(
    "test_time, test_text",
    [
        (datetime.datetime(2023, 3, 20, 7, 15, 45), "Доброе утро!"),
        (datetime.datetime(2023, 5, 24, 14, 3, 45), "Добрый день!"),
        (datetime.datetime(2023, 6, 11, 19, 22, 45), "Добрый вечер!"),
        (datetime.datetime(2023, 1, 10, 1, 31, 45), "Доброй ночи!"),
    ],
)
def test_get_greeting(test_time: str, test_text: str) -> None:
    """Тест приветствия, в зависимости от времени суток."""

    assert greetings(test_time) == test_text


def test_top_transactions(excel_data: list[dict]) -> None:
    """Тест вывода топ-5 транзакций."""

    data = top_transactions(pd.DataFrame(excel_data))
    assert data == [
        {
            "amount": 115909.42,
            "category": "Переводы",
            "date": "24.01.2018",
            "description": "Перевод Кредитная карта. ТП 10.2 RUR",
        },
        {"amount": 9700.0, "category": "Пополнения", "date": "25.01.2018", "description": "Перевод с карты"},
        {"amount": 5748.0, "category": "Авиабилеты", "date": "25.01.2018", "description": "Aviacassa"},
        {"amount": 840.3, "category": "Ж/д билеты", "date": "24.01.2018", "description": "РЖД"},
        {"amount": 376.0, "category": "Транспорт", "date": "25.01.2018", "description": "Яндекс Такси"},
    ]


@patch("requests.get")
def test_external_request_api_currency(requests_mock: Any) -> None:
    """Тест получения курса валюты по API"""
    requests_mock.return_value.status_code = 200
    requests_mock.return_value.json.return_value = {
        "USD": {"Weekly Time Series": {"2025-03-28": {"2. high": 1.887787}}}
    }
    data = external_request_api_currency()
    assert data == {"USD": 1.887787}


def test_simple_search(dict_data: list[dict]) -> None:
    """Тест простой поиск."""

    data = simple_search(dict_data, "OOO Frittella")
    assert data == (
        '[{"date of operation": "12.02.2018 12:40:34", "date of currency": '
        '"14.02.2018", "card number": "*7197", "status": "OK", "operation": {"add": '
        '-314.0, "currency": "RUB"}, "add": -314.0, "currency": "RUB", "cashback": '
        '50.0, "category": "Фастфуд", "description": "OOO Frittella", "Investment '
        'bank": 0, "add with round": 314.0}]'
    )
