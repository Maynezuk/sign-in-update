from pydantic import BaseModel


class UserBase(BaseModel):
    login: str
    password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    name: str
    surname: str
    patronymic: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str