from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UserChangeForm,
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User, Organisation


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("first_name", "email", "phone_number")

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label="Name",
        widget=forms.TextInput(
            attrs={
                "class": "lg:text-sm form-input-border lg:py-4 lg:px-5 lg:mt-3 lg:min-w-96 bg-black placeholder:text-gray-600 rounded-lg",
                "placeholder": "Please enter your name",
                "autocomplete": "off",
                "autocapitalize": "off",
                "id": "name",
            }
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "lg:text-sm form-input-border lg:py-4 lg:px-5 lg:mt-3 lg:min-w-96 bg-black placeholder:text-gray-600 rounded-lg",
                "placeholder": "Email Address",
                "autocomplete": "off",
                "autocapitalize": "off",
                "id": "email",
            }
        ),
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "lg:text-sm form-input-border lg:py-4 lg:px-5 lg:mt-3 lg:min-w-96 bg-black placeholder:text-gray-600 rounded-lg",
                "placeholder": "Password",
                "autocomplete": "off",
                "autocapitalize": "off",
                "onchange": "confirmPassword()",
                "id": "password",
            }
        ),
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "text-sm form-input-border hidden lg:py-4 lg:px-5 mt-3 min-w-96 bg-black placeholder:text-gray-600 rounded-lg",
                "autocomplete": "off",
                "autocapitalize": "off",
                "placeholder": "Confirm Password",
                "id": "confirm_password",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["first_name", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class OrganisationRegisterForm(forms.ModelForm):
    name = forms.CharField(
        label="Organisation Name",
        widget=forms.TextInput(
            attrs={
                "class": "lg:text-sm form-input-border lg:py-4 lg:px-5 lg:mt-3 lg:min-w-96 bg-black placeholder:text-gray-600 rounded-lg",
                "placeholder": "Please enter the organisation's name",
                "autocomplete": "off",
                "autocapitalize": "off",
                "id": "name",
            }
        ),
    )
    team_size = forms.ChoiceField(
        choices=Organisation.TEAM_SIZE_CHOICES,
        label="Team Size",
        widget=forms.Select(
            attrs={
                "class": "lg:text-sm form-input-border lg:py-4 lg:px-5 lg:mt-3 lg:min-w-96 bg-black placeholder:text-gray-600 text-white rounded-lg",
                "autocomplete": "off",
                "id": "team_size",
            }
        ),
    )

    class Meta:
        model = Organisation
        fields = ["name", "team_size"]


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Email",
        widget=forms.TextInput(
            attrs={
                "class": "lg:text-sm form-input-border lg:py-4 lg:px-5 lg:mt-3 lg:min-w-96 bg-black placeholder:text-gray-600 rounded-lg",
                "autocomplete": "off",
                "autocapitalize": "off",
                "placeholder": "Email Address",
                "id": "email",
            }
        ),
    )
    password = forms.CharField(
        max_length=60,
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "lg:text-sm form-input-border lg:mt-3 lg:py-4 lg:px-5 lg:min-w-96 bg-black placeholder:text-gray-600 rounded-lg",
                "autocomplete": "false",
                "placeholder": "Password",
                "autocapitalize": "off",
                "id": "password",
            }
        ),
    )
    error_messages = {
        "invalid_login": _("Incorrect log in credentials"),
        "inactive": _("This account has been suspended"),
    }

    def confirm_login_allowed(self, user: User):
        if not user.is_active:
            raise ValidationError(
                "This account is inactive.",
                code="inactive",
            )
