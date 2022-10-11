from django.urls import path
from . import views

urlpatterns = [
   path('', views.Home.as_view(), name="home"), 
   path('stores/', views.StoreList.as_view(), name="store_list"),
   path('stores/new', views.StoreCreate.as_view(), name="artist_create"),
]