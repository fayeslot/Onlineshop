from django.urls import path
from .views import *

urlpatterns = [
    path("create-account/",signup, name="account-signup"),
    path("account-login/",signin, name="account-login"),
    path("account-logout/",signout, name="account-logout"),
]