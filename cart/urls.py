from django.contrib import admin
from django.urls import path
from .views import *
app_name='cart'

urlpatterns = [
    path('add-to-cart/<slug>',add_to_cart,name='add-to-cart'),
    path('my_cart',CartView.as_view(),name='my_cart'),
    path('delete_cart/<slug>',delete_cart,name='delete_cart'),
    path('add/<slug>',add,name='add'),
    path('subtract/<slug>',subtract,name='subtract'),
    path('my_wishlist/',WishlistView.as_view(),name='my_wishlist'),
    path('add-wish-list/<slug>',add_wish_list,name='add-wish-list'),
    path('delete_wishlist/<slug>',delete_wishlist,name='delete_wishlist'),
    path('add_wish/<slug>',add_wish,name='add_wish'),
    path('subtract_wish/<slug>',subtract_wish,name='subtract_wish'),

]