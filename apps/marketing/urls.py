from django.urls import path

from apps.marketing.views import index, pricing

app_name = "marketing"


urlpatterns = [
    path("", index, name="index"),
    path("pricing/", pricing, name="pricing"),
]
