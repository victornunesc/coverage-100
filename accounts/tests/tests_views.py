from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from accounts.models import Account
from faker import Faker

fake = Faker()


class AccountViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.url = "/api/accounts/"
        cls.account_data = {
            "email": "test@mail.com",
            "password": "1234",
            "first_name": "John",
            "last_name": "Doe",
            "is_seller": True,
        }
        cls.invalid_account_data = {"email": "invalid@mail.com"}

    def test_create_account(self):
        response = self.client.post(self.url, self.account_data)

        self.assertEqual(response.status_code, 201)
        self.assertNotIn("password", response.json())

    def test_list_all_accounts(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json(), list))


class AccountNewestViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = "/api/accounts/newest/2/"

        for i in range(2):
            Account.objects.create_user(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                password="test",
                is_seller=fake.boolean(),
            )

    def test_newest_accounts(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            response.data[0]["date_joined"] > response.data[1]["date_joined"]
        )


class AccountIdView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.url = "/api/accounts/1/"
        cls.account_data = {
            "email": "test@mail.com",
            "password": "1234",
            "first_name": "John",
            "last_name": "Doe",
            "is_seller": True,
        }

    def setUp(self) -> None:
        self.first_name = fake.first_name()
        self.account = Account.objects.create_user(**self.account_data)

    def test_patch_account_with_credentials(self):
        token = Token.objects.create(user=self.account)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        response = self.client.patch(self.url, {"first_name": self.first_name})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["first_name"] == self.first_name)

    def test_fail_patch_account_without_credentials(self):
        response = self.client.patch(self.url, {"first_name": self.first_name})

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {"detail": "Authentication credentials were not provided."},
        )

    def test_fail_patch_account_with_insufficient_credentials(self):
        other_account = Account.objects.create_user(
            email="test2@mail.com",
            password="1234",
            is_seller=False,
        )

        token = Token.objects.create(user=other_account)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        response = self.client.patch(self.url, {"first_name": self.first_name})

        print(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You do not have permission to perform this action."},
        )
