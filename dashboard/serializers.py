from asyncore import read
from dataclasses import field, fields
from .models import *
from rest_framework import serializers
# from drf_extra_fields.fields import Base64FileField, Base64ImageField
from django.utils.html import strip_tags
from utils.calculate_price import calculate_price
import datetime
from django.utils import timezone
from datetime import datetime
from django.db.models import Q

# ..........***.......... Category ..........***..........

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

# ..........***.......... Product ..........***..........

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

# ..........***.......... Product Details ..........***..........

class ProductDetailsSerializer(serializers.ModelSerializer):
    category_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def get_category_details(self, obj):
        if obj:
            serializer = CategorySerializer(obj.category)
            return serializer.data
        return None
