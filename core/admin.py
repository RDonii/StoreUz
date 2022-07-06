from django.contrib import admin
from store.admin import ProductAdmin
from store.models import Product
from tags.models import TaggedItem
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", 'email', 'first_name', 'last_name'),
            },
        ),
    )

class TagItemInline(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ['tag']
    extra = 0

class CustomProductAdmin(ProductAdmin):
    inlines = [TagItemInline]

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)