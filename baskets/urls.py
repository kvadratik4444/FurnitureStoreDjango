from django.urls import path
from baskets import views

app_name = 'baskets'

urlpatterns = [
    path('basket_add/', views.BasketAddView.as_view(), name='basket_add'),
    path('basket_change/', views.BasketChangeView.as_view(), name='basket_change'),
    path('basket_remove/', views.BasketRemoveView.as_view(), name='basket_remove'),
]
