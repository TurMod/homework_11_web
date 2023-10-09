from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import date, datetime
from pydantic_extra_types.phone_numbers import PhoneNumber


class ContactModel(BaseModel):
    name: str = Field(max_length=50)
    lastname: str = Field(max_length=50)
    email: EmailStr = Field(max_length=50)
    phone_number: PhoneNumber = Field(max_length=30)
    birthday: date


class ContactResponse(ContactModel):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str


class UserResponse(BaseModel):
    user: UserDb
    detail: str = 'User successfully created!'


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class RequestEmail(BaseModel):
    email: EmailStr
