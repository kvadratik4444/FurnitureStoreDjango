from django.shortcuts import render, redirect

from baskets.models import Basket
from goods.models import Products


def basket_add(request, product_slug):
    product = Products.objects.get(slug=product_slug)

    if request.user.is_authenticated:
        basket, created = Basket.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': 1}
        )
        if not created:
            basket.quantity += 1
            basket.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))


def basket_change(request, product_slug):
    ...


def basket_remove(request, product_slug):
    ...

