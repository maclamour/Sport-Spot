
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
    img = models.ImageField(null=True,blank=True)
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
        
