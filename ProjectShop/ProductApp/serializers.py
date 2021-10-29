from rest_framework.serializers import ModelSerializer

from ProductApp.models import (
    Product,
    ProductImage,
    ProductVideo,
    ProductCategory,
    ProductSubcategory,
    Tag,
    Review,
    Reply,
)


class ProductCategorySerializer(ModelSerializer):
    """Serializer for ProductCategory model"""

    class Meta:
        model = ProductCategory
        fields = ["name"]


class ProductSubcategorySerializer(ModelSerializer):
    """Serializer for ProductSubcategory model"""

    class Meta:
        model = ProductSubcategory
        fields = ["name"]


class TagSerializer(ModelSerializer):
    """Serializer for Tag model"""

    class Meta:
        model = Tag
        fields = ["name", "group"]


class ProductNameSerializer(ModelSerializer):
    """Serializer for Product model with only name"""

    class Meta:
        model = Product
        fields = ["name"]


class ProductImageSerializer(ModelSerializer):
    """Serializer for ProductImage model"""

    class Meta:
        model = ProductImage
        fields = ["image"]


class ProductVideoSerializer(ModelSerializer):
    """Serializer for ProductVideo model"""

    class Meta:
        model = ProductVideo
        fields = ["video_link"]


class ProductSerializer(ModelSerializer):
    """Serializer for Product model"""

    categories = ProductCategorySerializer(many=True, read_only=True)
    subcategories = ProductSubcategorySerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True)
    video_links = ProductVideoSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "description",
            "stock_quantity",
            "categories",
            "subcategories",
            "tags",
            "images",
            "video_links",
        ]


class ReviewSerializer(ModelSerializer):
    """
    Serializer for Review view.    """

    product = ProductNameSerializer(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"

class ReplySerializer(ModelSerializer):
    """
    Serializer for reply view
    """
    product = ProductNameSerializer(read_only=True)
    class Meta:
        model = Reply
        fields = ["review",
                  "reaction"]