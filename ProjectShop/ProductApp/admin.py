from django.contrib import admin
from django.utils.html import format_html

from ProductApp.models import Product, ProductCategory, ProductSubcategory, Tag, Review, ProductMedia


class MediaInline(admin.TabularInline):
    model = ProductMedia
    fields = ('image_tag', "image")


class ProductAdmin(admin.ModelAdmin):
    inlines = (MediaInline,)
    fields = ('name', ('price', 'stock_quantity'), 'description', ('categories', 'subcategories', 'tags'))
    list_filter = ('media',)
    pass


class ProductMediaAdmin(admin.ModelAdmin):
    fields = ('image_tag', 'image')
    readonly_fields = ('image_tag',)


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory)
admin.site.register(ProductSubcategory)
admin.site.register(Tag)
admin.site.register(Review)
admin.site.register(ProductMedia, ProductMediaAdmin)
