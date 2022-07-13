from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):
    def _create_user(self, email: str, password: str, **kwargs: dict):
        if not email:
            raise ValueError("The given email must be set.")

        if kwargs.get("first_name", False):
            kwargs["first_name"]: str = kwargs["first_name"].title()

        if kwargs.get("last_name", False):
            kwargs["last_name"]: str = kwargs["last_name"].title()

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email: str, password: str, **kwargs: dict):
        kwargs.setdefault("is_superuser", False)

        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email: str, password: str, **kwargs: dict):
        kwargs.setdefault("is_seller", False)
        kwargs.setdefault("is_superuser", True)

        return self._create_user(email, password, **kwargs)
