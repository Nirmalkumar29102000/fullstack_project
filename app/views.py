from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password


from .models import *


def base(request):
    return render(request,'base.html')


def register(request):

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        role = request.POST.get("role")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(
                request,
                "register.html",
                {"error": "Passwords do not match"}
            )


        if User.objects.filter(email=email).exists():
            return render(
                request,
                "register.html",
                {"error": "Email already registered"}
            )

        User.objects.create(
            username=username,
            email=email,
            phone_number=phone_number,
            address=address,
            role=role,
            password=make_password(password)
        )

        return redirect("/login")

    return render(request, "register.html")

def login(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)

            if check_password(password, user.password):

                # Save session data
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                request.session['role'] = user.role


                if user.role == 'customer':
                    return redirect('/customer_dashboard')

                elif user.role == 'owner':
                    return redirect('/owner_dashboard')

                elif user.role == 'delivery':
                    return redirect('/delivery_dashboard')

            else:
                return render(
                    request,
                    'login.html',
                    {'error': 'Invalid Password'}
                )

        except User.DoesNotExist:
            return render(
                request,
                'login.html',
                {'error': 'Email does not exist'}
            )

    return render(request, 'login.html')


def customer_dashboard(request):

    customer_id = request.session.get('user_id')
    
    if not customer_id:
        messages.warning(request, "Please login to access the Customer Dashboard.")
        return redirect("login")

    customer = User.objects.get(
        id=customer_id
    )

    restaurants = Restaurant.objects.all()

    return render(
        request,
        "customer_dashboard.html",
        {
            'restaurants': restaurants,
            'customer': customer
        }
    )
    
def owner_dashboard(request):
    return render(request, "owner_dashboard.html")

def delivery_dashboard(request):

    orders = Order.objects.filter(
        status='Accepted'
    )

    return render(
        request,
        'delivery_dashboard.html',
        {'orders': orders}
    )

def add_restaurant(request):

    if request.method == "POST":

        owner_id = request.session.get('user_id')

        owner = User.objects.get(id=owner_id)

        Restaurant.objects.create(

            owner=owner,

            restaurant_name=request.POST.get(
                'restaurant_name'
            ),

            address=request.POST.get(
                'address'
            ),

            phone_number=request.POST.get(
                'phone_number'
            ),

            image=request.FILES.get(
                'image'
            )

        )

        return redirect('/owner_dashboard')

    return render(request,'add_restaurant.html')

def view_restaurant(request):

    owner_id = request.session.get('user_id')

    restaurants = Restaurant.objects.filter(
        owner_id=owner_id
    )

    return render(
        request,
        'view_restaurant.html',
        {'restaurants': restaurants}
    )   



def add_food(request, restaurant_id):

    restaurant = Restaurant.objects.get(
        id=restaurant_id
    )

    if request.method == "POST":

        FoodItem.objects.create(
            restaurant=restaurant,
            food_name=request.POST.get('food_name'),
            description=request.POST.get('description'),
            price=request.POST.get('price'),
            image=request.FILES.get('image'),
            is_available='is_available' in request.POST
        )

        return redirect('view_restaurant')

    return render(
        request,
        'add_food.html',
        {'restaurant': restaurant}
    )

def view_food(request, restaurant_id):

    restaurant = Restaurant.objects.get(
        id=restaurant_id
    )

    foods = FoodItem.objects.filter(
        restaurant=restaurant
    )

    return render(
        request,
        'view_food.html',
        {
            'restaurant': restaurant,
            'foods': foods
        }
    )

def edit_food(request, id):

    food = FoodItem.objects.get(id=id)

    if request.method == "POST":

        food.food_name = request.POST.get(
            'food_name'
        )

        food.description = request.POST.get(
            'description'
        )

        food.price = request.POST.get(
            'price'
        )

        if request.FILES.get('image'):
            food.image = request.FILES.get(
                'image'
            )

        food.is_available = (
            'is_available' in request.POST
        )

        food.save()

        return redirect(
            'view_food',
            restaurant_id=food.restaurant.id
        )

    return render(
        request,
        'edit_food.html',
        {'food': food}
    )

