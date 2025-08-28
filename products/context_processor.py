"""Context processors for products app."""
from .models import Category


def categories_processor(request):
    """Get all categories."""
    categories = Category.objects.filter(
        parent__isnull=True,
    )
    return {
        'categories': categories
    }
