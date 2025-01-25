"""
URL configuration for config project.
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    # marketing urls
    path("", include("apps.marketing.urls", namespace="marketing")),
    # Users App urls
    path("accounts/", include("apps.accounts.urls", namespace="accounts")),
    # Core app urls
    path("app/", include("apps.core.urls", namespace="core")),
]
