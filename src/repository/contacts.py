import asyncio
from datetime import datetime, timedelta, date

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.connect import SessionLocal
from src.database.models import Contact, User
from src.schemas import ContactModel

database = SessionLocal()


async def get_contacts(user: User, db: Session):
    """
    The get_contacts function returns a list of contacts for the user with the given id.


    :param user: User: Get the user id from the database
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    """
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


async def search_contact(search_word: str, db: Session):
    result = []
    all_contacts = db.query(Contact).all()
    for contact in all_contacts:
        if search_word in contact.name:
            result.append(contact)
        if search_word in contact.surname:
            result.append(contact)
        if search_word in contact.email:
            result.append(contact)
    return result


"""
    result = []
    if find_item:
        contacts_f_name = db.query(Contact).filter(and_(Contact.user_id == current_user,
                                                        Contact.first_name.like(f'%{find_item}%'))).all()
        if contacts_f_name:
            result.extend(contacts_f_name)

        contacts_l_name = db.query(Contact).filter(and_(Contact.user_id == current_user,
                                                        Contact.last_name.like(f'%{find_item}%'))).all()
        if contacts_l_name:
            result.extend(contacts_l_name)

        contacts_email = db.query(Contact).filter(and_(Contact.user_id == current_user,
                                                       Contact.email.like(f'%{find_item}%'))).all()
        if contacts_email:
            result.extend(contacts_email)
        result = list(set(result))
    return result"""
