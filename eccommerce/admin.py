from django.contrib import admin

from eccommerce.models import BillingAddress, Order, OrderItem, Product

# Register your models here.
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(BillingAddress)