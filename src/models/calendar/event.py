from datetime import datetime, date as _date
from typing import Optional
from typing_extensions import Self
from pydantic import Field, field_validator, model_validator
from src.models.base_schema import BaseEventModel
from src.models.calendar.event_meta import CalendarEventMetadata


class CalendarDateTime(BaseEventModel):
    date: Optional[_date] = None
    date_time: Optional[datetime] = Field(
        None,
        alias="dateTime",
    )
    time_zone: Optional[str] = None

    @model_validator(mode="after")
    def disallow_both_date_and_date_time(self):
        date = self.date
        date_time = self.date_time
        if date is not None and date_time is not None:
            raise ValueError('"date" and "dateTime" can\'t be defined simultaneously')
        return self


class CalendarEvent(BaseEventModel):
    id: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str | CalendarEventMetadata] = None
    start: Optional[CalendarDateTime]
    end: Optional[CalendarDateTime]
    html_link: Optional[str] = None

    @field_validator("description")
    def empty_str_to_none(cls, description):
        if description == "":
            return None
        return description

    @model_validator(mode="after")
    def model_validator(self) -> Self:
        start_date: _date = self.start.date
        end_date: _date = self.end.date
        if end_date is not None and end_date < start_date:
            raise ValueError("End date must be greater than start date")
        if self.end.date_time is not None and self.end.date_time < self.start.date_time:
            raise ValueError("End time must be greater than start time")
        return self
