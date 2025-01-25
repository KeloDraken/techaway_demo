from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from apps.accounts.forms import UserUpdateForm
from libs.middleware.htmx import HtmxHttpRequest


@require_http_methods(["GET", "PUT"])
def update_user_profile(request: HtmxHttpRequest):
    if request.method == "GET":
        form = UserUpdateForm()
        return render(request, "accounts/partials/user_settings.html", {"form": form})

    form = UserUpdateForm(request.PUT, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect("accounts:user_settings")
    return render(request, "accounts/partials/user_settings.html", {"form": form})
