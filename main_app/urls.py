from django.urls import path
from . import views

urlpatterns = [
   path('', views.Home.as_view(), name="home"), 
   path('stores/', views.StoreList.as_view(), name="store_list"),
   path('stores/new/', views.StoreCreate.as_view(),name='store_create'),
   path('stores/<int:pk>/', views.StoreDetail.as_view(), name="store_detail"),
   path('stores/<int:pk>/update', views.StoreUpdate.as_view(), name="store_update"),
   path('stores/<int:pk>/delete', views.StoreDelete.as_view(), name="store_delete"),
   path('accounts/signup/', views.Signup.as_view(), name="signup"),
   path('cart/', views.Cart.as_view(), name="cart")
]