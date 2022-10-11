from audioop import reverse
from django.shortcuts import render
from django.views import View # <- View class to handle requests
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from .models import Product
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse





# Create your views here.

# Here we will be creating a class called Home and extending it from the View class
class Home(TemplateView):
    template_name = "home.html"

# class Store:
#     def __init__(self,name,img):
#         self.name = name
#         self.img = img


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