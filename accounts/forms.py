"""Forms for accounts app."""
from django import forms
from django.contrib.auth import get_user_model

from .models import Review


User = get_user_model()


class UserForm(forms.ModelForm):
    """Form based on user model."""

    class Meta:
        """Meta class."""

        model = User
        fields = ('first_name', 'last_name', 'phone_number')


class ReviewForm(forms.ModelForm):
    """Form based on review model."""

    RATING_CHOICES = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select()
    )

    class Meta:
        """Meta class."""

        model = Review
        fields = ('rating', 'text')