def delete_food(request, id):

    food = FoodItem.objects.get(id=id)

    restaurant_id = food.restaurant.id

    food.delete()

    return redirect(
        'view_food',
        restaurant_id=restaurant_id
    )

def view_menu(request, restaurant_id):

    restaurant = Restaurant.objects.get(
        id=restaurant_id
    )

    foods = FoodItem.objects.filter(
        restaurant=restaurant,
        is_available=True
    )

    return render(
        request,
        'view_menu.html',
        {
            'restaurant': restaurant,
            'foods': foods
        }
    )

def add_to_cart(request, food_id):

    customer_id = request.session.get('user_id')

    customer = User.objects.get(
        id=customer_id
    )

    food = FoodItem.objects.get(
        id=food_id
    )

    quantity = int(
        request.POST.get('quantity')
    )

    cart, created = Cart.objects.get_or_create(
        customer=customer
    )

    CartItem.objects.create(
        cart=cart,
        food=food,
        quantity=quantity
    )

    return redirect(
        'view_menu',
        restaurant_id=food.restaurant.id
    )

def view_cart(request):

    customer_id = request.session.get(
        'user_id'
    )

    customer = User.objects.get(
        id=customer_id
    )

    cart = Cart.objects.get(
        customer=customer
    )

    cart_items = CartItem.objects.filter(
        cart=cart
    )

    grand_total = 0

    for item in cart_items:

        grand_total += (
            item.food.price *
            item.quantity
        )

    return render(
        request,
        'view_cart.html',
        {
            'cart_items': cart_items,
            'grand_total': grand_total
        }
    )

def place_order(request):

    customer_id = request.session.get(
        'user_id'
    )

    customer = User.objects.get(
        id=customer_id
    )

    cart = Cart.objects.get(
        customer=customer
    )

    cart_items = CartItem.objects.filter(
        cart=cart
    )

    total_amount = 0

    for item in cart_items:

        total_amount += (
            item.food.price *
            item.quantity
        )

    payment_method = request.POST.get(
    'payment_method'
    )
    
    order = Order.objects.create(
        customer=customer,
        total_amount=total_amount,
        payment_method=payment_method
        )

    for item in cart_items:

        OrderItem.objects.create(
            order=order,
            food=item.food,
            quantity=item.quantity,
            price=item.food.price
        )

    cart_items.delete()

    return redirect('my_orders')

def my_orders(request):

    customer_id = request.session.get(
        'user_id'
    )

    orders = Order.objects.filter(
        customer_id=customer_id
    ).order_by('-id')

    return render(
        request,
        'my_orders.html',
        {'orders': orders}
    )

def owner_orders(request):

    orders = Order.objects.all().order_by(
        '-created_at'
    )

    return render(
        request,
        'owner_orders.html',
        {'orders': orders}
    )

def accept_order(request, id):

    order = Order.objects.get(
        id=id
    )

    order.status = 'Accepted'

    order.save()

    return redirect(
        'owner_orders'
    )

def deliver_order(request, id):

    order = Order.objects.get(
        id=id
    )

    order.status = 'Delivered'

    order.save()

    return redirect(
        'delivery_dashboard'
    )

def payment_page(request):

    customer_id = request.session.get('user_id')

    customer = User.objects.get(
        id=customer_id
    )

    cart = Cart.objects.get(
        customer=customer
    )

    cart_items = CartItem.objects.filter(
        cart=cart
    )

    grand_total = 0

    for item in cart_items:

        grand_total += (
            item.food.price *
            item.quantity
        )

    return render(
        request,
        'payment_page.html',
        {
            'grand_total': grand_total
        }
    )

def logout(request):
    request.session.flush()   # Removes all session data
    return redirect('login')