import datetime
import json

from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from src.configs.config import settings
from src.models.calendar.event import CalendarEvent
from src.utils.logger import logger


class GoogleCalendar:
    def __init__(self):
        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            json.loads(settings.GOOGLE_CLIENT_CONFIG.get_secret_value(), strict=False)
        )
        try:
            self.service = build("calendar", "v3", credentials=creds)
        except HttpError as error:
            logger.error(f"An error occurred: {error}")

    def get_calendars(self):
        calendar_list = self.service.calendarList().list().execute()
        calendars = calendar_list.get("items", [])
        logger.debug(f"{calendars=}")  # TODO Loggers
        return calendars

    def get_events(self, calendar_id=None, max_results=10):
        now = (
            datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=1)
        ).isoformat()
        logger.info("Getting the upcoming 10 events")
        events_result = (
            self.service.events()
            .list(
                calendarId=calendar_id,
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])
        logger.debug(f"{events=}")
        return events

    def create_event(self, event: CalendarEvent):
        event_json = json.loads(event.model_dump_json(exclude_none=True))
        logger.debug(f"{event_json=}")
        event = (
            self.service.events()
            .insert(calendarId=settings.CALENDAR_ID, body=event_json)
            .execute()
        )
        return event
        # pass

    def delete_event(self, event_id: str):
        logger.info(f"Deleting event {event_id}")
        try:
            response = (
                self.service.events()
                .delete(
                    calendarId=settings.CALENDAR_ID,
                    eventId=event_id,
                )
                .execute()
            )
            logger.debug(f"{response=}")
        except HttpError as error:
            logger.error(f"Error while deleting event {event_id}: {error}")
            return None
        logger.info(f"Event {event_id} deleted")
        return response

    def update_event(self, event_id: str, body: CalendarEvent):
        logger.info(f"Updating event {event_id}")
        body_json = json.loads(body.model_dump_json(exclude_none=True, exclude="id"))
        logger.debug(f"{body_json=}")
        # try:
        response = (
            self.service.events()
            .update(calendarId=settings.CALENDAR_ID, eventId=event_id, body=body_json)
            .execute()
        )
        logger.debug(f"{response=}")
        # except HttpError as error:
        #     logger.error(f'Error while updated event {event_id}: {error}')
        #     return None
        logger.info(f"Event {event_id} updated")
        return response
