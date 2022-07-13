from django.urls import path
from accounts.views import AccountView

urlpatterns = [path("accounts/", AccountView.as_view())]
