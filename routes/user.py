from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_database
from db.actions import create_user, current_user, user_by_id, user_by_name, delete_this_user_by_id, \
    update_this_user_by_id
from schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)


@router.post("/create")
async def register_user(user: UserCreate, db: Session = Depends(get_database)) -> UserResponse:
    user = await create_user(user.name, user.email, user.password, user.role, db)
    return UserResponse.model_validate(user)


@router.get("/me")
async def get_current_user(user: UserResponse = Depends(current_user)) -> UserResponse:
    return UserResponse.model_validate(user)


@router.get("/id/{user_id}")
async def get_user_by_id(user_id: int, db: Session = Depends(get_database),
                         user: UserResponse = Depends(current_user)) -> UserResponse:
    user = await user_by_id(user_id, db)
    return UserResponse.model_validate(user)


@router.get("/name/{user_name}")
async def get_user_by_name(user_name: str, db: Session = Depends(get_database),
                           user: UserResponse = Depends(current_user)) -> UserResponse:
    user = await user_by_name(user_name, db)
    return UserResponse.model_validate(user)


@router.delete("/delete/{user_id}")
async def delete_user_by_id(user_id: int, db: Session = Depends(get_database),
                            user: UserResponse = Depends(current_user)) -> UserResponse:
    user = await delete_this_user_by_id(user_id, db)
    return UserResponse.model_validate(user)


@router.patch("/update")
async def update_user_by_id(user_info: UserUpdate, db: Session = Depends(get_database),
                            user: UserResponse = Depends(current_user)) -> UserResponse:
    user_info = await update_this_user_by_id(user_info, db)
    return UserResponse.model_validate(user_info)
