from django.shortcuts import render, redirect
from .models import Product

from rest_framework.response import Response
from .serializers import ProductSerializer
from rest_framework.decorators import api_view


@api_view(['GET'])
def list_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)

@api_view(['POST'])
def create_product(request):
    serializer = ProductSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['POST'])
def update_product(request, id):
    product = Product.objects.get(id=id)
    serializer = ProductSerializer(data=request.data, instance=product)

    if serializer.is_valid():
        serializer.save()


    return Response(serializer.data)

@api_view(['DELETE'])
def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()

    return Response('Product has been deleted')
