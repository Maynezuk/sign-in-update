from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    login: str
    password: str


class DbUser(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    name: str
    surname: str
    patronymic: str


class RefreshTokenBase(BaseModel):
    refresh_token: str