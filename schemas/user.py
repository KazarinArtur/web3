from pydantic import BaseModel


class UserDelete(BaseModel):
    id: int


class UserCreate(BaseModel):
    name: str
    email: str | None = None
    password: str
    role: bool = False


class UserUpdate(UserDelete):
    name: str | None = None
    email: str | None = None
    password: str | None = None
    role: bool | None = None


class UserResponse(UserCreate):
    class Config:
        from_attributes = True
