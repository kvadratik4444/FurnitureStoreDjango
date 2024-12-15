from orders import views
from django.urls import path

app_name = 'orders'

urlpatterns = [
    path('create-order/', views.CreateOrderView.as_view(), name='create_order'),
]