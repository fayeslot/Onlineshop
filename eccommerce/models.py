from django.db import models
from django_countries.fields import CountryField 
from django.shortcuts import reverse
from django.contrib.auth.models import User

CATEGORY_CHOICES = (
    ('A', 'All'),
    ('S', 'Shoes'),
    ('E', 'Electronics'),
    ('B','Bags'),
    ('C','Clothes')
)

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='item_images/',blank=True,null=True)
    price = models.FloatField()
    discount_price = models.FloatField(blank="True", null="True")
    category = models.CharField(choices = CATEGORY_CHOICES,max_length=2,blank=True,null=True)
    slug = models.SlugField()
    description = models.TextField()
    

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse ("product",kwargs={
            'slug':self.slug
        })
    
    def get_add_to_cart_url(self):
        return reverse("add-to-cart",kwargs={
            'slug':self.slug
        })
    
    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart",kwargs={
            'slug':self.slug
        })
    def get_remove_item_from_cart_url(self):
        return reverse("remove-item-from-cart",kwargs={
            'slug':self.slug
        })
    
class OrderItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity}  {self.product.title}"
    
    def get_total_item_price(self):
        return self.quantity * self.product.price

    def get_total_discount_price(self):
        return self.quantity * self.product.discount_price
    
    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_discount_price() 
        return self.get_total_item_price() 
    
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress',on_delete=models.SET_NULL,blank=True,null=True)
    payment = models.ForeignKey('Payment',on_delete=models.SET_NULL,blank=True,null=True)


    def __str__(self):
        return self.user.username
    
    def get_total(self):
        total = 0
        for order_item in self.product.all():
            total += order_item.get_final_price()
        return total
            
class BillingAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
    
class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

