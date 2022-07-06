from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, CustomerSerializer, ProductSerializer, CollectionSerializer, ReviewSerializer, UpdateCartItemSerializer
from .pagination import CustomPageNumberPagination
from .models import Cart, CartItem, Collection, Customer, Product, Review
from .filters import ProductFilter
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = CustomPageNumberPagination
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']

    # def get_serializer_context(self):
    #     return {'request': self.request}

    def destroy(self, request: HttpRequest, pk: int):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitem.count() > 0:
            return Response( 'Delete related order items first.', status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('product')).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.product_set.count > 0:
            return Response('Delete related products first.', status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            collection.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

class CartViewSet(RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer

class CartItemViewSet(ModelViewSet):

    http_method_names = ['patch', 'post', 'delete', 'get']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')

    def get_serializer_context(self):
        contex = super().get_serializer_context()
        contex['cart_id'] = self.kwargs['cart_pk']
        return contex

class CustomerViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer