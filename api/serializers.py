from rest_framework import serializers
from .models import Category, Products


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'subcategory_of', 'parent_id']

class ProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    price = serializers.FloatField()
    categories = serializers.ListField(child=serializers.IntegerField())
