from rest_framework import serializers

from ProductApp.models import Product, ProductMedia, ProductCategory, ProductSubcategory, Tag, Review
from UserApp.serializers import UserSerializer


class ProductCategorySerializer(serializers.ModelSerializer):
	"""Serializer for ProductCategory model"""
	class Meta:
		model = ProductCategory
		fields = '__all__'


class ProductSubcategorySerializer(serializers.ModelSerializer):
	"""Serializer for ProductSubcategory model"""
	class Meta:
		model = ProductSubcategory
		fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
	"""Serializer for Tag model"""
	class Meta:
		model = Tag
		fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
	"""Serializer for Product model"""
	categories = ProductCategorySerializer(many=True, read_only=True)
	subcategories = ProductSubcategorySerializer(many=True, read_only=True)
	tags = TagSerializer(many=True, read_only=True)

	class Meta:
		model = Product
		fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
	"""Serializer for Review model"""
	product = ProductSerializer(read_only=True)
	user = UserSerializer(read_only=True)

	class Meta:
		model = Review
		fields = '__all__'


class ProductMediaSerializer(serializers.ModelSerializer):
	"""Serializer for ProductMedia model"""
	product = ProductSerializer(read_only=True)

	class Meta:
		model = ProductMedia
		fields = '__all__'
