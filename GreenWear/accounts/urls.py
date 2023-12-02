from django.urls import path
from . import views

urlpatterns = [
    path('accedi/', views.LoginView.as_view(), name='login'),
    path('registrati/', views.SignupView.as_view(), name='signup'),
    path('profilo/', views.account, name='account'),
    path('logout/', views.logout, name='logout'),
    path('impostazioni/', views.profile_settings, name='profile_settings'),

    path('preferiti/', views.wishlist, name='wishlist'),
    path('preferiti/modifica/', views.modify_wishlist, name='modify_wishlist'),
    path('preferiti/rimuovi/', views.remove_wishlist, name='remove_wishlist'),
]