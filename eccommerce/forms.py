from django import forms 
from django_countries.fields import CountryField 
from django_countries.widgets import CountrySelectWidget 

PAYMENT_CHOICES  = (
    ('S','Stripe'),
    ('p','Paypal'),
)

class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'1234 Main St'}))
    apartment_address = forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder':'Apartment or suite'}))
    country = CountryField(blank_label = '(select country)').formfield(widget=CountrySelectWidget(attrs={'class':'col-lg-4 col-md-12 mb-4'}))
    zip = forms.CharField(widget=forms.TextInput(attrs={'class':'col-lg-4 col-md-12 mb-4'}))
    same_shipping_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
