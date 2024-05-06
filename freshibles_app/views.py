from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import login as auth_login, authenticate
from .forms import CustomUserCreationForm, EmailAuthenticationForm, QuickPasswordResetForm
from django.db.models import Q

from django.http import HttpResponseRedirect, JsonResponse
from .models import Product, Cart,CartItem, Newsletter, Message
import random
from decimal import Decimal

def home(request):
    categories = Product.CATEGORY_CHOICES
    products_by_category = {}

    for category in categories:
        category_name = category[0]
        products_by_category[category_name] = Product.objects.filter(category=category_name)

    # Fetching random products for the carousel
    all_products = list(Product.objects.all())
    random_products = random.sample(all_products, min(len(all_products), 5))  # Get 5 random products

    context = {
        'products_by_category': products_by_category,
        'carousel_items': random_products,
    }
    return render(request, 'index.html', context)



def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            validate_email(email)
            Newsletter.objects.create(email=email)
            messages.success(request, 'Thank you for subscribing!')
        except ValidationError:
           messages.error(request, 'Invalid email address.')
        except Exception as e:
            messages.error(request, 'An error occurred: ' + str(e))
    return redirect('home')

def add_to_cart(request, product_id):
    if not(request.user.is_authenticated):
        messages.success(request=request,message="You need to sign in first")
        return redirect('login')
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user, defaults={'user': request.user})

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'product': product, 'cart': cart})
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'home'))
def about(request):
    return render(request, 'about.html')

def shop(request):
    # search_query = request.GET.get('search', '')
    # if search_query:
    #     products = Product.objects.filter(product_name__icontains=search_query)
    # else:
    products = Product.objects.all()
    print
    context = {
        'products': products,
        #'search_query': search_query
    }
    print("Hello Product")
    return render(request, 'shop.html', context)

def services(request):
    return render(request, 'services.html')

def contact(request):
    return render(request, 'contact.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(request, username=user.username, password=request.POST['password1'])  # Assuming username and password fields are used
            if user:
                auth_login(request, user)
                return redirect('home')  # Redirect to a post-login page
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form}) 
def login(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Email or password is incorrect")
    else:
        form = EmailAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def quick_password_reset(request):
    if request.method == 'POST':
        form = QuickPasswordResetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))  # Redirect to login after reset
    else:
        form = QuickPasswordResetForm()
    return render(request, 'password_reset.html', {'form': form})


def cart(request):
    if not(request.user.is_authenticated):
        messages.success(request=request,message="You need to sign in first")
        return redirect('login')
    try:
        cart = Cart.objects.get(user=request.user)
        items = cart.items.all()
        subtotal = sum(item.get_total_item_price() for item in items)
        total_price = cart.get_total_price()
        shipping_cost = Decimal('3.00')  # Convert float to Decimal for consistency
        total = subtotal + shipping_cost
    except Cart.DoesNotExist:
        items = []
        subtotal = Decimal('0.00')  # Initialize as Decimal
        total = Decimal('0.00')  # Initialize as Decimal
        shipping_cost = Decimal('0.00')  # Initialize as Decimal

    context = {
        'cart_items': items,
        'subtotal': subtotal,
        'total': total,
        'shipping_cost': shipping_cost,
        'total_price': total_price
    }
    return render(request, 'cart.html', context)


def product_search(request):
    query = request.GET.get('query', '')  # Get the query from GET request
    if query:
        products = Product.objects.filter(
            Q(product_name__icontains=query) |
            Q(product_description__icontains=query) |
            Q(category__icontains=query) |
            Q(product_price__icontains=query)
        )
    else:
        products = Product.objects.all()

    return render(request, 'search_results.html', {'products': products})


def update_cart_item(request, item_id, action):
    if not(request.user.is_authenticated):
        messages.success(request=request,message="You need to sign in first")
        return redirect('login')
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        if action == 'inc':
            cart_item.quantity += 1
        elif action == 'dec' and cart_item.quantity > 1:
            cart_item.quantity -= 1
        cart_item.save()
        return JsonResponse({
            'status': 'success',
            'quantity': cart_item.quantity,
            'total_price': cart_item.get_total_item_price()
        })


def delete_cart_item(request, item_id):
    if not(request.user.is_authenticated):
        messages.success(request=request,message="You need to sign in first")
        return redirect('login')
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.delete()
        return JsonResponse({'status': 'success', 'message': 'Item deleted successfully'})

def submit_message(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_body = request.POST.get('message_body')

        # Save the message to the database
        Message.objects.create(name=name, email=email, message_body=message_body)
        messages.success(request, f'Thank you for your message. {name} ! We will get back to you soon.')
        return redirect('contact')  # Assuming 'contact' is the name of the URL where the contact form lives
    else:
        return render(request, 'contact.html')