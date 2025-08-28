"""Forms for orders app."""
from django import forms
from django.contrib.auth import get_user_model

from .models import Order

User = get_user_model()


class OrderForm(forms.ModelForm):
    """Form for orders."""

    def __init__(self, *args, **kwargs):
        """Overriden initializing method."""
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        """Save request user in the order model."""
        instance = super().save(commit=False)
        if self.request and self.request.user.is_authenticated:
            instance.user = self.request.user
        if commit:
            instance.save()
        return instance

    class Meta:
        """Meta class."""

        model = Order
        fields = (
            'phone_number',
            'delivery_adress',
            'cash_on_delivery',
            'requires_delivery'
        )
        widgets = {
            'delivery_adress': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
