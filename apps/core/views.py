"""
This module contains views for handling user-related pages in the application.
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


@login_required
def core_base_view(request: HttpRequest) -> HttpResponse:
    """
    Render the user dashboard page.

    This view is protected by login and will render the user's dashboard
    template when accessed.

    Args:
        request (HttpRequest): The HTTP request object for the current request.

    Returns:
        HttpResponse: The rendered dashboard page.
    """
    return render(request, "config/base.html")
