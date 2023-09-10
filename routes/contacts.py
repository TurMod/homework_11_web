from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from db.connect_db import get_db
from schemas import ContactModel, ContactResponse
from pydantic import EmailStr
from repository import contacts as repository_contacts

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get('/', response_model=List[ContactResponse])
async def get_contacts(name: str | None = None, lastname: str | None = None, email: EmailStr | None = None, nearest_birthday: bool = False, db: Session = Depends(get_db)):
    if nearest_birthday:
        return await repository_contacts.get_contacts_with_nearest_birthday(db)
    return await repository_contacts.get_contacts(name, lastname, email, db)

@router.post('/', response_model=ContactResponse)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, db)

@router.get('/{contact_id}', response_model=ContactResponse)
async def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact

@router.put('/{contact_id}', response_model=ContactResponse)
async def update_contact(contact_id: int, body: ContactModel, db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact

@router.delete('/{contact_id}', response_model=ContactResponse)
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.delete_contact(contact_id, db)
    if contact is None:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact