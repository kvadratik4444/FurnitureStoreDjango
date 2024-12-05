from django.core.paginator import Paginator
from django.shortcuts import render, get_list_or_404

from goods.models import Products


def catalog(request, catalog_slug):

    page = request.GET.get('page', 1)
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)

    goods = Products.objects.all()
    if catalog_slug != 'all':
        goods = goods.filter(category__slug=catalog_slug)

    print(goods)
    if on_sale:
        goods = goods.filter(discount__gt=0)

    if order_by and order_by != 'default':
        goods = goods.order_by(order_by)

    paginator = Paginator(goods,3)
    current_page = paginator.page(int(page))
    context = {
        'title': 'Home - Каталог',
        'goods': current_page,
        'slug_url': catalog_slug,
    }
    return render(request, 'goods/catalog.html', context)


def product(request, product_slug):

    product = Products.objects.get(slug=product_slug)

    context = {
        'product': product
    }
    return render(request, 'goods/product.html', context)