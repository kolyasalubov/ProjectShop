from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportActionModelAdmin

from ProjectShop.custom_filters import MultipleChoiceListFilter
from order.models import Order, OrderItems


class ShippingStatusListFilter(MultipleChoiceListFilter):
    title = _("shipping status")
    parameter_name = "shipping_status__in"
    
    def lookups(self, request, model_admin):
        return Order.ShippingStatus.choices


class OrderItemsInline(admin.TabularInline):
    model = OrderItems
    readonly_fields = ("order_items_quantity", "product")
    extra = 1


class OrderAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    fields = (
        "user",
        "payment_method",
        "shipping_status",
        "payment_status",
        "shippingAddress_id",
        "order_date",
    )
    readonly_fields = ("order_date",)
    inlines = (OrderItemsInline,)
    list_display = (
        "user",
        "payment_status",
        "shipping_status",
    )
    list_editable = (
        "payment_status",
        "shipping_status",
    )
    list_filter = (
        "payment_status",
        ShippingStatusListFilter,
    )
    ordering = (
        "payment_status",
        "shipping_status",
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + (
                "user",
                "payment_method",
                "shippingAddress_id",
            )
        return self.readonly_fields
    
    def has_add_permission(self, request):
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class OrderItemsAdmin(admin.ModelAdmin):
    fields = ("order_items_quantity", "order", "product")
    list_display = ("product", "order_items_quantity", "order")
    list_filter = ("product",)
    ordering = (
        "product",
        "order",
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItems, OrderItemsAdmin)
