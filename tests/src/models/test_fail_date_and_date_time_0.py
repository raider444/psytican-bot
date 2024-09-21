import pytest
from pydantic_core import ValidationError
from src.telegram.tg_wrapper import event_list


def test_event_list():
    calendar_data = [
        {
            "kind": "calendar#event",
            "etag": '"3452471884512000"',
            "id": "mb1hpc45cksed2fhsuuq85shfc",
            "status": "confirmed",
            "htmlLink": "https://some-link.example.com/foo/bar",
            "created": "2024-09-13T13:59:02.000Z",
            "updated": "2024-09-13T13:59:02.256Z",
            "summary": "sdfgsdfgsfd",
            "description": '{"version":1,"owner":{"first_name":"John","id":000000,"is_bot":false,"is_premium":true,"language_code":"en","last_name":"Smith","username":"username"}}',  # noqa: E501
            "creator": {
                "email": "psytican-bot-sa@psynet-418607.iam.gserviceaccount.com"
            },
            "organizer": {
                "email": "2a587912e793ca40431cdd93c5d30f0b220f5d30de58d1eb11a6473cf2f30aa8@group.calendar.google.com",
                "displayName": "TEST",
                "self": True,
            },
            "start": {"date": "2024-09-15", "dateTime": "2024-09-15 21:00:03"},
            "end": {"date": "2024-09-14"},
            "iCalUID": "mb1hpc45cksed2fhsuuq85shfc@google.com",
            "sequence": 0,
            "reminders": {"useDefault": False},
            "eventType": "default",
        },
    ]

    with pytest.raises(ValidationError, match=r"\"date\"\ and\ \"dateTime\""):
        event_list(events=calendar_data)
