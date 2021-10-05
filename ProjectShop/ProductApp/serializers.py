from rest_framework.serializers import ModelSerializer, SlugRelatedField

from ProductApp.models import Product, ProductMedia, ProductCategory, ProductSubcategory, Tag, Review


class ProductCategorySerializer(ModelSerializer):
	"""Serializer for ProductCategory model"""
	class Meta:
		model = ProductCategory
		fields = ['name']


class ProductSubcategorySerializer(ModelSerializer):
	"""Serializer for ProductSubcategory model"""
	class Meta:
		model = ProductSubcategory
		fields = ['name']


class TagSerializer(ModelSerializer):
	"""Serializer for Tag model"""
	class Meta:
		model = Tag
		fields = ['name']


class ProductSerializer(ModelSerializer):
	"""Serializer for Product model"""
	categories = ProductCategorySerializer(many=True, read_only=True)
	subcategories = ProductSubcategorySerializer(many=True, read_only=True)
	tags = TagSerializer(many=True, read_only=True)
	media = SlugRelatedField(many=True, read_only=True, slug_field='video_link')

	class Meta:
		model = Product
		fields = ['id', 'name', 'price', 'description', 'stock_quantity',
				  'categories', 'subcategories', 'tags', 'media']


class ProductNameSerializer(ModelSerializer):
	"""Serializer for Product model with only name"""
	class Meta:
		model = Product
		fields = ['name']


class ProductMediaSerializer(ModelSerializer):
	"""Serializer for ProductMedia model"""
	product = ProductNameSerializer(read_only=True)

	class Meta:
		model = ProductMedia
		fields = '__all__'


class ReviewSerializer(ModelSerializer):
	"""Serializer for Review view. Replies for review (likes and dislikes) will be added later"""
	product = ProductNameSerializer(read_only=True)

	class Meta:
		model = Review
		fields = "__all__"
