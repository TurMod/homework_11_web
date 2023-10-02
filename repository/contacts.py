from typing import List
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import extract, and_

from db.models import Contact, User
from schemas import ContactModel


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    contact = Contact(name=body.name, lastname=body.lastname, email=body.email, phone_number=body.phone_number, birthday=body.birthday, user=user)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def get_contacts(name: str, lastname: str, email: str, user: User, db: Session) -> List[Contact]:
    q = db.query(Contact)
    if name:
        return q.filter(and_(Contact.name == name, Contact.user_id == user.id)).all()
    elif lastname:
        return q.filter(and_(Contact.lastname == lastname, Contact.user_id == user.id)).all()
    elif email:
        return q.filter(and_(Contact.email == email, Contact.user_id == user.id)).all()
    return q.filter(Contact.user_id == user.id).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def update_contact(contact_id: int, body: ContactModel, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.name = body.name
        contact.lastname = body.lastname
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        db.commit()
    return contact


async def delete_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact

async def get_contacts_with_nearest_birthday(user: User, db: Session) -> List[Contact]:
    today = datetime.now()
    contacts = db.query(Contact).filter(and_(
    extract('month', Contact.birthday) == today.month,
    extract('day', Contact.birthday) >= today.day,
    extract('day', Contact.birthday) < today.day + 7,
    Contact.user_id == user.id
    )).all()
    return contacts
