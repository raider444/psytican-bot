from src.models.base_schema import BaseEventModel


class CalendarEventMetadata(BaseEventModel):
    version: int = 1
    owner: dict
