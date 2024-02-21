from django.shortcuts import render, redirect
from product.models import Product 
from .forms import SignUpForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

def index(request):
    products = Product.objects.all()[0:3]
    return render(request, 'core/home.html', {'products': products})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()

    return render(request, 'core/signup.html', {'form': form})

def shop(request):
    products = Product.objects.all()
    return render(request, 'core/shop.html', {'products': products})

@login_required
def account(request):
    return render(request, 'core/account.html')

@login_required
def edit_account(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name =  request.POST.get('last_name')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()

        return redirect('account')
    return render(request, 'core/edit_account.html')

    