from pathlib import Path

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles

from routes.auth import router as auth_router
from routes.user import router as user_router
from routes.review import router as review_router
from routes.book import router as book_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(review_router)
app.include_router(book_router)

openapi_schema = get_openapi(
    title="My app",
    version="1.0.0",
    routes=app.routes
)

app.mount("/", StaticFiles(directory=Path("frontend/build"), html=True))


def run():
    import uvicorn
    uvicorn.run("app:app", reload=True)
