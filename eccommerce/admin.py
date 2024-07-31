from django.contrib import admin

from eccommerce.models import BillingAddress, Order, OrderItem, Product

# Register your models here.
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','price','discount_price','category','image']
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(BillingAddress)