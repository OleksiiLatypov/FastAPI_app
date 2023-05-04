import asyncio
from datetime import datetime, timedelta, date

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.connect import SessionLocal
from src.database.models import Contact, User
from src.schemas import ContactModel

database = SessionLocal()


async def get_contacts(user: User, db: Session):
    contacts = db.query(Contact).filter(and_(Contact.user_id == user.id)).all()
    return contacts


async def get_contact(contact_id: int, user: User, db: Session):
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    return contact


async def create_contact(body: ContactModel, user: User, db: Session):
    contact = Contact(**body.dict(), user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(body: ContactModel, contact_id: int, user: User, db: Session):
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.additionally = body.additionally
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session):
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def birthday_list(db: Session):
    contacts_all = db.query(Contact).all()
    current_day = date.today()
    next_week = [(current_day + timedelta(i)).strftime('%B %d') for i in range(7)]
    list_of_contacts = [contact for contact in contacts_all if contact.birthday.date().strftime('%B %d') in next_week]
    return list_of_contacts


async def searcher(part_to_search: str, db: Session):
    contact_list = []
    contacts_all = db.query(Contact).all()
    for contact in contacts_all:
        if part_to_search.lower() in contact.name.lower() and contact not in contact_list:
            contact_list.append(contact)
        if part_to_search.lower() in contact.surname.lower() and contact not in contact_list:
            contact_list.append(contact)
        if part_to_search.lower() in contact.email.lower() and contact not in contact_list:
            contact_list.append(contact)

    return contact_list


if __name__ == '__main__':
    print(asyncio.run(searcher('r', database)))
