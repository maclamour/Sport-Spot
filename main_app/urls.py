from django.urls import path
from . import views

urlpatterns = [
   path('', views.Home.as_view(), name="home"), 
   path('stores/', views.StoreList.as_view(), name="store_list"),
]