from django.urls import path
from products.views import ProductIdView, ProductView

urlpatterns = [
    path("products/", ProductView.as_view()),
    path("products/<pk>/", ProductIdView.as_view()),
]
