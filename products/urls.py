from django.urls import path
from .views import CartView
from .views import (
    DlyaTelaView, DlyaVolosView, ParfumView, AboutView, AromatiView,
    ProductListView, ProductDetailView,
    cart_add, cart_remove, cart_detail,
)

urlpatterns = [
    path('dlya-tela/',  DlyaTelaView.as_view(),   name='dlya_tela'),
    path('dlya-volos/', DlyaVolosView.as_view(),  name='dlya_volos'),
    path('parfum/',     ParfumView.as_view(),     name='parfum'),
    path('aromati/',    AromatiView.as_view(),      name='aromati'),
    path('about/',      AboutView.as_view(),      name='about'),
    path('cart/', CartView.as_view(), name='cart'),

    path('',            ProductListView.as_view(),   name='product_list'),
    path('<int:pk>/',   ProductDetailView.as_view(), name='product_detail'),

    path('api/cart/add/',    cart_add,    name='cart_add'),
    path('api/cart/remove/', cart_remove, name='cart_remove'),
    path('api/cart/',        cart_detail, name='cart_detail'),
]
