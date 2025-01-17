from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

@api_view(['GET'])
def Products(request):
    products = Product.objects.all()  # Fetch all products from the database
    serializer = ProductSerializer(products, many=True)  # Serialize the products
    return Response(serializer.data)  # Return serialized data as a response


