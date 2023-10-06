from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
from pydantic import EmailStr

from db.connect_db import get_db
from db.models import User
from schemas import ContactModel, ContactResponse
from repository import contacts as repository_contacts
from services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get('/', response_model=List[ContactResponse])
async def get_contacts(name: str | None = None, lastname: str | None = None, email: EmailStr | None = None, nearest_birthday: bool = False, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    if nearest_birthday:
        return await repository_contacts.get_contacts_with_nearest_birthday(current_user, db)
    return await repository_contacts.get_contacts(name, lastname, email, current_user, db)

@router.post('/', response_model=ContactResponse, description='No more than 4 request per 10 seconds', dependencies=[Depends(RateLimiter(times=4, seconds=10))])
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    return await repository_contacts.create_contact(body, current_user, db)

@router.get('/{contact_id}', response_model=ContactResponse)
async def get_contact(contact_id: int, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact

@router.put('/{contact_id}', response_model=ContactResponse)
async def update_contact(contact_id: int, body: ContactModel, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact

@router.delete('/{contact_id}', response_model=ContactResponse)
async def delete_contact(contact_id: int, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.delete_contact(contact_id, current_user, db)
    if contact is None:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact
