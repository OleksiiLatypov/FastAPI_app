import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from src.database.models import User
from src.schemas import UserModel
from src.repository.users import get_user_by_email, create_user, confirmed_email, update_token, update_avatar


class TestUser(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.session = MagicMock(spec=Session)
        self.user = User(id=1, email='stathem@test.ua')
        self.body = UserModel(username='Jason', email='stathem@test.ua', password='123456789')

    async def test_get_user_by_email(self):
        # user = User()
        self.session.query().filter().first.return_value = self.user
        result = await get_user_by_email(email=self.user.email, db=self.session)
        self.assertEqual(result, self.user)

    async def test_get_user_by_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_user_by_email(email=self.user.email, db=self.session)
        self.assertIsNone(result)

    async def test_create_user(self):
        body = self.body
        result = await create_user(body=body, db=self.session)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)

    async def test_update_token(self):
        self.session.query().filter().first.return_value = self.user
        token = self.user.refresh_token
        result = await update_token(user=self.user, token=token, db=self.session)
        # print(result, token)
        self.assertEqual(result, token)

    async def test_confirmed_email(self):
        self.session.query().filter().first.return_value = self.user
        result = await confirmed_email(email=self.user.email, db=self.session)
        self.assertTrue(self.user.confirmed)

    async def test_update_avatar(self):
        """
        The test_update_avatar function tests the update_avatar function.
        It does this by first creating a mock user object, and then setting the return value of
        the query() method to be that mock user object. The test then calls the update_avatar function,
        passing in an email address and url for a new avatar image. It asserts that after calling
        update_avatar, the avatar attribute of result is equal to url.

        :param self: Access the class attributes and methods
        :return: The user avatar
        :doc-author: Trelent
        """

        self.session.query().filter().first.return_value = self.user
        url = 'https://user_photo.png'
        result = await update_avatar(email=self.user.email, url=url, db=self.session)
        self.assertEqual(result.avatar, url)


if __name__ == '__main__':
    unittest.main()
