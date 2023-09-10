from typing import List
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import extract

from db.models import Contact
from schemas import ContactModel


async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(**body.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def get_contacts(name: str, lastname: str, email: str, db: Session) -> List[Contact]:
    q = db.query(Contact)
    if name:
        return q.filter(Contact.name == name).all()
    elif lastname:
        return q.filter(Contact.lastname == lastname).all()
    elif email:
        return q.filter(Contact.email == email).all()
    return q.all()


async def get_contact(contact_id: int, db: Session) -> Contact | None:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def update_contact(contact_id: int, body: ContactModel, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.name = body.name
        contact.lastname = body.lastname
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        db.commit()
    return contact


async def delete_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact

async def get_contacts_with_nearest_birthday(db: Session) -> List[Contact]:
    today = datetime.now()
    contacts = db.query(Contact).filter(
    extract('month', Contact.birthday) == today.month,
    extract('day', Contact.birthday) >= today.day,
    extract('day', Contact.birthday) < today.day + 7
    ).all()
    return contacts
