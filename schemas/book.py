from typing import Text

from pydantic import BaseModel


class BookDelete(BaseModel):
    id: int


class BookCreate(BaseModel):
    name: str
    description: Text | None = None
    file_path: str


class BookUpdate(BookDelete):
    name: str | None = None
    description: Text | None = None
    file_path: str | None = None


class BookResponse(BookCreate):
    id: int

    class Config:
        from_attributes = True
