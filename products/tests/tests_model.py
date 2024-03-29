from django.db import IntegrityError
from django.test import TestCase
from faker import Faker

from products.models import Product
from accounts.models import Account


fake = Faker()


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.seller_account_data = {
            "email": fake.email(),
            "password": "1234",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "is_seller": True,
        }

    def setUp(self) -> None:
        self.account = Account.objects.create_user(**self.seller_account_data)

        self.product_data = {
            "description": "Text",
            "price": fake.random_int(1, 2000),
            "quantity": fake.random_int(1, 100),
            "seller": self.account,
        }

        self.product = Product.objects.create(**self.product_data)

    def test_all_account_fields(self):
        self.assertIsInstance(self.product.description, str)
        self.assertEqual(self.product.description, self.product_data["description"])

        self.assertIsInstance(self.product.price, int)
        self.assertEqual(self.product.price, self.product_data["price"])

        self.assertIsInstance(self.product.quantity, int)
        self.assertEqual(self.product.quantity, self.product_data["quantity"])

        self.assertIsInstance(self.product.seller, Account)
        self.assertEqual(self.product.seller, self.account)

    def test_fail_should_throw_integrity_error_when_not_has_selle_attr(self):
        self.assertRaises(
            IntegrityError, Product.objects.create, seller=None, price=0, quantity=0
        )
