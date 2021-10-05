from rest_framework.serializers import ModelSerializer

from ProductApp.models import Product, ProductMedia, ProductCategory, ProductSubcategory, Tag, Review
from UserApp.serializers import UserSerializer


class ProductCategorySerializer(ModelSerializer):
	"""Serializer for ProductCategory model"""
	class Meta:
		model = ProductCategory
		fields = '__all__'


class ProductSubcategorySerializer(ModelSerializer):
	"""Serializer for ProductSubcategory model"""
	class Meta:
		model = ProductSubcategory
		fields = '__all__'


class TagSerializer(ModelSerializer):
	"""Serializer for Tag model"""
	class Meta:
		model = Tag
		fields = '__all__'


class ProductSerializer(ModelSerializer):
	"""Serializer for Product model"""
	categories = ProductCategorySerializer(many=True, read_only=True)
	subcategories = ProductSubcategorySerializer(many=True, read_only=True)
	tags = TagSerializer(many=True, read_only=True)

	class Meta:
		model = Product
		fields = '__all__'


class ProductMediaSerializer(ModelSerializer):
	"""Serializer for ProductMedia model"""
	product = ProductSerializer(read_only=True)

	class Meta:
		model = ProductMedia
		fields = '__all__'


class ReviewSerializer(ModelSerializer):
    """
    Serializer for Review view. Replies for review (likes and dislikes) will be added later
    """
    class Meta:
        model = Review
        fields = "__all__"
