from django.urls import path
from .views import *

urlpatterns = [
    
    path("productslist/",ProductListView.as_view(),name = 'productsapi'),
    path("product/<slug>/",ProductDetailView.as_view(),name = 'product-detail'),

    path("customers/",UserListView.as_view(),name = 'customers'),
    path("customer-detail/<int:pk>/",UserDetailView.as_view(),name = 'customers-detail'),
    
]