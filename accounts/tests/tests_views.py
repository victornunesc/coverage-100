from urllib import response
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
            "email": fake.email(),
            "password": "1234",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "is_seller": fake.boolean(),
        }
        cls.invalid_account_data = {"email": "invalid@mail.com"}

    def test_success_should_create_account_when_request_is_correct(self):
        response = self.client.post(self.url, self.account_data)

        self.assertEqual(response.status_code, 201)
        self.assertNotIn("password", response.json())

    def test_fail_should_throw_bad_request_status_when_invalid_body(self):
        response = self.client.post(self.url, self.invalid_account_data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("password", response.json())

    def test_success_should_list_all_accounts_when_request_is_correct(self):
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

    def test_success_should_show_by_order_newest_accounts_when_request_is_correct(
        self,
    ):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            response.data[0]["date_joined"] > response.data[1]["date_joined"]
        )


class AccountIdViewTest(APITestCase):
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

    def test_success_should_patch_account_when_has_correct_credentials(self):
        token = Token.objects.create(user=self.account)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        response = self.client.patch(self.url, {"first_name": self.first_name})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["first_name"] == self.first_name)

    def test_fail_should_not_patch_account_when_not_has_credentials(self):
        response = self.client.patch(self.url, {"first_name": self.first_name})

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {"detail": "Authentication credentials were not provided."},
        )

    def test_fail_should_not_patch_account_when_has_insufficient_credentials(self):
        other_account = Account.objects.create_user(
            email="test2@mail.com",
            password="1234",
            is_seller=False,
        )

        token = Token.objects.create(user=other_account)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        response = self.client.patch(self.url, {"first_name": self.first_name})

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You do not have permission to perform this action."},
        )


class AccountManagementView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.admin_account_data = {
            "email": fake.email(),
            "password": "1234",
            "is_seller": fake.boolean(),
            "is_superuser": True,
        }
        cls.normal_account_data = {
            "email": fake.email(),
            "password": "1234",
            "is_seller": fake.boolean(),
        }

    def setUp(self) -> None:
        self.admin_account = Account.objects.create_user(**self.admin_account_data)
        self.normal_account = Account.objects.create_user(**self.normal_account_data)

    def get_url(self, id):
        return f"/api/accounts/{id}/management/"

    def test_success_should_change_is_active_attribute_when_is_super_user(self):
        url = self.get_url(id=self.normal_account.id)
        token = Token.objects.create(user=self.admin_account)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        response = self.client.patch(url, {"is_active": False})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["is_active"], False)

    def test_fail_should_not_allow_when_try_change_is_active_attribute_without_correct_credentials(
        self,
    ):
        url = self.get_url(id=self.admin_account.id)
        token = Token.objects.create(user=self.normal_account)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        response = self.client.patch(url, {"is_active": False})

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You do not have permission to perform this action."},
        )


class LoginViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.url = "/api/login/"
        cls.account_data = {
            "email": fake.email(),
            "password": "1234",
            "is_seller": fake.boolean(),
        }
        cls.invalid_credentials = {
            "email": fake.email(),
            "password": "1234",
        }

    def setUp(self) -> None:
        Account.objects.create_user(**self.account_data)

    def test_success_should_login_when_the_request_is_correct(self):
        response = self.client.post(
            self.url,
            {
                "email": self.account_data["email"],
                "password": self.account_data["password"],
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Token", response.json())

    def test_fail_should_not_allow_login_when_invalid_credentials(self):
        response = self.client.post(self.url, self.invalid_credentials)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {"detail": "invalid email or password"},
        )

    def test_fail_should_not_allow_login_when_invalid_body(self):
        response = self.client.post(self.url, {"": ""})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "email": ["This field is required."],
                "password": ["This field is required."],
            },
        )
