from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, null=True)
    img = models.ImageField(upload_to='media/images')  # Updated upload_to path
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def img_url(self):
        return self.img.url if self.img else ''

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order_date = models.DateField(auto_now_add=True)
    completed_order = models.BooleanField(default=False)
    order_id = models.CharField(max_length=105, null=True)
    name = models.CharField(max_length=255, null=True)  # Add this field
    email = models.EmailField(null=True)  # Add this field
    address = models.TextField(null=True)  # Add this field

    def __str__(self):
        return str(self.id)



class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def total_price(self):
        return self.quantity * self.product.price


class CartManager(models.Manager):
    def get_cart_for_user(self, user):
        return self.get(user=user)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_items = models.ManyToManyField('OrderItem', related_name='carts')

    # Define a custom manager
    objects = CartManager()

    def __str__(self):
        return f"Cart for {self.user.username}"

    def total_price(self):
        return sum(item.total_price() for item in self.order_items.all())
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    # Add any additional fields you need, e.g., selected options or custom fields

    def __str__(self):
        return f"CartItem for {self.product.name}"

    def total_price(self):
        return self.product.price * self.quantity