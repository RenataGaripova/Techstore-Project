"""Views for products."""
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.views.generic.detail import DetailView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.views.generic import CreateView, UpdateView, DeleteView

from products.models import Category, Product
from products.forms import FilterForm, FilterFormDetailed
from accounts.forms import ReviewForm
from .mixins import AuthorCheckMixin, ControlReviewMixin, BaseReviewMixin


def custom_logout(request):
    """Logout function."""
    logout(request)
    return render(request, 'registration/logged_out.html')


def get_page_object(
        objects,
        page_number,
        objects_count=settings.ITEMS_PER_PAGE
):
    """Paginator function."""
    paginator = Paginator(objects, objects_count)
    return paginator.get_page(page_number)


def category_base_view():
    """Retrieve category queryset."""
    return Category.objects.filter(parent__isnull=True).order_by('slug')


def products_base_view(
        sort_by='rating',
        category=None,
        producer='',
        pattern='',
        min_price=0,
        max_price=0,
):
    """Retrieve products queryset."""
    product_list = Product.objects.all()

    if category:
        product_list = category.get_all_products()

    if min_price:
        product_list = product_list.filter(price__gte=min_price)

    if max_price:
        product_list = product_list.filter(price__lte=max_price)

    if pattern:
        product_list = product_list.filter(name__contains=pattern)

    if producer:
        product_list = product_list.filter(producer=producer)

    product_list = product_list.annotate(
            product_rating=Avg('reviews__rating'))
    sort_by = sort_by or 'rating'
    return product_list.order_by(sort_by)


def index(request):
    """View for the main page."""
    template_name = 'products/index.html'
    category_list = category_base_view()[:4]
    context = {
        'category_list': category_list,
    }
    return render(request, template_name, context)


def category_list_view(request):
    """View for categories page."""
    template_name = 'products/category_list.html'

    if request.method == 'POST':
        pattern = request.POST.get('pattern')
        category_list = category_base_view().filter(name__contains=pattern)
    else:
        category_list = category_base_view()

    page_obj = get_page_object(
            category_list,
            request.GET.get('page'),
            settings.CATEGORIES_PER_PAGE,
    )

    context = {
        'page_obj': page_obj,
    }
    return render(request, template_name, context)


def products_by_category_view(request, category_slug):
    """View for list of products by category."""
    template_name = 'products/products_by_category_list.html'

    form = FilterForm(request.GET or None)

    category = get_object_or_404(
            Category.objects.all(),
            slug=category_slug
    )

    if form.is_valid():
        product_list = products_base_view(
            category=category,
            pattern=form.cleaned_data['search_field'],
            min_price=form.cleaned_data['min_price'],
            max_price=form.cleaned_data['max_price'],
            sort_by=form.cleaned_data['sort_by'],
        )
    else:
        product_list = products_base_view(
            category=category,
        )

    page_obj = get_page_object(
            product_list,
            request.GET.get('page'),
            settings.ITEMS_PER_PAGE,
    )

    context = {
        'category': category,
        'form': form,
        'page_obj': page_obj,
        'sub_categories': category.subcategories.all(),
    }
    return render(request, template_name, context)


def all_products_view(request):
    """View for list of all products."""
    template_name = 'products/products_by_category_list.html'

    form = FilterFormDetailed(request.GET or None)

    if form.is_valid():
        if form.cleaned_data['category']:
            category = get_object_or_404(
                Category.objects.all(),
                slug=form.cleaned_data['category'],
            )
        else:
            category = None
        product_list = products_base_view(
            category=category,
            producer=form.cleaned_data['producer'],
            pattern=form.cleaned_data['search_field'],
            min_price=form.cleaned_data['min_price'],
            max_price=form.cleaned_data['max_price'],
            sort_by=form.cleaned_data['sort_by'],
        )
    else:
        product_list = products_base_view()

    page_obj = get_page_object(
            product_list,
            request.GET.get('page'),
            settings.ITEMS_PER_PAGE,
    )

    context = {
        'form': form,
        'page_obj': page_obj,
    }
    return render(request, template_name, context)


class ProductDetailView(DetailView):
    """View class for product page."""

    model = Product
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'

    def get_context_data(self, **kwargs):
        """Override get context method."""
        context = super().get_context_data(**kwargs)

        average_rating = self.get_object().reviews.aggregate(
            Avg('rating')
        )['rating__avg']
        gallery = self.get_object().images.all()
        reviews = self.get_object().reviews.all()
        form = ReviewForm()

        context['gallery'] = gallery
        context['reviews'] = reviews
        context['form'] = form
        context['average_rating'] = average_rating
        return context


class ReviewCreateView(
    LoginRequiredMixin,
    BaseReviewMixin,
    CreateView
):
    """CBV для добавления комментариев к посту."""

    template_name = 'products/product_detail.html'
    form_class = ReviewForm

    def form_valid(self, form):
        """Validate review and assign current user as it's author."""
        form.instance.author = self.request.user
        form.instance.product = get_object_or_404(
            Product,
            slug=self.kwargs.get('product_slug')
        )
        return super().form_valid(form)


class ReviewUpdateView(
    AuthorCheckMixin,
    BaseReviewMixin,
    ControlReviewMixin,
    UpdateView
):
    """CBV for comment update."""

    form_class = ReviewForm


class ReviewDeleteView(
    AuthorCheckMixin,
    BaseReviewMixin,
    ControlReviewMixin,
    DeleteView
):
    """CBV для удаления комментариев."""

    def get_context_data(self, **kwargs):
        """Override context data method."""
        context = super().get_context_data(**kwargs)
        context['review'] = ReviewForm(instance=self.get_object())
        return context
