import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from datetime import datetime

from schemas import ContactModel
from db.models import User, Contact
from repository.contacts import (
    get_contacts,
    get_contact,
    get_contacts_with_nearest_birthday,
    create_contact,
    update_contact,
    delete_contact,
)

class TestContact(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts(name=None, lastname=None, email=None, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_get_contacts_with_nearest_birthday(self):
        contacts = [Contact(birthday=datetime.now().date())]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_with_nearest_birthday(user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_create_contact(self):
        body = ContactModel(name='TestName', lastname='TestLastName', email='user@example.com', phone_number='+380666666666', birthday='2020-09-12')
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.lastname, body.lastname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertEqual(result.birthday, body.birthday)
        self.assertTrue(hasattr(result, 'id'))

    async def test_update_contact_found(self):
        body = ContactModel(name='TestName', lastname='TestLastName', email='user@example.com', phone_number='+380666666666', birthday='2020-09-12')
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        body = ContactModel(name='TestName', lastname='TestLastName', email='user@example.com', phone_number='+380666666666', birthday='2020-09-12')
        self.session.query().filter().first.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_delete_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await delete_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_delete_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await delete_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
