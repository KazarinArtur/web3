from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_database
from db.actions import current_user, create_review, delete_this_review_by_id
from schemas.review import ReviewCreate, ReviewResponse
from schemas.user import UserResponse

router = APIRouter(
    prefix="/review",
    tags=["Reviews"]
)


@router.post("/create")
async def write_review(review: ReviewCreate, user: UserResponse = Depends(current_user),
                       db: Session = Depends(get_database)) -> ReviewResponse:
    if user.id != review.user_id:
        raise HTTPException(status_code=401, detail="Invalid user id")

    review = await create_review(review.content, review.user_id, review.book_id, db)
    return ReviewResponse.model_validate(review)


@router.delete("/delete/{review_id}")
async def delete_review_by_id(review_id: int, db: Session = Depends(get_database),
                              user: UserResponse = Depends(current_user)) -> ReviewResponse:
    review = await delete_this_review_by_id(review_id, db)
    return ReviewResponse.model_validate(review)
