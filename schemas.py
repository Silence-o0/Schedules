import datetime

from pydantic import BaseModel


class FieldOfStudy(BaseModel):
    id: int
    short_title: str
    title: str
    created_at: datetime.datetime
