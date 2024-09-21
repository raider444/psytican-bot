import pytest
from datetime import date as _date
from src.telegram.utils import separate_callback_data, format_calndar_date


def test_separate_callback_data():
    data = "dsfsd;sdfdsf;sdgdsgdsf"
    result = ["dsfsd", "sdfdsf", "sdgdsgdsf"]
    assert separate_callback_data(data) == result


def test_format_calendar_data():
    date = "24/12/2020"
    result = _date(2020, 12, 24)
    assert format_calndar_date(date) == result

    date = "24/23/2020"
    date1 = "24-03-2020"
    with pytest.raises(ValueError, match=r"does\ not\ match\ format"):
        format_calndar_date(date)
        format_calndar_date(date1)
