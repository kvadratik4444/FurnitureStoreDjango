from users import views
from django.urls import path

app_name = 'users'

urlpatterns = [
    path('login/', views.UserListView.as_view(), name='login'),
    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('logout/', views.logout, name='logout'),
    path('users-basket/', views.UserBasketVies.as_view(), name='users_basket'),
]
