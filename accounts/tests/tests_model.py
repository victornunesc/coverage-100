import email
from django.test import TestCase
from faker import Faker
from accounts.models import Account
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AbstractUser


fake = Faker()


class AccountModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.account_data = {
            "email": fake.email(),
            "password": "1234",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "is_seller": fake.boolean(),
        }

    def setUp(self) -> None:
        self.account_obj: Account = Account.objects.create_user(**self.account_data)

    def test_all_account_fields(self):
        self.assertIsInstance(self.account_obj.email, str)
        self.assertEqual(self.account_obj.email, self.account_data["email"])

        self.assertIsInstance(self.account_obj.password, str)
        self.assertTrue(
            check_password(self.account_data["password"], self.account_obj.password)
        )

        self.assertIsInstance(self.account_obj.first_name, str)
        self.assertEqual(self.account_obj.first_name, self.account_data["first_name"])

        self.assertIsInstance(self.account_obj.last_name, str)
        self.assertEqual(self.account_obj.last_name, self.account_data["last_name"])

        self.assertEqual(self.account_obj.is_seller, self.account_data["is_seller"])
        self.assertIsInstance(self.account_obj, AbstractUser)

    def test_fail_should_throw_value_error_exception_when_not_has_email(self):
        self.assertRaises(
            ValueError, Account.objects.create_user, email=None, password="123"
        )

    def test_success_should_create_super_user_when_called_correct_method(self):
        account = Account.objects.create_superuser(
            email="adm@mail.com", password="1234"
        )

        self.assertTrue(account.is_superuser)
