from django.contrib import admin
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models
from django.db.models import Count

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'),
            ('>10', 'OK')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        else:
            return queryset.filter(inventory__gte=10)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_filter = ['collection', 'last_update', InventoryFilter]

    @admin.display(ordering='collection')
    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        else:
            return 'OK'


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders_count']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']


    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        url = (
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({'customer__id__exact': str(customer.id)})
        )
        return format_html('<a href={}>{} orders</a>', url, customer.orders_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(orders_count=Count('order'))


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'featured_product', 'products_count']
    list_per_page = 10

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({"collection__id__exact": str(collection.id)})
        )
        return format_html('<a href={}>{}</a>', url, collection.products_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('product'))


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_fullname', 'payment_status', 'placed_at']
    ordering = ['id']
    list_per_page = 10

    def customer_fullname(self, order):
        return f'{order.customer.first_name} {order.customer.last_name}'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('customer')