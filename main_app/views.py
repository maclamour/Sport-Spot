from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Product, Order, OrderItem, Cart
from django.core.exceptions import ObjectDoesNotExist

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
            cartitems = order.orderitem_set.all()  # Use the OrderItem model instead of Order

            context["order_created"] = order
            context["cartitems"] = cartitems  # Update the context variable
        else:
            context["order_created"] = None
            context["cartitems"] = []

        return context

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user = request.user

    if user.is_authenticated:
        customer = user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed_order=False)

        # Use the OrderItem model instead of OrderItem
        order_item, created = OrderItem.objects.get_or_create(product=product, order=order, defaults={'quantity': 0})
        order_item.quantity += 1
        order_item.save()

    return redirect('cart')



def update_cart( item_id, new_quantity):
    try:
        cart_item = OrderItem.objects.get(pk=item_id)
        cart_item.quantity = new_quantity
        cart_item.save()

        cart = cart_item.order
        cart_item_count = cart.orderitem_set.aggregate(cart_item_count=models.Sum('quantity'))['cart_item_count']
        cart_total_price = cart.total_price()

        return JsonResponse({
            'quantity': new_quantity,
            'total_price': cart_item.total_price(),
            'cart_item_count': cart_item_count,
            'cart_total_price': cart_total_price
        })
    except OrderItem.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    template_name = "checkout.html"

    def get(self, request):
        # Retrieve the user's cart and associated items
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed_order=False)
        cartitems = order.orderitem_set.all()

        # Calculate the total price for the order
        cart_total_price = sum(item.total_price() for item in cartitems)

        context = {
            'cartitems': cartitems,
            'cart_total_price': cart_total_price,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        if request.method == 'POST':
            # Retrieve customer information and order details from the form
            name = request.POST.get('name')
            email = request.POST.get('email')
            address = request.POST.get('address')
            # ... other form fields ...

            # Create a new Order record in your database
            order = Order.objects.create(
                customer=request.user.customer,
                name=name,
                email=email,
                address=address,
                completed_order=True,  # Mark the order as completed
                # ... other order fields ...
            )

            # Transfer items from the user's cart to the order
            user_cart = Cart.objects.get(user=request.user)
            order_items = user_cart.order_items.all()
            for cart_item in order_items:
                OrderItem.objects.create(
                    product=cart_item.product,
                    order=order,
                    quantity=cart_item.quantity,
                )

            # Clear the user's cart
            user_cart.order_items.clear()

            # Handle any additional actions related to order processing
            # ...

            # Optionally, you can display a success message to the user
            messages.success(request, 'Your order has been placed successfully.')

            # Redirect the user to a thank-you page or another relevant page
            return redirect('thank_you')

        # Handle GET requests or invalid form submissions
        return render(request, 'checkout.html')  # Render the checkout page if needed
    


def process_order(request):
    if request.method == 'POST':
        try:
            # Retrieve customer information and order details from the form
            name = request.POST.get('name')
            email = request.POST.get('email')
            address = request.POST.get('address')

            # Create a new Order record in your database
            order = Order.objects.create(
                customer=request.user.customer,
                name=name,
                email=email,
                address=address,
                completed_order=True,  # Mark the order as completed
                # ... other order fields ...
            )

            # Transfer items from the user's cart to the order
            # Retrieve the user's cart using the custom manager
            user_cart = Cart.objects.get_cart_for_user(request.user)
            order_items = user_cart.order_items.all()
            for cart_item in order_items:
                OrderItem.objects.create(
                    product=cart_item.product,
                    order=order,
                    quantity=cart_item.quantity,
                )

            # Clear the user's cart
            user_cart.order_items.clear()

            # Send a confirmation email to the customer
            subject = 'Order Confirmation'
            message = 'Thank you for your order! Your order has been received and will be processed shortly.'
            from_email = 'your_email@example.com'  # Replace with your email address
            recipient_list = [email]  # Use the customer's email address
            send_mail(subject, message, from_email, recipient_list)

            # Optionally, you can display a success message to the user
            messages.success(request, 'Your order has been placed successfully.')

            # Redirect the user to a thank-you page or another relevant page
            return redirect('home.html')
        except ObjectDoesNotExist as e:
            # Handle the case where an object does not exist (e.g., user's cart)
            messages.error(request, 'An error occurred while processing your order.')
            return render(request, 'checkout.html')
        except Exception as e:
            # Handle other exceptions as needed
            messages.error(request, 'An error occurred while processing your order.')
            return render(request, 'checkout.html')

    else:
        # Handle GET requests or invalid form submissions
        return render(request, 'checkout.html')

