"""Mixins used in products CBV's."""
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from accounts.models import Review
from .models import Product


class AuthorCheckMixin(UserPassesTestMixin):
    """Checks if the user is review's author."""

    def test_func(self):
        """Check if user is an author."""
        object = self.get_object()
        return object.author == self.request.user

    def handle_no_permission(self):
        """Handle no permission."""
        product_slug = self.kwargs.get('product_slug')
        return redirect('products:product_details', product_slug=product_slug)


class BaseReviewMixin:
    """Base review mixin."""

    model = Review

    def get_success_url(self):
        """Success url for posting a review."""
        return reverse(
            'products:product_details',
            kwargs={'product_slug': self.kwargs['product_slug']}
        )


class ControlReviewMixin:
    """Mixin for review update and delete."""

    template_name = 'accounts/review.html'

    def get_object(self, queryset=None):
        """Get review of a product by slug and id."""
        product = get_object_or_404(
            Product,
            slug=self.kwargs['product_slug']
        )
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            product=product,
        )
