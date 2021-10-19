from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet 
from rest_framework.response import Response
from rest_framework.decorators import action
from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from ProductApp.forms import ReviewForm

from ProductApp.models import Product, ProductCategory, ProductSubcategory, ProductMedia, Review, Tag
from ProductApp.serializers import (ProductSerializer, ProductCategorySerializer,
                                    ProductSubcategorySerializer, ProductMediaSerializer,
                                    ReviewSerializer, TagSerializer)


class ProductViewSet(ReadOnlyModelViewSet):
    """This is viewset for Product model"""
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductCategoryViewSet(ReadOnlyModelViewSet):
    """This is viewset for ProductCategory model"""
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all()


class ProductSubcategoryViewSet(ReadOnlyModelViewSet):
    """This is viewset for ProductSubcategory model"""
    serializer_class = ProductSubcategorySerializer
    queryset = ProductSubcategory.objects.all()


class TagViewSet(ReadOnlyModelViewSet):
    """This is viewset for Tag model"""
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class ProductMediaViewSet(ReadOnlyModelViewSet):
    """This is viewset for ProductMedia model"""
    serializer_class = ProductMediaSerializer
    queryset = ProductMedia.objects.all()
    

class ReviewViewSet(ModelViewSet):
    """
    ViewSet to view and write reviews for specified in path product
    """
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        queryset_list = Review.objects.filter(product=product_id)
        return queryset_list

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        serializer.save(product=Product.objects.get(pk=product_id))


def ProductOverviewPageView(request, product_id = 1):
    product__object =  Product.get_product_by_id(product_id=product_id)
    product_media = ProductMedia.get_media_by_product(product = product__object)
    product_media_video = ProductMedia.get_media_video_by_product(product = product__object)
    product_all = ProductMedia.get_all_products()

    new_review = None
    reviews = Review.get_review_by_product(product = product__object)


    if request.method == 'POST':
        review_form = ReviewForm(user = request.user ,data=request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.product = product__object
            new_review.save()

            return redirect('product_overview', product_id=product_id )
    else:
        review_form = ReviewForm()

    context={
        'product_object' : product__object,
        'product_media' : product_media,
        'product_media_video' : product_media_video,
        'product_all' : product_all,

        'comments': reviews,
        'new_comment': new_review,
        'comment_form': review_form
    }

    return render(request, 'ProductApp/ProductOverviewPage.html', context)


