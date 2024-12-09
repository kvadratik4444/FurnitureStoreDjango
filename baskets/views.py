from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from baskets.models import Basket
from goods.models import Products
from baskets.utils import get_user_baskets


def basket_add(request):
    product_id = request.POST.get('product_id')
    product = Products.objects.get(id=product_id)

    if request.user.is_authenticated:
        basket, created = Basket.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': 1}
        )
        if not created:
            basket.quantity += 1
            basket.save()

    user_basket = get_user_baskets(request)
    basket_items_html = render_to_string(
        "baskets/includes/included_basket.html", {'baskets': user_basket}, request=request)

    response_data = {
        "message": "Товар добавлен в корзину",
        "basket_items_html": basket_items_html
    }

    return JsonResponse(response_data)


def basket_change(request):
    ...


def basket_remove(request):
    basket_id = request.POST.get('basket_id')

    basket = Basket.objects.get(id=basket_id)
    quantity = basket.quantity
    basket.delete()

    user_basket = get_user_baskets(request)
    basket_items_html = render_to_string(
        "baskets/includes/included_basket.html", {'baskets': user_basket}, request=request)

    response_data = {
        "message": "Товар удален из корзины",
        "basket_items_html": basket_items_html,
        "basket_deleted": quantity,
    }

    return JsonResponse(response_data)

