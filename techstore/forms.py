from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form."""

    email = forms.EmailField(
        required=True,
        help_text="Enter a valid email adress."
    )

    class Meta:
        """Class Meta."""

        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('email',)
