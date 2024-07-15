from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required 
from django.shortcuts import render,redirect
from eccommerce.forms import  SignupForm

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('account-login')
    else:
        form = SignupForm()
    return render(request,'accounts/signup.html',{'form':form})

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')

        user = authenticate(username=username,password=password)

        if user != None:
            login(request,user)
            return redirect('products')
        
        else:
            messages.error(request,"Invalid username or Password")
            return redirect("account-login")

        
    return render(request, "accounts/signin.html")

@login_required
def signout(request):
    logout(request)
    messages.success(request,"You have been logged out")
    return redirect("account-login")

