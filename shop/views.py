from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Product, CATEGORY_CHOICES, Profile, Order, Cart, Product_Request, Received_Order
SERVICE_CHARGE = 25.00


def checkAccountType(request):
    account_type = []
    if request.user.is_authenticated == True:
        user_profile = Profile.objects.filter(user=request.user)
        account_type = user_profile[0].account_type
    return account_type


def getAddress(request):
    string_address = ''
    if request.user.is_authenticated == True:
        user_profile = Profile.objects.filter(user=request.user)
        string_address = string_address + user_profile[0].address_line_1 + '\n'
        string_address = string_address + user_profile[0].address_line_2 + '\n'
        string_address = string_address + user_profile[0].city + '\n'
        string_address = string_address + user_profile[0].state + '\n'
        string_address = string_address + str(user_profile[0].zip_code)
    return string_address


def getCartItems(request):
    context = {}
    if Cart.objects.exists:
        cart_items = Cart.objects.filter(user=request.user, ordered=False)
        if cart_items.__len__() > 0:
            order_items = cart_items[0].items.all()
            total_amount = round(cart_items[0].get_total_amount(), 2)
            billed_amount = round(cart_items[0].get_billed_amount(), 2)
            total_saving = round(cart_items[0].get_total_savings(), 2)

            context = {
                'order_items': order_items,
                'total_amount': total_amount,
                'total_saving': total_saving,
                'billed_amount': billed_amount,
                'service_charge': SERVICE_CHARGE
            }
    return context


def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order, created = Order.objects.get_or_create(
        product=product, user=request.user, ordered=False)
    cart_query_set = Cart.objects.filter(user=request.user, ordered=False)
    if cart_query_set.exists():
        cart = cart_query_set[0]
        if cart.items.filter(product__slug=product.slug).exists():
            order.quantity += 1
            order.save()
            messages.success(request, "This item quantity was updated.")
        else:
            cart.items.add(order)
            messages.success(
                request, "This item quantity was addded to the cart.")

    else:
        ordered_date = timezone.now()
        cart = Cart.objects.create(
            user=request.user, ordered_date=ordered_date)
        cart.items.add(order)
        messages.success(request, "This item quantity was addded to the cart.")
    return redirect("Cart")


def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart_query_set = Cart.objects.filter(user=request.user, ordered=False)
    cart = cart_query_set[0]
    if cart.items.filter(product__slug=product.slug).exists():
        order = Order.objects.filter(
            product=product, user=request.user, ordered=False)[0]
        cart.items.remove(order)
        order.delete()
        messages.success(request, "This item  was removed from the cart.")

    return redirect('Cart')


def remove_single_item_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart_query_set = Cart.objects.filter(user=request.user, ordered=False)
    if cart_query_set.exists():
        cart = cart_query_set[0]
        if cart.items.filter(product__slug=product.slug).exists():
            order = Order.objects.filter(
                product=product, user=request.user, ordered=False)[0]
            order.quantity -= 1
            order.save()
            if order.quantity == 0:
                cart.items.remove(order)
                order.delete()
                messages.success(request, "This item was removed.")
                return redirect('Cart')

            messages.success(request, "This item quantity was updated.")
            return redirect('Cart')

        return redirect('Cart')


def add_single_item_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart_query_set = Cart.objects.filter(user=request.user, ordered=False)
    if cart_query_set.exists():
        cart = cart_query_set[0]
        if cart.items.filter(product__slug=product.slug).exists():
            order = Order.objects.filter(
                product=product, user=request.user, ordered=False)[0]
            order.quantity += 1
            order.save()
            messages.success(request, "This item quantity was updated.")
            return redirect('Cart')

        return redirect('Cart')


def index(request):
    if request.method == 'POST':
        login_email = request.POST.get('login-email')
        login_password = request.POST.get('login-password')
        user = authenticate(username=login_email, password=login_password)

        if user is not None:
            login(request, user)
            return redirect('Home')
        else:
            messages.error(request=request,
                           message="Invalid Credentials! Please try again.")
            return redirect('Login')

    return render(request, 'index.html')


