import os
import sys

sys.path.append('../')

from typing import Text, Optional

from sqlalchemy.orm import Session

from config import Config
from db import get_database

from fastapi import HTTPException, Depends
import fastapi.security as security

import passlib.hash as _hash
import jwt

from db.models import User, Review, Book


async def authenticate_user(username: str, password: str, db: Session):
    user = await user_by_name(user_name=username, db=db)

    if user is None:
        return False

    if not user.verify_password(password):
        return False

    return user


async def create_token(user: User):
    token = jwt.encode(dict(id=user.id, name=user.name, email=user.email, password=user.password), Config.secret,
                       algorithm="HS256")
    return {
        "access_token": token,
        "token_type": "Bearer",
        "user_id": user.id
    }


async def create_user(name: str, email: str, password: str, role: bool, db: Session):
    user_model = User(
        name=name,
        email=email,
        password=_hash.bcrypt.hash(password),
        role=role
    )

    db.add(user_model)
    db.commit()
    db.refresh(user_model)

    return user_model


oauth2schema = security.OAuth2PasswordBearer(tokenUrl="/auth/token")


async def current_user(token: str = Depends(oauth2schema), db: Session = Depends(get_database)):
    try:
        payload = jwt.decode(token, Config.secret, algorithms="HS256")
        user = db.query(User).get(payload["id"])
    except:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return user


async def user_by_id(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        db.close()
        raise HTTPException(status_code=404, detail=f"User with id = {user_id} not found")

    return user


async def user_by_name(user_name: str, db: Session):
    user = db.query(User).filter(User.name == user_name).first()
    return user


async def delete_this_user_by_id(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        db.close()
        raise HTTPException(status_code=404, detail=f"User with id = {user_id} not found")

    db.delete(user)
    db.commit()

    return user


async def update_this_user_by_id(user: User, db: Session):
    old_user = db.query(User).filter(User.id == user.id).first()

    if old_user is None:
        db.close()
        raise HTTPException(status_code=404, detail=f"User with id = {user.id} not found")

    if user.password:
        user.password = _hash.bcrypt.hash(user.password)

    db.query(User).filter(User.id == user.id).update(user.model_dump(exclude_unset=True))
    db.commit()

    return old_user


async def create_book(name: str, description: Text, file_path: str, db: Session):
    book_model = Book(
        name=name,
        description=description,
        file_path=file_path
    )

    db.add(book_model)
    db.commit()
    db.refresh(book_model)

    return book_model


async def book_by_id(book_id: int, db: Session):
    book = db.query(Book).filter(Book.id == book_id).first()

    if book is None:
        db.close()
        raise HTTPException(status_code=404, detail=f"Book with id = {book_id} not found")

    return book


async def get_books_list(db: Session) -> Optional[Book]:
    books = db.query(Book).all()
    return books


async def delete_this_book_by_id(book_id: int, db: Session):
    book = db.query(Book).filter(Book.id == book_id).first()

    if book is None:
        db.close()
        raise HTTPException(status_code=404, detail=f"Book with id = {book_id} not found")

    db.delete(book)
    db.commit()

    os.remove(book.file_path)

    return book

async def create_review(content: str, user_id: int, book_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    book = db.query(Book).filter(Book.id == book_id).first()

    if user is None:
        db.close()
        raise HTTPException(status_code=404, detail=f"User with id = {user_id} not found")
    elif book is None:
        db.close()
        raise HTTPException(status_code=404, detail=f"Book with id = {book_id} not found")

    review_model = Review(
        content=content,
        user_id=user_id,
        book_id=book_id
    )

    db.add(review_model)
    db.commit()
    db.refresh(review_model)

    return review_model


async def delete_this_review_by_id(review_id: int, db: Session):
    review = db.query(Review).filter(Review.id == review_id).first()

    if review is None:
        db.close()
        raise HTTPException(status_code=404, detail=f"Review with id = {review_id} not found")

    db.delete(review)
    db.commit()

    return review
