"""
This module contains middleware for ensuring that administrators are associated with an organisation.
It defines a class used to redirect unauthenticated admin users to the organisation creation view.
"""

from django.shortcuts import redirect
from django.urls import reverse


class RequireOrganisationForAdmins:
    """
    Middleware to ensure that authenticated admin users belong to an organisation.
    If the user is authenticated but does not have an associated organisation, they are
    redirected to the organisation creation page.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Handles the incoming HTTP request to check if the authenticated user has an associated organisation.
        Redirects to the organisation creation page if no organisation is linked to the user.

        Args:
            request: The incoming HTTP request object.

        Returns:
            An HTTP response, either a redirect to the organisation creation page or the original response.
        """

        whitelist = [
            reverse("accounts:user_logout"),
        ]

        if request.path.startswith(reverse("admin:index")):
            return self.get_response(request)

        elif request.user.is_authenticated:
            if any(request.path.startswith(path) for path in whitelist):
                return self.get_response(request)

            if not request.user.organisation:
                if not request.path == reverse("accounts:create_organisation"):
                    return redirect("accounts:create_organisation")
        return self.get_response(request)
