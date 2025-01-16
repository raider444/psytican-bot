import pytest
from datetime import date as _date
from src.utils.convert import DateParser

current_year = _date.today().year


@pytest.mark.parametrize(
    "date,result",
    [
        ("30.11", _date(current_year, 11, 30)),
        ("3.01", _date(current_year, 1, 3)),
        ("30.11.2023", _date(2023, 11, 30)),
        ("1.3.24", _date(2024, 3, 1)),
        ("30/11", _date(current_year, 11, 30)),
        ("30/11/2023", _date(2023, 11, 30)),
        ("1/3/24", _date(2024, 3, 1)),
    ],
)
def test_date_parser_success(date, result):
    assert DateParser.parse_date(date=date) == result


@pytest.mark.parametrize(
    "date,error,result",
    [
        ("32.11", ValueError, r"day is out of range for month"),
        ("30.02", ValueError, r"day is out of range for month"),
        ("11/24", ValueError, r"month must be in 1\.\.12"),
        ("11/24/24", ValueError, r"month must be in 1\.\.12"),
        ("11/24/2024", ValueError, r"month must be in 1\.\.12"),
        ("11-11-2020", ValueError, r"Date \".*\" does not match pattern"),
    ],
)
def test_date_parser_fail(date, error, result):
    with pytest.raises(error, match=result):
        DateParser.parse_date(date=date)
