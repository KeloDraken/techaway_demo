"""
This module contains views for handling user authentication, registration, and organisation creation for the application.

Functions:
    - register: Handles new user registration by rendering the form, validating input, and saving the user.
    - create_organisation: Manages organisation registration and associates the organisation with the currently logged-in user.
    - password_reset: Renders the password reset page.

Classes:
    - UserLoginView: A custom login view that authenticates users with a specific login form.

Dependencies:
    - Django libraries for HTTP requests, authentication, forms, and messages.
    - Custom forms from `accounts.forms`.

Usage:
    Import the relevant function or class into your URL configuration to map it to a URL pattern.
"""

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_not_required, login_required
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from apps.accounts.forms import (
    UserRegisterForm,
    UserLoginForm,
    OrganisationRegisterForm,
)
from libs.auth import login_user_after_registration


@login_not_required
@require_http_methods(["GET", "POST"])
def register(request: HttpRequest) -> HttpResponse:
    """
    Handles user registration.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the registration form if the method is GET.
                      On POST, validates and saves the user data, and logs the user in if successful.
                      Otherwise, re-renders the form with validation errors.
    """
    if request.user.is_authenticated:
        return redirect("config:core_base_view")

    if request.method == "GET":
        form = UserRegisterForm()
        return render(request, "accounts/user_registration.html", {"form": form})

    form = UserRegisterForm(request.POST)
    if form.is_valid():
        try:
            form.save()
            return login_user_after_registration(request)
        except IntegrityError:
            form.add_error(
                None, {"email": "User already exists. Try logging in instead."}
            )
    return render(request, "accounts/user_registration.html", {"form": form})


@login_required
@require_http_methods(["GET", "POST"])
def add_card_information(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        messages.success(
            request,
            (
                "Welcome to Jocoss! We’re thrilled to have you on board. "
                "We’ve designed our system to be as user-friendly as possible, "
                "but if you have any questions or suggestions, don’t hesitate to "
                "reach out to us. Since we’re also built on Jocoss, "
                "you can expect a swift response."
            ),
        )
    return render(request, "accounts/add_credit_card_information.html")


@login_required
@require_http_methods(["GET", "POST"])
def create_organisation(request: HttpRequest) -> HttpResponse:
    """
    Handles organisation registration for the currently logged-in user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the organisation registration form if the method is GET.
                      On POST, validates and saves the organisation data.
                      Redirects to the user dashboard on success or re-renders the form with errors.
    """
    if request.method == "GET":
        form = OrganisationRegisterForm()
        return render(
            request, "accounts/organisation_registration.html", {"form": form}
        )

    form = OrganisationRegisterForm(request.POST)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.owner = request.user
        instance.save()

        request.user.is_organisation_owner = True
        request.user.organisation = instance
        request.user.save()
        return redirect("config:core_base_view")

    return render(request, "accounts/organisation_registration.html", {"form": form})


class UserLoginView(LoginView):
    """
    Custom login view for user authentication.

    Attributes:
        template_name (str): Path to the HTML template used for the login form.
        authentication_form (Form): The form class used to authenticate users.
        redirect_authenticated_user (bool): Whether to redirect authenticated users to their dashboard.
        next_page (str): URL to redirect to after logout.
    """

    template_name = "accounts/user_login.html"
    authentication_form = UserLoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        """
        Override the form_valid method to add a success message after login.
        """
        messages.success(self.request, "Welcome back! You are now logged in.")
        return super().form_valid(form)


user_login = UserLoginView.as_view()


@login_required
@require_http_methods(["GET"])
def user_logout(request: HttpRequest) -> HttpResponseRedirect:
    """
    Handle user logout request.

    This view is responsible for logging out the user, displaying a success
    message, and redirecting them to the landing page.

    Args:
        request (HttpRequest): The HTTP request object used to log out the
        authenticated user.

    Returns:
        HttpResponseRedirect: A redirect response to the landing page.
    """
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("accounts:user_login")


@login_not_required
@require_http_methods(["GET", "POST"])
def password_reset(request: HttpRequest) -> HttpResponse:
    """
    Renders the password reset page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the forgot password page.
    """
    if request.user.is_authenticated:
        return redirect("config:core_base_view")
    return render(request, "accounts/forgot_password.html")
