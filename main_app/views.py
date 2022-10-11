from django.shortcuts import render
from django.views import View # <- View class to handle requests
from django.http import HttpResponse # <- a class to handle sending a type of response
#...
from django.views.generic.base import TemplateView
from .models import Product


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