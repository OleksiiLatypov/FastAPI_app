from datetime import datetime, date
from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    name: str = Field()
    lastname: str = Field()
    email: EmailStr
    phone: str = Field()
    birthday: date = Field()
    additional_info: str = Field(max_length=300)


class ResponseContact(BaseModel):
    id: int
    name: str
    lastname: str
    email: EmailStr
    phone: str
    birthday: date
    additional_info: str

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_lenght=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=3)


class UserDb(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(UserDb):
    user: UserDb
    details: str = 'User successfully created'


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type = 'bearer'
