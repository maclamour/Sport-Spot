from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Product, Order, OrderItem, Cart  # Import necessary models
from django.http import JsonResponse

class Home(TemplateView):
    template_name = "home.html"

class StoreList(TemplateView):
    template_name = "store_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")

        if name is not None:
            context["products"] = Product.objects.filter(name__icontains=name)
            context["header"] = f"Searching for {name} in Products"
        else:
            context["products"] = Product.objects.all()
            context["header"] = "All Available Products"
        return context

class StoreCreate(CreateView):
    model = Product
    fields = ['name', 'img', 'description', 'price']
    template_name = 'store_create.html'

    def get_success_url(self):
        return reverse('store_detail', kwargs={'pk': self.object.pk})

class StoreDetail(DetailView):
    model = Product
    template_name = 'store_detail.html'

class StoreUpdate(UpdateView):
    model = Product
    fields = ['name', 'img', 'description', 'price']
    template_name = 'store_update.html'

    def get_success_url(self):
        return reverse('store_detail', kwargs={'pk': self.object.pk})

class StoreDelete(DeleteView):
    model = Product
    template_name = 'store_delete_confirmation.html'
    success_url = '/stores'

class Signup(View):
    def get(self, request):
        form = UserCreationForm()
        context = {"form": form}
        return render(request, "registration/signup.html", context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("login"))  # Redirect to the 'login' URL name
        else:
            context = {"form": form}
            return render(request, "registration/signup.html", context)


class Cart(TemplateView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            customer = self.request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, completed_order=False)
            items = order.orderitem_set.all()
            cartitems = order.orderitem_set.all()

            context["order_created"] = order
            context["items"] = items
            context["cartitems"] = cartitems
        else:
            context["order_created"] = None
            context["items"] = []
            context["cartitems"] = []

        return context


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user = request.user

    if user.is_authenticated:
        customer = user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed_order=False)

        order_item, created = OrderItem.objects.get_or_create(product=product, order=order, defaults={'quantity': 0})
        order_item.quantity += 1
        order_item.save()

    return redirect('store_list')


def update_cart(request, item_id, new_quantity):
    cart_item = OrderItem.objects.get(pk=item_id)

    cart_item.quantity = new_quantity
    cart_item.save()

    total_price = cart_item.total_price()

    cart = Order.objects.get(pk=cart_item.order.id)
    cart_item_count = cart.orderitem_set.aggregate(cart_item_count=models.Sum('quantity'))['cart_item_count']
    cart_total_price = cart.total_price()

    return JsonResponse({
        'quantity': new_quantity,
        'total_price': total_price,
        'cart_item_count': cart_item_count,
        'cart_total_price': cart_total_price
    })