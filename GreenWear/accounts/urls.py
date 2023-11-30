from django.urls import path
from . import views

urlpatterns = [
    path('accedi/', views.login, name='login'),
    path('registrati/', views.signup, name='signup'),
    path('profilo/', views.account, name='account'),

    path('preferiti/', views.wishlist, name='wishlist'),
    path('preferiti/modifica/', views.modify_wishlist, name='modify_wishlist'),

]