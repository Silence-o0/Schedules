from pydantic import BaseModel


class Lesson(BaseModel):
    id: int
    title: str
