from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView

from .forms import CustomAuthenticationForm, CustomUserCreationForm, CustomUserChangeForm
from products.models import Product
from accounts.models import CustomUser, NUM_LIVES
from gamification.models import Quiz


# --- LOGIN --- #
class LoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'

# --- SIGNUP --- #
class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')

# --- WISHLIST --- #
@login_required(login_url='login')
def wishlist(request):
    products = Product.objects.filter(users_wishlist=request.user)
    
    context = {
        'wishlist_products': products,
    }
    return render(request, 'accounts/wishlist.html', context)

@login_required(login_url='login')
def modify_wishlist(request):

    if request.method == 'POST':
        product_name = request.POST.get('name')
        product = get_object_or_404(Product, name=product_name)
        
        if product.users_wishlist.filter(id=request.user.id).exists():
            product.users_wishlist.remove(request.user)
            data = {'is_present': False}
        else:
            product.users_wishlist.add(request.user)
            data = {'is_present': True}

        return JsonResponse(data)

@login_required(login_url='login')
def remove_wishlist(request):

    if request.method == 'POST':
        product_name = request.POST.get('name')
        product = get_object_or_404(Product, name=product_name)
        products = Product.objects.filter(users_wishlist=request.user)
        
        product.users_wishlist.remove(request.user)
        data = {'num_items': len(products)}

        return JsonResponse(data)


# --- ACCOUNT --- #
@login_required(login_url='login')
def account(request):
    users = CustomUser.objects.all().order_by('-green_points')[0:5]
    levels = CustomUser.LEVELS
    quiz = Quiz.objects.last()
    
    context = {
        'top_users': users,
        'levels': levels,
        'quiz': quiz,
        'lives': range(NUM_LIVES),
    }
    return render(request, 'accounts/account.html', context)

# --- LOGOUT --- #
@login_required(login_url='login')
def logout(request):
    response = LogoutView.as_view()(request)
    
    return redirect('home')

# --- PROFILE SETTINGS --- #
@login_required(login_url='login')
def profile_settings(request):
    
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            messages.info(request, 'Il profilo è stato aggiornato correttamente')
            return redirect('profile_settings')
    else:
        form = CustomUserChangeForm(instance=request.user)
        
    context = {
        'form': form,
    }
    
    return render(request, 'accounts/settings.html', context)
