from django.contrib import admin

from ProductApp.models import Product, ProductCategory, ProductSubcategory, Tag, Review, ProductMedia


admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductSubcategory)
admin.site.register(Tag)
admin.site.register(Review)
admin.site.register(ProductMedia)
