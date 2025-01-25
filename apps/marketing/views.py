from django.contrib.auth.decorators import login_not_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect


@login_not_required
def index(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("config:core_base_view")
    return render(request, "marketing/landing_page.html")


@login_not_required
def pricing(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("config:core_base_view")
    return render(request, "marketing/pricing.html")
