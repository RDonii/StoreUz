from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Collection, Product
from .serializers import ProductSerializer, CollectionSerializer
from rest_framework import status
from django.http import HttpRequest, HttpResponse
from django.db.models.aggregates import Count

@api_view(['GET', 'POST'])
def product_list(request: HttpRequest):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()[:20]
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request: HttpRequest, id: int):
    product = get_object_or_404(Product, pk=id)
    if request.method=='GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method=='PUT':
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method=='DELETE':
        if product.orderitem.count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def collection_list(request: HttpRequest):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(products_count=Count('product')).all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request: HttpRequest, pk: int):
    collection = get_object_or_404(Collection, pk=pk)
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)