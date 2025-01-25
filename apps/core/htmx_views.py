from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from libs.middleware.htmx import HtmxHttpRequest


@require_http_methods(["GET", "POST"])
def get_dashboard(request: HtmxHttpRequest):
    return render(request, "config/partials/dashboard.html")
