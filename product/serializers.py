from rest_framework import serializers
from django.db.models import Avg
from .models import Category, Product, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def validate_text(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Текст отзыва слишком короткий"
            )
        return value


class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'description',
            'price',
            'category',
            'reviews',
            'rating',
        ]

    def validate_title(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Название слишком короткое"
            )
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Цена должна быть больше 0"
            )
        return value

    def get_rating(self, obj):
        return obj.reviews.aggregate(
            Avg('stars')
        )['stars__avg']


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'products_count',
        ]

    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Название категории слишком короткое"
            )
        return value

    def get_products_count(self, obj):
        return obj.product_set.count()
    
    