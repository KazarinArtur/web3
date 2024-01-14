import os
from typing import Annotated, Text, List

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse

from db import get_database
from db.actions import create_book, book_by_id, get_books_list, current_user, delete_this_book_by_id
from schemas.book import BookCreate, BookResponse
from schemas.user import UserResponse

router = APIRouter(
    prefix="/book",
    tags=["Books"]
)


@router.post("/upload")
async def upload_book(file: Annotated[UploadFile, File(description="A file read as UploadFile")], name: str,
                      description: Text = None, db: Session = Depends(get_database),
                      user: UserResponse = Depends(current_user)) -> BookResponse:
    file_path = f"books//{file.filename}"
    with open(file_path, "wb") as new_book:
        new_book.write(file.file.read())

    book_schema = BookCreate(
        name=name,
        description=description,
        file_path=file_path
    )

    book = await create_book(book_schema.name, book_schema.description, book_schema.file_path, db)
    return BookResponse.model_validate(book)


@router.get("/download/{file_path:path}")
def download_book(file_path: str):
    return FileResponse(path=file_path, filename=file_path[7:], media_type="application/pdf")


@router.get("/get/{book_id}")
async def get_book_by_id(book_id: int, db: Session = Depends(get_database), user: UserResponse = Depends(current_user)):
    book = await book_by_id(book_id, db)
    return book


@router.get('/list')
async def list_books(db: Session = Depends(get_database), user: UserResponse = Depends(current_user)) -> List[
    BookResponse]:
    """
    Lists all books
    """
    books = await get_books_list(db)
    return books


@router.delete("/delete/{book_id}")
async def delete_book_by_id(book_id: int, db: Session = Depends(get_database),
                            user: UserResponse = Depends(current_user)) -> BookResponse:
    book = await delete_this_book_by_id(book_id, db)
    return BookResponse.model_validate(book)


@router.get("/open/{file_path:path}")
async def open_book(file_path: str, user: UserResponse = Depends(current_user)):
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Book with path {file_path} not found")

    return FileResponse(file_path)
