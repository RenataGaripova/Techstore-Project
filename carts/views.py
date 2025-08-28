"""Views for working with carts."""

import json

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from products.models import Product
from .models import Cart, Wishlist


@login_required
def cart_add(request, product_slug):
    """Add products into the cart."""
    if request.method == "POST":
        product = get_object_or_404(Product, slug=product_slug)

        carts = Cart.objects.filter(
            user=request.user,
            product=product).select_related('product')
        try:
            data = json.loads(request.body)
            prod_quantity = int(data.get('quantity', 1))
        except (ValueError, TypeError, json.JSONDecodeError):
            prod_quantity = 1
        if carts.exists():
            cart = carts.first()
            new_quantity = min(
                product.quantity,
                cart.quantity + prod_quantity
            )
            carts.update(quantity=new_quantity)
        else:
            new_quantity = min(
                product.quantity, prod_quantity)

            cart = Cart.objects.create(
                user=request.user,
                product=product,
                quantity=new_quantity,
            )

        return JsonResponse({
            'success': True,
            'message': f'Item {product_slug} was added to your cart.'
            f'Current quantity in cart: {new_quantity}',
        })

    return JsonResponse({"success": False}, status=400)


@login_required
def cart_change(request, product_slug):
    """Change products inside the cart."""
    if request.method == 'POST':
        product = get_object_or_404(Product, slug=product_slug)

        user_carts = Cart.objects.filter(user=request.user)
        carts = user_carts.filter(product=product)
        prod_quantity = int(request.POST.get('quantity'))
        if carts.exists():
            cart = carts.first()
            cart.quantity = prod_quantity
            cart.save()
        else:
            Cart.objects.create(
                user=request.user,
                product=product,
                quantity=prod_quantity
            )

        return JsonResponse({
            'success': True,
            'product_quantity': cart.quantity,
            'cart_id': cart.id,
            'cart_total': user_carts.total_price(),
            'product_total': carts.total_price(),
        })
    return JsonResponse({"success": False}, status=400)


@login_required
def cart_remove(request, product_slug):
    """Remove products from cart."""
    if request.method == 'POST':
        product = Product.objects.get(slug=product_slug)

        user_carts = Cart.objects.filter(user=request.user)
        carts = user_carts.filter(product=product)
        if carts.exists():
            carts.delete()

        return JsonResponse({
            "success": True,
            "cart_total": user_carts.total_price(),
        })

    return JsonResponse({"success": False}, status=400)


@login_required
def cart_items(request):
    """Get cart items."""
    template_name = 'carts/user_cart.html'
    carts = Cart.objects.filter(
        user=request.user,
        product__quantity__gte=1,
    ).select_related('product')
    context = {
        'carts': carts,
    }
    return render(request, template_name, context)


@login_required
def wishlist_add(request, product_slug):
    """Add product to a wishlist."""
    if request.method == "POST":
        product = get_object_or_404(Product, slug=product_slug)
        try:
            Wishlist.objects.create(
                user=request.user,
                product=product,
            )
        except IntegrityError:
            return JsonResponse({
                'success': True,
                'message': f'Item {product.name} is arleady in your wishlist.'
            })
        return JsonResponse({
                'success': True,
                'message': f'Item {product.name} was added to your wishlist!'
            })


@login_required
def wishlist_remove(request, product_slug):
    """Remove product from a wishlist."""
    if request.method == "POST":
        product = get_object_or_404(Product, slug=product_slug)
        wishlist = Wishlist.objects.filter(
            user=request.user,
            product=product
        )
        if wishlist.exists():
            wishlist.delete()

        return JsonResponse({
            "success": True,
        })

    return JsonResponse({"success": False}, status=400)


@login_required
def wishlist_items(request):
    """Get wishlist items."""
    template_name = 'carts/user_wishlist.html'
    wishlists = Wishlist.objects.filter(
        user=request.user,
        product__quantity__gte=1,
    ).select_related('product')
    context = {
        'wishlists': wishlists,
    }
    return render(request, template_name, context)
