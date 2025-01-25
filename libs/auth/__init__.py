from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_not_required
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods


@login_not_required
@require_http_methods(["POST"])
def login_user_after_registration(request: HttpRequest) -> HttpResponseRedirect:
    """
    Authenticates and logs in a user after successful registration.

    Args:
        request (HttpRequest): The HTTP request object containing POST data with the user's credentials.

    Returns:
        HttpResponseRedirect: Redirects the user to the organisation creation page on successful login.
                              Redirects to the registration page with an error message on failure.
    """
    username = request.POST["email"]
    password = request.POST.get("password2")

    if password is None:
        password = request.POST.get("password")

        if password is None:
            messages.error(request, "Something went wrong. Please try again.")
            return redirect("accounts:user_register")

    user = authenticate(username=username.lower(), password=password)

    if user is not None:
        login(request, user)
        return redirect("accounts:create_organisation")
    else:
        messages.error(request, "Something went wrong. Please try again.")
        return redirect("accounts:user_register")
