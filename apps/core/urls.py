from django.urls import path
from apps.core.views import core_base_view
from apps.core.htmx_views import get_dashboard

app_name = "core"

urlpatterns = [
    path("home/", core_base_view, name="core_base_view"),
    path("dashboard/", get_dashboard, name="user_dashboard"),
]
