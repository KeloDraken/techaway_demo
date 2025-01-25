import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Extend Django's built-in User model to include additional fields or functionality.
    """

    object_id = models.UUIDField(unique=True, default=uuid.uuid4)

    is_organisation_owner = models.BooleanField(
        default=False,
        help_text="Indicates if the user is the owner of an organisation.",
    )
    has_subscribed = models.BooleanField(
        default=False, help_text="Indicates if the user has subscribed to the plan."
    )
    phone_number = models.CharField(null=True, blank=True, max_length=255)
    organisation = models.ForeignKey(
        "Organisation",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="members",
        help_text="The organisation the user belongs to.",
    )

    class Meta:
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username


class Organisation(models.Model):
    """
    Represents an organisation. Each organisation can have one owner and multiple additional users.
    """

    TEAM_SIZE_CHOICES = [
        ("small business (1-10)", "Small Business (1-10)"),
        ("medium business (11-50)", "Medium Business (11-50)"),
        ("large business (51+)", "Large Business (51+)"),
    ]

    object_id = models.UUIDField(unique=True, default=uuid.uuid4)
    name = models.CharField(
        max_length=255, unique=True, help_text="The name of the organisation."
    )
    team_size = models.CharField(
        max_length=255,
        help_text="How big is your team?",
        choices=TEAM_SIZE_CHOICES,
        default="small business (1-10)",
        null=False,
        blank=False,
    )
    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="owned_organisation",
        help_text="The user who owns the organisation and is billed.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Billing(models.Model):
    """
    Represents the billing information for a user. This includes the Paystack customer ID and subscription ID.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="billing",
        help_text="The user to bill.",
    )
    paystack_customer_id = models.CharField(
        max_length=255,
        help_text="The ID of the customer in Paystack.",
    )
    subscription_id = models.CharField(
        max_length=255,
        help_text="The ID of the subscription in Paystack.",
    )
    subscription_status = models.CharField(
        max_length=255,
        help_text="The status of the subscription in Paystack.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Billing"

    def __str__(self):
        return f"{self.user.username} - {self.paystack_customer_id}"
