from rest_framework import serializers

from ProductApp.models import Review, Product


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model. Will include Replies later"""
    class Meta:
        model = Review
        fields = '__all__'


class ProductReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, source="review_set")

    class Meta:
        model = Product
        fields = ['reviews']
