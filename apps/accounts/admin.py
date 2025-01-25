from django.contrib import admin
from apps.accounts.models import User, Organisation, Billing


class UserAdmin(admin.ModelAdmin):
    search_fields = [
        "organisation__name",
        "username",
        "email",
        "first_name",
        "last_name",
        "phone_number",
    ]
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "phone_number",
        "is_superuser",
    ]
    list_filter = ["is_active", "is_staff", "is_superuser"]


class BillingAdmin(admin.ModelAdmin):
    search_fields = ["user__username", "paystack_customer_id", "subscription_id"]
    list_display = ["user", "paystack_customer_id", "subscription_id"]


class OrganisationAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "created_at"]


admin.site.register(User, UserAdmin)
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Billing, BillingAdmin)
