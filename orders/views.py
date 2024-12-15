from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ValidationError
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import FormView
from django.urls import reverse_lazy
from orders.models import Order, OrderItem
from orders.forms import CreateOrderForm
from baskets.models import Basket


class CreateOrderView(LoginRequiredMixin, FormView):
    template_name = 'orders/create_order.html'
    form_class = CreateOrderForm
    success_url = reverse_lazy('users:profile')

    def get_initial(self):
        initial = super().get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Оформление заказа'
        context['order'] = True
        return context

    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = self.request.user
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
                            raise ValidationError(
                                f"Недостаточное кол-во товара {name} на складе. \n В наличии - {product.quantity}")

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

                    messages.success(self.request, "Заказ оформлен")
                    return redirect("user:profile")
        except ValidationError as error:
            messages.error(self.request, str(error))
            return redirect("orders:order_list")

    def form_invalid(self, form):
        messages.error(self.request, 'Заполните все обязательные поля!')
        return redirect("orders:create_order")
