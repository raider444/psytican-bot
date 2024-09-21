import datetime
from src.models.calendar.event import (
    CalendarEvent,
    CalendarDateTime,
    CalendarEventMetadata,
)

calendar_data = [
    {
        "kind": "calendar#event",
        "etag": '"3452471884512000"',
        "id": "mb1hpc45cksed2fhsuuq85shfc",
        "status": "confirmed",
        "htmlLink": "https://www.google.com/calendar/event?eid=bWIxaHBjNDVja3NlZDJmaHN1dXE4NXNoZmMgMmE1ODc5MTJlNzkzY2E0MDQzMWNkZDkzYzVkMzBmMGIyMjBmNWQzMGRlNThkMWViMTFhNjQ3M2NmMmYzMGFhOEBn",
        "created": "2024-09-13T13:59:02.000Z",
        "updated": "2024-09-13T13:59:02.256Z",
        "summary": "кпевыапывп",
        "description": '{"version":1,"owner":{"first_name":"Igor","id":198742277,"is_bot":false,"is_premium":true,"language_code":"en","last_name":"Shatunov","username":"raider444"}}',
        "creator": {"email": "psytican-bot-sa@psynet-418607.iam.gserviceaccount.com"},
        "organizer": {
            "email": "2a587912e793ca40431cdd93c5d30f0b220f5d30de58d1eb11a6473cf2f30aa8@group.calendar.google.com",
            "displayName": "TEST",
            "self": True,
        },
        "start": {"date": "2024-09-15"},
        "end": {"date": "2024-09-15"},
        "iCalUID": "mb1hpc45cksed2fhsuuq85shfc@google.com",
        "sequence": 0,
        "reminders": {"useDefault": False},
        "eventType": "default",
    },
    {
        "kind": "calendar#event",
        "etag": '"3451275443510000"',
        "id": "tkqu7pfh7q4vo8nnpqp5v0435c",
        "status": "confirmed",
        "htmlLink": "https://www.google.com/calendar/event?eid=dGtxdTdwZmg3cTR2bzhubnBxcDV2MDQzNWMgMmE1ODc5MTJlNzkzY2E0MDQzMWNkZDkzYzVkMzBmMGIyMjBmNWQzMGRlNThkMWViMTFhNjQ3M2NmMmYzMGFhOEBn",
        "created": "2024-09-06T15:48:41.000Z",
        "updated": "2024-09-06T15:48:41.755Z",
        "summary": "Test book",
        "creator": {"email": "psytican-bot-sa@psynet-418607.iam.gserviceaccount.com"},
        "organizer": {
            "email": "2a587912e793ca40431cdd93c5d30f0b220f5d30de58d1eb11a6473cf2f30aa8@group.calendar.google.com",
            "displayName": "TEST",
            "self": True,
        },
        "start": {"date": "2024-09-21"},
        "end": {"date": "2024-09-21"},
        "iCalUID": "tkqu7pfh7q4vo8nnpqp5v0435c@google.com",
        "sequence": 0,
        "reminders": {"useDefault": False},
        "eventType": "default",
    },
]

result_data = [
    CalendarEvent(
        id="mb1hpc45cksed2fhsuuq85shfc",
        summary="кпевыапывп",
        description=CalendarEventMetadata(
            version=1,
            owner={
                "first_name": "Igor",
                "id": 198742277,
                "is_bot": False,
                "is_premium": True,
                "language_code": "en",
                "last_name": "Shatunov",
                "username": "raider444",
            },
        ),
        start=CalendarDateTime(
            date=datetime.date(2024, 9, 15), date_time=None, time_zone=None
        ),
        end=CalendarDateTime(
            date=datetime.date(2024, 9, 15), date_time=None, time_zone=None
        ),
        html_link="https://www.google.com/calendar/event?eid=bWIxaHBjNDVja3NlZDJmaHN1dXE4NXNoZmMgMmE1ODc5MTJlNzkzY2E0MDQzMWNkZDkzYzVkMzBmMGIyMjBmNWQzMGRlNThkMWViMTFhNjQ3M2NmMmYzMGFhOEBn",
    ),
    CalendarEvent(
        id="tkqu7pfh7q4vo8nnpqp5v0435c",
        summary="Test book",
        description=None,
        start=CalendarDateTime(
            date=datetime.date(2024, 9, 21), date_time=None, time_zone=None
        ),
        end=CalendarDateTime(
            date=datetime.date(2024, 9, 21), date_time=None, time_zone=None
        ),
        html_link="https://www.google.com/calendar/event?eid=dGtxdTdwZmg3cTR2bzhubnBxcDV2MDQzNWMgMmE1ODc5MTJlNzkzY2E0MDQzMWNkZDkzYzVkMzBmMGIyMjBmNWQzMGRlNThkMWViMTFhNjQ3M2NmMmYzMGFhOEBn",
    ),
]

# flake8: noqa E501
