from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages

from orders.models import Order, OrderItem
from orders.forms import CreateOrderForm
from baskets.models import Basket


@login_required
def create_order(request):
    if request.method == 'POST':
        form = CreateOrderForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
                    basket_items = Basket.objects.filter(user=user)
                    if basket_items.exists():
                        order = Order.objects.create(
                            user=user,
                            phone_number=form.cleaned_data['phone_number'],
                            requires_delivery=form.cleaned_data['requires_delivery'],
                            delivery_address=form.cleaned_data['delivery_address'],
                            payment_on_get=form.cleaned_data['payment_on_get'],
                        )
                        for basket_item in basket_items:
                            product = basket_item.product
                            name = basket_item.product.name
                            price = basket_item.product_price()
                            quantity = basket_item.quantity

                            if product.quantity < quantity:
                                raise ValidationError(f"Недостаточное кол-во товара {name} на складе. \n В наличии - {product.quantity}")

                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                price=price,
                                name=name,
                                quantity=quantity,
                            )
                            product.quantity -= quantity
                            product.save()

                        basket_items.delete()

                        messages.success(request, "Заказ оформлен")
                        return redirect("user:profile")
            except ValidationError as error:
                messages.error(request, str(error))
                return redirect("basket:order")
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }
        form = CreateOrderForm(initial=initial)

    context = {
        'title': 'Home - Оформление заказа',
        'form': form,
        'order': True,
    }

    return render(request, 'orders/create_order.html', context)
