from django.shortcuts import render
from store.models import Customer, Collection, Product, Order, OrderItem

def homeview(request):
    customers = Customer.objects.filter(email__icontains='.com')
    collections = Collection.objects.filter(featured_product__isnull=True)
    products = Product.objects.filter(inventory__lt=10)
    orders = Order.objects.filter(customer__id=1)
    orderItems = OrderItem.objects.filter(product__collection__id=3)

    context = {
        "customers": customers,
        "collections": collections,
        "products": products,
        "orders": orders,
        "orderItems": orderItems,
    }
    print(context)

    return render(request, 'index.html', context=context)