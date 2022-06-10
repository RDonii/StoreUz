from django.contrib import admin
from store.admin import ProductAdmin
from store.models import Product
from tags.models import TaggedItem
from django.contrib.contenttypes.admin import GenericTabularInline


class TagItemInline(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ['tag']
    extra = 0

class CustomProductAdmin(ProductAdmin):
    inlines = [TagItemInline]

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
