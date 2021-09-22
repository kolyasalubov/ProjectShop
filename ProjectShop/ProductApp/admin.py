from django.contrib import admin


from ProductApp.models import Product, Review, ProductCategory, ProductSubcategory, Tag


admin.site.register(Product)
admin.site.register(Review)
admin.site.register(ProductCategory)
admin.site.register(ProductSubcategory)
admin.site.register(Tag)
