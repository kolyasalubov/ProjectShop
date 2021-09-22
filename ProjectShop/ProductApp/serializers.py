from rest_framework import serializers
from ProductApp.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Review view. Replies for review (likes and dislikes) will be added later
    """
    class Meta:
        model = Review
        fields = "__all__"
