from datetime import datetime, timedelta, date
import unittest
from unittest.mock import MagicMock
from datetime import date
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel

from src.repository.contacts import get_contacts, get_contact, create_contact, search_contact, remove_contact, \
    birthday_list, update_contact
import asyncio


class TestContactRepository(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts(user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact(self):
        contact = Contact()
        self.session.query(Contact).filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = ContactModel(
            name='Jacob',
            surname='Kabasik',
            email='test@test.ua',
            phone='123456789',
            birthday=date.today(),
            additionally='Some info',
        )
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.surname, body.surname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.additionally, body.additionally)
        self.assertTrue(hasattr(result, "id"))

    async def test_update_contact(self):
        body = ContactModel(
            name='Gwido',
            surname='Van Rosum',
            email='van@test.ua',
            phone='987654321',
            birthday=date.today(),
            additionally='New info',
        )
        contact = Contact(id=1, name="Jane", surname="Doe", email="janedoe@example.com", phone="0987654321",
                          birthday=date.today(), additionally="Old info")
        self.session.query(Contact).filter().first.return_value = contact
        result = await update_contact(body=body, contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.surname, body.surname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.additionally, body.additionally)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_get_birthdays(self):
        contacts = [Contact(birthday=datetime.now() + timedelta(i)) for i in range(10)]

        self.session.query().all.return_value = contacts
        result = await birthday_list(db=self.session)
        self.assertEqual(result, contacts[:7])

    async def test_search_contact(self):
        contacts = [Contact(name='Mykola', surname='Luzan', email='luzan@test.ua'),
                    Contact(name='Mykola', surname='Hvylyovyi', email='mykola@meta.ua'),
                    Contact(name='Jason', surname='Statham', email='statham@test.ua')]
        self.session.query().all.return_value = contacts
        result = await search_contact('kola', db=self.session)
        self.assertIn(contacts[0], result)
        self.assertNotIn(contacts[2], result)
