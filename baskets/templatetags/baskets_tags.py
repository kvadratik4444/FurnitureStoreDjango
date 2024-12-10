from django import template

from baskets.models import Basket

register = template.Library()


@register.simple_tag()
def user_baskets(request):
    if request.user.is_authenticated:
        return Basket.objects.filter(user=request.user)