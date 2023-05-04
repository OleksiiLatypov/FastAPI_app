from datetime import date as birth_date

from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    name: str = Field(min_length=2, max_length=15)
    surname: str = Field(min_length=2, max_length=15)
    email: EmailStr
    phone: str = Field(min_length=6, max_length=16)
    birthday: birth_date
    additionally: str = Field(min_length=3, max_length=300)


class ResponseContact(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    phone: str
    birthday: birth_date
    additionally: str

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=3, max_length=16)
    email: str
    password: str = Field(min_length=3)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
