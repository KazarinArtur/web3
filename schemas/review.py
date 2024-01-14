from typing import Text

from pydantic import BaseModel


class ReviewDelete(BaseModel):
    id: int


class ReviewCreate(BaseModel):
    content: Text
    user_id: int
    book_id: int


class ReviewUpdate(ReviewDelete):
    content: Text | None = None
    user_id: int | None = None
    book_id: int | None = None


class ReviewResponse(ReviewCreate):
    class Config:
        from_attributes = True
