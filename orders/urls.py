from orders import views
from django.urls import path

app_name = 'orders'

urlpatterns = [
    path('create-order/', views.create_order, name='create_order'),
]