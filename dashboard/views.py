from django.shortcuts import render

from utils.custom_viewset import CustomViewSet
from utils.response_wrapper import ResponseWrapper
from .serializers import *
from .models import *

# Create your views here.


class CategoryViewSet(CustomViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'pk'


class ProductViewSet(CustomViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'pk'

    def product_details(self, request,id, *args, **kwargs):
        qs = Product.objects.filter(id = id).last()
        if not qs:
            return ResponseWrapper(error_msg='Product Not Found', status=400)
        
        serializer  = ProductDetailsSerializer(instance=qs)
        return ResponseWrapper(data=serializer.data, status=200)
