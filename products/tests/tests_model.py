from django.test import TestCase
from faker import Faker

from products.models import Product
from accounts.models import Account


fake = Faker()


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.mock_account_seller = {
            "email": fake.email(),
            "password": "1234",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "is_seller": True,
        }

        cls.account = Account.objects.create_user(**cls.mock_account_seller)

        cls.mock_product = {
            "description": "Text",
            "price": fake.random_int(1, 2000),
            "quantity": fake.random_int(1, 100),
            "seller": cls.account,
        }

        cls.product = Product.objects.create(**cls.mock_product)

    def test_all_account_fields(self):
        self.assertIsInstance(self.product.description, str)
        self.assertEqual(self.product.description, self.mock_product["description"])

        self.assertIsInstance(self.product.price, int)
        self.assertEqual(self.product.price, self.mock_product["price"])

        self.assertIsInstance(self.product.quantity, int)
        self.assertEqual(self.product.quantity, self.mock_product["quantity"])

        self.assertIsInstance(self.product.seller, Account)
        self.assertEqual(self.product.seller, self.account)
