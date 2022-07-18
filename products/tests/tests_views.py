from this import s
from urllib import response
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from faker import Faker

from accounts.models import Account
from products.models import Product


fake = Faker()


class ProductViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.url = "/api/products/"
        cls.seller_account_data = {
            "email": fake.email(),
            "password": "1234",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "is_seller": True,
        }
        cls.buyer_account_data = {
            "email": fake.email(),
            "password": "1234",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "is_seller": False,
        }
        cls.product_data = {
            "description": "Text",
            "price": fake.random_int(1, 2000),
            "quantity": fake.random_int(1, 100),
        }

    def setUp(self) -> None:
        self.seller_account = Account.objects.create_user(**self.seller_account_data)
        self.buyer_account = Account.objects.create_user(**self.buyer_account_data)

    def test_should_create_product_when_is_a_seller_account(self):
        token = Token.objects.create(user=self.seller_account)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        response = self.client.post(self.url, self.product_data)

        self.assertEqual(response.status_code, 201)
        self.assertIn(self.seller_account.email, response.data["seller"]["email"])

    def test_should_fail_create_product_when_is_buyer_account(self):
        token = Token.objects.create(user=self.buyer_account)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        response = self.client.post(self.url, self.product_data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You do not have permission to perform this action."},
        )

    def test_should_fail_create_product_when_not_has_credentials(self):
        response = self.client.post(self.url, self.product_data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {"detail": "Authentication credentials were not provided."},
        )

    def test_should_show_all_products_when_solicited(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
