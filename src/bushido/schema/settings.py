from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field

from bushido.settings import DAY_START_HOUR, TIMEZONE, Category


class TimeZone(BaseModel):
    timezone: ZoneInfo = Field(default=TIMEZONE)


class DayStart(BaseModel):
    hour: int = Field(default=DAY_START_HOUR)


class LogSpec(BaseModel):
    category: Category
    name: str
    emoji: bytes
