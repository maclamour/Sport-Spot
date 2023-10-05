from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.Home.as_view(), name="home"), 
    path('stores/', views.StoreList.as_view(), name="store_list"),
    path('stores/new/', views.StoreCreate.as_view(), name='store_create'),
    path('stores/<int:pk>/', views.StoreDetail.as_view(), name="store_detail"),
    path('stores/<int:pk>/update/', views.StoreUpdate.as_view(), name="store_update"),
    path('stores/<int:pk>/delete/', views.StoreDelete.as_view(), name="store_delete"),
    path('accounts/signup/', views.Signup.as_view(), name="signup"),
    path('cart/', views.Cart.as_view(), name="cart"),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
