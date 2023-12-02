from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('modifica_quantità/<slug:slug>/', views.modify_item_quantity, name='modify_item_quantity'),
    path('rimuovi/<slug:slug>/', views.remove_item, name='remove_item'),
]