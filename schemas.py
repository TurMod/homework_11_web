from pydantic import BaseModel, Field, EmailStr
from datetime import date
from pydantic_extra_types.phone_numbers import PhoneNumber


class ContactModel(BaseModel):
    name: str = Field(max_length=50)
    lastname: str = Field(max_length=50)
    email: EmailStr = Field(max_length=50)
    phone_number: PhoneNumber = Field(max_length=30)
    birthday: date

class ContactResponse(ContactModel):
    id: int

    class Config:
        from_attributes = True
