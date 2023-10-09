import unittest
from unittest.mock import MagicMock, patch

from sqlalchemy.orm import Session
from libgravatar import Gravatar

from db.models import User
from schemas import UserModel
from repository.users import (
    create_user,
    confirmed_email,
    get_user_by_email,
    update_token,
    update_avatar,
)


class TestRepositoryUsers(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.body = UserModel(
            username="username",
            email="email@example.com",
            password="qwerty_123",
        )

    async def test_create_user(self):
        with patch.object(Gravatar, 'get_image', return_value="https://www.gravatar.com/avatar/test_image") as mock_get_image:

            result = await create_user(self.body, self.session)

            mock_get_image.assert_called_once_with()
            self.assertIsInstance(result, User)
            self.assertEqual(result.username, self.body.username)
            self.assertEqual(result.email, self.body.email)
            self.assertEqual(result.password, self.body.password)
            self.assertEqual(result.avatar, "https://www.gravatar.com/avatar/test_image")
            self.assertTrue(hasattr(result, 'id'))

            self.session.add.assert_called_once_with(result)
            self.session.commit.assert_called_once()
            self.session.refresh.assert_called_once_with(result)

    async def test_confirmed_email(self):
        user = User(id=1, confirmed=True)

        result = await confirmed_email(email='user@example.com', db=self.session)

        self.assertIsNone(result)
        self.assertTrue(user.confirmed)
        self.session.commit.assert_called_once()

    async def test_get_user_by_email_found(self):
        user = User()
        self.session.query().filter().first.return_value = user

        result = await get_user_by_email(email="email@example.com", db=self.session)

        self.assertEqual(result, user)

    async def test_get_user_by_email_not_found(self):
        self.session.query().filter().first.return_value = None

        result = await get_user_by_email(email="email@example.com", db=self.session)

        self.assertIsNone(result)

    async def test_update_token_found(self):
        user = User()
        self.session.query().filter().first.return_value = user

        new_token = "new_token"
        result = await update_token(user=user, token=new_token, db=self.session)

        self.assertIsNone(result)
        self.assertEqual(user.refresh_token, new_token)
        self.session.commit.assert_called_once()

    async def test_update_avatar_found(self):
        user = User()
        self.session.query().filter().first.return_value = user

        result = await update_avatar(email='user@example.com', url='new_url_address', db=self.session)

        self.assertEqual(result, user)
        self.session.commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()