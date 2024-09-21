from src.telegram.tg_calendar import create_callback_data


def test_cerate_callback_data():
    data = {"action": "DAY", "year": 2020, "month": 9, "day": 19}
    result = "CALENDAR;DAY;2020;9;19"
    assert (
        create_callback_data(data["action"], data["year"], data["month"], data["day"])
        == result
    )

    data = {"action": "DFGDF", "year": 2020, "month": 9, "day": 19}
    result = "CALENDAR;DFGDF;2020;9;19"
    assert (
        create_callback_data(data["action"], data["year"], data["month"], data["day"])
        == result
    )
