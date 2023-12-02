from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import CustomUser, Discount


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["username", "first_name", "last_name", "email", "age", "phone_number", "green_points"]
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', ),
        }),
    )
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'age', 'profile_picture')}),
        ('Data', {'fields': ('green_points', 'level', 'quiz_lives')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Stats', {'fields': ('last_login', 'date_joined')}),
    ) 

@admin.register(Discount)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'saving')
