from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from ProductApp.models import Product, ProductCategory, ProductSubcategory, Tag, Review, ProductMedia


class IsAvailableProductFilter(admin.SimpleListFilter):
    title = _('is available')
    parameter_name = 'is_available'

    def lookups(self, request, model_admin):
        return (
            ('available', _('available')),
            ('not_available', _('not available')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'available':
            return queryset.filter(stock_quantity__gt=0)
        if self.value() == 'not_available':
            return queryset.filter(stock_quantity__lte=0)


class MediaInline(admin.TabularInline):
    model = ProductMedia
    fields = ('media_type', 'video_link', 'image', 'image_tag')
    readonly_fields = ('image_tag',)
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = (MediaInline,)
    fields = ('name', 'slug', 'price', 'stock_quantity', 'description', 'categories', 'subcategories', 'tags')
    list_display = ('name', 'price', 'stock_quantity', 'short_description')
    list_filter = (IsAvailableProductFilter,)
    search_fields = ('name', 'description')
    filter_horizontal = ('categories', 'subcategories', 'tags')

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = slugify(obj.name)
        slug, i = obj.slug, 1
        while Product.objects.filter(slug=obj.slug):
            obj.slug = f'{slug}-{i}'
            i += 1
        super(ProductAdmin, self).save_model(request, obj, form, change)


class ProductMediaAdmin(admin.ModelAdmin):
    fields = ('product', 'media_type', 'video_link', 'image', 'image_tag')
    readonly_fields = ('image_tag',)
    list_display = ('name', 'media_type', 'video_link', 'image', 'small_image_tag')
    list_filter = ('media_type',)
    search_fields = ('product__name',)
    raw_id_fields = ('product',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'user', 'product', 'rating')
    list_filter = ('is_active', 'rating')
    search_fields = ('product__name', 'user__email')

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return False

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        enabled_fields = {'is_active'}
        for field in form.base_fields:
            if field in enabled_fields:
                continue
            form.base_fields[field].disabled = True
        return form


class ProductCategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = slugify(obj.name)
        slug, i = obj.slug, 1
        while ProductCategory.objects.filter(slug=obj.slug):
            obj.slug = f'{slug}-{i}'
            i += 1
        super(ProductCategoryAdmin, self).save_model(request, obj, form, change)


class ProductSubcategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = slugify(obj.name)
        slug, i = obj.slug, 1
        while ProductSubcategory.objects.filter(slug=obj.slug):
            obj.slug = f'{slug}-{i}'
            i += 1
        super(ProductSubcategoryAdmin, self).save_model(request, obj, form, change)


class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = slugify(obj.name)
        slug, i = obj.slug, 1
        while Tag.objects.filter(slug=obj.slug):
            obj.slug = f'{slug}-{i}'
            i += 1
        super(TagAdmin, self).save_model(request, obj, form, change)


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(ProductSubcategory, ProductSubcategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(ProductMedia, ProductMediaAdmin)
