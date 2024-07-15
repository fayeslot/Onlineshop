from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render,redirect,get_object_or_404
from django.utils import timezone
from django.views.generic import ListView,DetailView,View
from eccommerce.forms import CheckoutForm
from eccommerce.models import Order, OrderItem, Product, BillingAddress

# Create your views here.

class ProductList(ListView):
    model = Product
    template_name = "eccomerce/Home.html"

class ProductDetail(DetailView):
    model = Product
    template_name = "eccomerce/product.html"

@login_required
def add_to_cart(request,slug):
    product = get_object_or_404(Product,slug=slug)
    order_item, created = OrderItem.objects.get_or_create(product=product,user = request.user, ordered=False)
    order_qs = Order.objects.filter(user = request.user,ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.product.filter(product__slug=product.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request,"Item quantity was updated")
            return redirect("product")
        else:
            messages.info(request,"Item was added to your cart")
            order.product.add(order_item)
            return redirect("product",slug=slug)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user = request.user,ordered_date=ordered_date)
        order.product.add(order_item)
        messages.info(request,"Item was added to your cart")
    return redirect("product",slug=slug)

@login_required
def remove_from_cart(request,slug):
    product = get_object_or_404(Product,slug=slug)
    
    order_qs = Order.objects.filter(user = request.user,ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.product.filter(product__slug=product.slug).exists():
            order_item = OrderItem.objects.filter(product=product,user = request.user,ordered=False)[0]
            order.product.remove(order_item)
            messages.info(request,"Item was removed from your cart")
            return redirect("order-summary")
        else:
            messages.info(request,"Item was not in your cart")
            return redirect("product",slug=slug)

    else:
        messages.info(request,"You do not have an active order")
    return redirect("product",slug=slug)

@login_required
def remove_item_from_cart(request,slug):
    product = get_object_or_404(Product,slug=slug)
    order_qs = Order.objects.filter(user=request.user,ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.product.filter(item__slug=product.slug).exists():
            order_item = OrderItem.objects.filter(product=product,user = request.user,ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.product.remove(order_item)
            messages.info(request,"Item quantity was updated")
            return redirect("order-summary")
        else:
            messages.info(request,"Item was not in your cart")
            return redirect("product",slug=slug)
    else:
        messages.info(request,"You do not have an active order")
        return redirect("product",slug=slug)


class OrderSummary(LoginRequiredMixin,View):
    def get(self, request):
        try:
            order = get_object_or_404(Order, user=self.request.user, ordered=False)
        except ObjectDoesNotExist:
            messages.info(self.request,"You do not have an active order")
            return render(self.request, 'eccomerce/order_summary.html')
        context = {'order': order}
        return render(self.request, 'eccomerce/order_summary.html', context)
    
class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            form = CheckoutForm()
            order = Order.objects.get(user=self.request.user)
            context = {'form':form, 'order': order}
            return render(self.request,"eccomerce/Checkout.HTML",context)
        except ObjectDoesNotExist:
            messages.info(self.request,'You do not have an active order')
            return redirect("checkout")
    
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)

        try:
            order = get_object_or_404(Order, user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                same_billing_address = form.cleaned_data.get('same_billing_address')
                save_info = form.cleaned_data.get('save_info ')
                payment_option = form.cleaned_data.get('payment_option')

                billing_address = BillingAddress(user = self.request.user,street_address = street_address,apartment_address = apartment_address,
                                                country = country,zip = zip,same_billing_address = same_billing_address,save_info = save_info,payment_option = payment_option)
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                return redirect("checkout")
            messages.warning(self.request,"Failed checkout")
            return render(self.request,"eccomerce/Checkout.html")
            # Do something with the form data
            
        except ObjectDoesNotExist:
            messages.info(self.request,"You do not have an active order")
            return redirect('order_summary')
        
class PaymentView(View):
    def get():
        return render("eccomerce/payment.html")

def search_feature(request):
    if request.method == 'POST':
        # Retrieve the search query entered by the user
        search_query = request.POST['search_query']
        # Filter your model by the search query
        if search_query:
            posts = Product.objects.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
        else:
            messages.info(request,"Please enter a search query")

        return render(request, 'eccomerce/searchpost.html', {'query':search_query, 'posts':posts})
    else:
        return render(request, 'eccomerce/searchpost.html',{})
        