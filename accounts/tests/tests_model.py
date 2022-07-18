from django.test import TestCase
from accounts.models import Account
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AbstractUser


class AccountModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.mock_account = {
            "email": "test@mail.com",
            "password": "1234",
            "first_name": "John",
            "last_name": "Doe",
            "is_seller": True,
        }
        cls.account_obj: Account = Account.objects.create_user(**cls.mock_account)

    def test_all_account_fields(self):
        self.assertIsInstance(self.account_obj.email, str)
        self.assertEqual(self.account_obj.email, self.mock_account["email"])

        self.assertIsInstance(self.account_obj.password, str)
        self.assertTrue(
            check_password(self.mock_account["password"], self.account_obj.password)
        )

        self.assertIsInstance(self.account_obj.first_name, str)
        self.assertEqual(self.account_obj.first_name, self.mock_account["first_name"])

        self.assertIsInstance(self.account_obj.last_name, str)
        self.assertEqual(self.account_obj.last_name, self.mock_account["last_name"])

        self.assertEqual(self.account_obj.is_seller, self.mock_account["is_seller"])
        self.assertIsInstance(self.account_obj, AbstractUser)
