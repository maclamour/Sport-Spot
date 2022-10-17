from audioop import reverse

from urllib.request import Request
from django.shortcuts import render,redirect
from django.views import View # <- View class to handle requests
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from .models import Product, Order
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.models import User





# Create your views here.

# Here we will be creating a class called Home and extending it from the View class
class Home(TemplateView):
    template_name = "home.html"



class StoreList(TemplateView):
    template_name = "store_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")

        if name != None:
            context["products"] = Product.objects.filter(name__icontains=name)
            context["header"] = f"Searching for {name} in Products"
        else:
            context["products"] = Product.objects.all()
            context["header"] = "All Available Products"
        return context


class StoreCreate(CreateView):
    model = Product
    fields =['name','img','description','price']
    template_name = 'store_create.html'
    
    def get_success_url(self):
        return reverse('store_detail', kwargs={'pk': self.object.pk})
    
class StoreDetail(DetailView):
    model = Product
    template_name = 'store_detail.html'

class StoreUpdate(UpdateView):
    model = Product
    fields =['name','img','description','price']
    template_name ='store_update.html'
    
    def get_success_url(self):
        return reverse('store_detail', kwargs={'pk': self.object.pk})

class StoreDelete(DeleteView):
    model = Product
    template_name='store_delete_confirmation.html'
    success_url= '/stores'


class Signup(View):
    # show a form to fill out
    def get(self, request):
        form = UserCreationForm()
        context = {"form": form}
        return render(request, "registration/signup.html", context)
    # on form submit, validate the form and login the user.
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("store_list")
        else:
            context = {"form": form}
            return render(request, "registration/signup.html", context)


class Cart(TemplateView):
    template_name = "cart.html" 

    def cart(self, request):
        customer = request.user.customer
        order_created = Order.objects.get_or_create(customer=customer, complete=False)
        items = Order.orderitem_set.all()
        cartitems = Order.get_cart_items

        context = {"order_created": order_created, "items": items, "cartitems": cartitems}
        return render(request, "cart.html", context)
