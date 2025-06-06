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


# class PostBase(BaseModel):
#     title: str
#     body: str
#     author_id: int
#
#
# class PostCreate(PostBase):
#     pass
#
#
# class PostResponse(PostBase):
#     id: int
#     author: User
#
#     class Config:
#         orm_mode = True