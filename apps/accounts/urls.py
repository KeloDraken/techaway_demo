from django.urls import path

from apps.accounts.htmx_views import update_user_profile
from apps.accounts.views import (
    register,
    user_login,
    user_logout,
    password_reset,
    create_organisation,
    add_card_information,
)

app_name = "accounts"
urlpatterns = [
    path("register/", register, name="user_register"),
    path("register/org/", create_organisation, name="create_organisation"),
    path("subscribe/", add_card_information, name="add_card_information"),
    path("login/", user_login, name="user_login"),
    path("logout/", user_logout, name="user_logout"),
    path("password-reset/", password_reset, name="user_password_reset"),
    path("settings/", update_user_profile, name="user_settings"),
]
