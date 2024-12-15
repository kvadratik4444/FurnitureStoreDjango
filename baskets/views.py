from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View

from baskets.models import Basket
from goods.models import Products
from baskets.utils import get_user_baskets


class BasketAddView(View):
    def post(self, request):
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
        else:
            if not request.session.session_key:
                request.session.create()

            basket, created = Basket.objects.get_or_create(
                session_key=request.session.session_key,
                product=product,
                defaults={'quantity': 1}
            )
            if not created:
                basket.quantity += 1
                basket.save()

        user_basket = get_user_baskets(request)
        basket_items_html = render_to_string(
            "baskets/includes/included_basket.html", {'baskets': user_basket}, request=request
        )

        response_data = {
            "message": "Товар добавлен в корзину",
            "basket_items_html": basket_items_html
        }

        return JsonResponse(response_data)


class BasketChangeView(View):
    def post(self, request):
        basket_id = request.POST.get('basket_id')
        quantity = request.POST.get('quantity')

        basket = Basket.objects.get(id=basket_id)
        basket.quantity = quantity
        basket.save()

        user_basket = get_user_baskets(request)
        context = {"baskets": user_basket}

        referer = request.META.get('HTTP_REFERER')
        if reverse('orders:create_order') in referer:
            context["order"] = True

        basket_items_html = render_to_string(
            "baskets/includes/included_basket.html", context, request=request)

        response_data = {
            "message": "Количество изменено",
            "basket_items_html": basket_items_html,
            "quantity": quantity,
        }

        return JsonResponse(response_data)


class BasketRemoveView(View):
    def post(self, request):
        basket_id = request.POST.get('basket_id')

        basket = Basket.objects.get(id=basket_id)
        quantity = basket.quantity
        basket.delete()

        user_basket = get_user_baskets(request)
        context = {"baskets": user_basket}

        referer = request.META.get('HTTP_REFERER')
        if reverse('orders:create_order') in referer:
            context["order"] = True

        basket_items_html = render_to_string(
            "baskets/includes/included_basket.html", context, request=request)

        response_data = {
            "message": "Товар удален из корзины",
            "basket_items_html": basket_items_html,
            "quantity_deleted": quantity,
        }

        return JsonResponse(response_data)
