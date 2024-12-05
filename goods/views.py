from django.core.paginator import Paginator
from django.shortcuts import render, get_list_or_404

from goods.models import Products


def catalog(request, catalog_slug, page=1):
    goods = Products.objects.all()
    if catalog_slug != 'all':
        goods = get_list_or_404(goods.filter(category__slug=catalog_slug))

    paginator = Paginator(goods,3)
    current_page = paginator.page(page)
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