def registration(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        # email - logic goes here!!####################
        account_type = request.POST.get('account-type')
        password = request.POST.get('password')
        re_password = request.POST.get('re-password')

        if password != re_password:
            messages.error(
                request=request, message="Passwords didn't match! Login to access the website.")
            return redirect('Registration')
        else:

            user = User.objects.create_user(username=email, email=email, password=password,
                                            first_name=fname, last_name=lname)
            user.save()

            user_profile = Profile.objects.create(user=user)
            user_profile.account_type = account_type
            user_profile.save()

            messages.success(
                request=request, message="Successfully Registered!")
            return redirect('Login')

    return render(request, 'registration.html')


def home(request):
    all_products = []
    for category in CATEGORY_CHOICES:
        product = Product.objects.filter(category=category[0])[:10]
        all_products.append([product, category[1]])

    account_type = checkAccountType(request)

    context = {
        'all_products': all_products,
        'account_type': account_type
    }

    return render(request, 'home.html', context)


def search(request):
    query = request.GET.get('query')

    if len(query) > 70:
        products = []
    else:
        words = query.split()
        products = Product.objects.filter(product_name__icontains=query)
        for word in words:
            product = Product.objects.filter(product_name__icontains=word)
            products = products.union(product)

        if products.__len__() < 1:
            for category_items in CATEGORY_CHOICES:
                category = category_items[1].lower()
                if category == query.lower():
                    product = Product.objects.filter(
                        category=category_items[0])
                    products = products.union(product)

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    account_type = checkAccountType(request)

    context = {
        'page_obj': page_obj,
        'query': query,
        'account_type': account_type
    }
    return render(request, 'search.html', context=context)


def track_order(request):
    total_amount = 0
    items = 0
    receiving_time = 0
    delivered = True
    if request.user.is_authenticated == True:
        received_order = Received_Order.objects.filter(user=request.user)
        if received_order.__len__() > 0:
            length = received_order.__len__()
            total_amount = received_order[length-1].total_amount
            items = received_order[length-1].items
            receiving_time = received_order[length-1].receiving_time
            delivered = received_order[length-1].delivered
        context = {
            'total_amount': total_amount,
            'items': items,
            'receiving_time': receiving_time,
            'delivered': delivered
        }
    return render(request, 'track-order.html', context=context)


def cart(request):
    if request.user.is_authenticated == True:
        context = getCartItems(request=request)
        if context.__len__ == 0:
            return render(request, 'cart.html')
    else:
        return render(request, 'cart.html')
    return render(request, 'cart.html', context=context)


def product(request, slug):
    product = Product.objects.filter(slug=slug)
    other_products = Product.objects.filter(
        category=product[0].category).exclude(slug=slug)[:4]

    account_type = checkAccountType(request)

    if account_type == 'P':
        you_save = round(product[0].mrp - product[0].consumer_price, 2)
    else:
        you_save = round(product[0].mrp - product[0].wholesaler_price, 2)

    context = {
        'product': product[0],
        'other_products': other_products,
        'account_type': account_type,
        'you_save': you_save
    }
    return render(request, 'product-view.html', context)


def product_list(request, category):
    products = None
    for category_items in CATEGORY_CHOICES:
        if category_items[1] == category:
            products = Product.objects.filter(category=category_items[0])
            category = category_items[1]

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    account_type = checkAccountType(request)

    context = {
        'page_obj': page_obj,
        'category': category,
        'account_type': account_type
    }
    return render(request, 'product-list.html', context)


def about(request):
    return render(request, 'about-us.html')


def address(request):
    if request.method == 'POST':
        add1 = request.POST.get('address-line-1').strip()
        add2 = request.POST.get('address-line-2').strip()
        city = request.POST.get('city').strip()
        state = request.POST.get('state').strip()
        zipcode = request.POST.get('zip').strip()
        if request.user.is_authenticated == True:
            user_profile = Profile.objects.get(user=request.user)
            user_profile.address_line_1 = add1
            user_profile.address_line_2 = add2
            user_profile.city = city
            user_profile.state = state
            user_profile.zip_code = zipcode
            user_profile.save()
            messages.success(
                request=request, message="Information Updated Successfully!")
            return redirect('Checkout')
    return render(request, 'address.html')


def checkout(request):
    if request.method == 'POST':
        user_profile = Profile.objects.filter(user=request.user)
        cart_desc = getCartItems(request)
        total_amount = cart_desc.get('total_amount')
        items = cart_desc.get('order_items')
        string_item = ''
        for item in items:
            string_item = string_item + str(item) + ',\n'

        string_address = getAddress(request)

        received_order = Received_Order.objects.create(
            user=request.user, items=string_item, total_amount=total_amount, address=string_address, receiving_time=timezone.now(), delivered=False)
        received_order.save()
        cart = Cart.objects.get(user=request.user, ordered=False)
        cart.delete()
        # email - logic goes here!!####################
        messages.success(request=request, message="Order Placed Successfully!")
        return redirect('Home')
    else:
        context = {}
        if request.user.is_authenticated == True:
            user_profile = Profile.objects.filter(user=request.user)
            cart_desc = getCartItems(request)
            total_amount = cart_desc.get('total_amount')
            items = cart_desc.get('order_items')
            print(items)
            order_items = cart_desc.get('order_items').__len__()
            if order_items == 0:
                return redirect('Cart')
            if user_profile[0].zip_code != 1:
                context = {
                    'user_profile': user_profile[0],
                    'order_items': order_items,
                    'total_amount': total_amount
                }
        return render(request, 'checkout.html', context=context)


def request_product(request):
    if request.method == 'POST':
        product_request = request.POST.get('product_request').strip()
        if request.user.is_authenticated == True:
            new_request = Product_Request.objects.create(
                user=request.user, request=product_request, product_request_time=timezone.now())
            new_request.save()

        # email - logic goes here!!####################
        messages.success(
            request=request, message="Product request was sent successfully!")
        return redirect('Home')

    return render(request, 'request-product.html')


@login_required
def logout(request):
    django_logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('Login')
    return HttpResponse('Logout!')
