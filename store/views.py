from calendar import c
from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
import json
import datetime
from decimal import Decimal
from .utils import cartData, cookieCart, guestOrder
from django.contrib.auth import login
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse


@csrf_protect
def registerUser(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')

            messages.success(
                request, 'Account created successfully for ' + user)

            new_user = User.objects.get(username=user)
            Customer.objects.create(user=new_user,
                                    name=new_user.username,
                                    email=new_user.email)
            print("Successfuly registered")

            return redirect('login')
    context = {'form': form}
    return render(request, 'register.html', context)


@csrf_protect
def loginUser(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.info(
                request, 'Username or password is incorrect, Please Try Again!')

    context = {}
    return render(request, 'login.html', context)


@csrf_protect
def logoutUser(request):
    logout(request)
    return redirect('store')


def store(request):

    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all().order_by('created_at')
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 9)

    categories = Categories.objects.all()

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {'products': products,
               'cartItems': cartItems, 'categories': categories}

    return render(request, 'store.html', context)


def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'cart.html', context)


def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'checkout.html', context)


def updateItem(request):

    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer

    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added!', safe=False)


def processOrder(request):

    transaction_id = datetime.datetime.now().timestamp()

    data = json.loads(request.body)

    if request.user.is_authenticated:

        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

    try:
        email_template = render_to_string('email.html',
                                          {"name": customer.name,
                                           "product": product.name})
        send = EmailMultiAlternatives(
            "Thank you for your Order",
            "Order Confirmation From HantaStore",
            settings.EMAIL_HOST_USER,
            [customer.email],
        )
        send.attach_alternative(email_template, 'text/html')
        send.send()
    except Exception as e:
        print(str(e))

    else:
        cutomer, order = guestOrder(request, data)

    total = Decimal(data['form']['total'])
    order.transaction_id = transaction_id

    # if total == order.get_cart_total:
    order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            country=data['shipping']['country'],
            zip_code=data['shipping']['zip_code'],
        )

    return JsonResponse('Payment Complete!', safe=False)


def ProductView(request, pk):
    product = Product.objects.get(pk=pk)

    data = cartData(request)
    cartItems = data['cartItems']

    context = {'product': product, 'cartItems': cartItems}
    return render(request, 'view.html', context)


def search(request):

    data = cartData(request)
    cartItems = data['cartItems']

    q = request.GET['q']
    products = Product.objects.filter(name__icontains=q).order_by('created_at')

    page = request.GET.get('page', 1)
    paginator = Paginator(products, 9)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {'products': products, 'cartItems': cartItems}

    return render(request, 'search.html', context)


def categoryFilter(request, pk):

    product_category = Categories.objects.get(pk=pk)

    products = Product.objects.filter(
        product_category=product_category).order_by('created_at')

    data = cartData(request)
    cartItems = data['cartItems']

    categories = Categories.objects.all()

    page = request.GET.get('page', 1)
    paginator = Paginator(products, 9)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {'products': products,
               'cartItems': cartItems, 'categories': categories, 'FilterCat': product_category}

    return render(request, 'category.html', context)


def ratingsFilter(request, num):

    product_rating = num
    products = Product.objects.filter(
        avg_rating=num).order_by('created_at')

    product_first = products.first()

    data = cartData(request)
    cartItems = data['cartItems']

    categories = Categories.objects.all()

    page = request.GET.get('page', 1)
    paginator = Paginator(products, 9)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {'products': products,
               'cartItems': cartItems,
               'categories': categories,
               "product_first": product_first}

    return render(request, 'ratings.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email_address'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, 'po0janhunt@gmail.com',
                          ['po0janhunt@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("store")

    form = ContactForm()
    return render(request, "contact.html", {'form': form})


def about(request):
    context = {}
    return render(request, 'about.html', context)
