from goods import views
from django.urls import path

app_name = 'goods'

urlpatterns = [
    path('search/', views.catalog, name='search'),
    path('<slug:catalog_slug>/', views.catalog, name='index'),
    path('product/<slug:product_slug>/', views.product, name='product'),
]
