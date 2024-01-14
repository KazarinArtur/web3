from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db import get_database
from db.actions import create_token, authenticate_user

router = APIRouter(
    prefix="/auth",
    tags=["Authorization"]
)


@router.post("/token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends(),
                         db: Session = Depends(get_database)):
    user = await authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return await create_token(user)
