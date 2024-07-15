from django.urls import path
from .views import *

urlpatterns = [
    path("products/",ProductList.as_view(),name = 'products'),
    path("order-summary/",OrderSummary.as_view(),name = "order-summary"),
    path("product/<slug>/",ProductDetail.as_view(),name = 'product'),
    path("add-to-cart/<slug>",add_to_cart, name="add-to-cart"),
    path("remove-from-cart/<slug>",remove_from_cart, name="remove-from-cart"),
    path("remove-item-from-cart/<slug>",remove_item_from_cart, name="remove-item-from-cart"),
    path("checkout/",CheckoutView.as_view(),name = 'checkout'),
    path("payment/<payment_option>/",PaymentView.as_view(),name = "payment"),
    path('search/', search_feature, name='search'),
    
]