from django.db import models

class User(models.Model):

    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('owner', 'Owner'),
        ('delivery', 'Delivery'),
    ]

    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20,choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.username

class Restaurant(models.Model):

    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to='restaurants/')

    def __str__(self):
        return self.restaurant_name

class FoodItem(models.Model):

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE
    )

    food_name = models.CharField(max_length=100)

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    image = models.ImageField(
        upload_to='food_items/'
    )

    is_available = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.food_name

class Cart(models.Model):

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE
    )

    food = models.ForeignKey(
        FoodItem,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

class Order(models.Model):

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    payment_method = models.CharField(
        max_length=50,
        default='Cash On Delivery'
    )

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )

    food = models.ForeignKey(
        FoodItem,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )