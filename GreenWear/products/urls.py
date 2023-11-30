from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>/', views.product, name='product'),
    path('<slug:slug>/aggiungi_al_carrello/', views.add_to_cart, name='add_to_cart'),
]