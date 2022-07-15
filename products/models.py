from django.db import models


class Product(models.Model):
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    seller = models.ForeignKey(
        "accounts.Account", on_delete=models.CASCADE, related_name="products"
    )
