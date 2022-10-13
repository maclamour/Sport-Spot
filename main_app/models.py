
from distutils.command.upload import upload
from itertools import product
from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class Customer(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE,null=True, blank=True) 
    name = models.CharField(max_length=255,null=True)
    email = models.EmailField(unique=True)
    

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255,null=True)
    img = models.ImageField(upload_to='images/')
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @property
    def imgUrl(self):
        try:
            url=self.img.url
        except:
            url=''
        return url    
        
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,blank=True, null=True)
    order_date = models.DateField(auto_now_add=True)
    complated_order = models.BooleanField(default=False)
    order_id = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.id

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,null=True,blank=True)
    quantity = models.IntegerField(default=0, null=True,blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product.name




