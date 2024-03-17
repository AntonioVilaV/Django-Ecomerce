from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, ValidationError

from apps.profiles.models import ContactDetails


class ContactDetailsForm(ModelForm):
    class Meta:
        model = ContactDetails
        fields = ["phone", "address"]

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if not phone:
            raise ValidationError("This field cannot be empty")
        elif not phone.isdigit():
            raise ValidationError("You can only enter numbers")
        else:
            return phone


class UserDetailsForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "groups"]
        labels = {
            "username": "User name",
            "first_name": "Name",
            "last_name": "Second name",
            "email": "Email",
            "groups": "Groups",
        }
