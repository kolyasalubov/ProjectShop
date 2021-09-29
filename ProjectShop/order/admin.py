from django.contrib import admin

from order.models import OrderModel, OrderItemsModel
from order.export import export_to_csv


class OrderItemsInline(admin.TabularInline):
    model = OrderItemsModel
    readonly_fields = ('order_items_qantity', 'product')
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    fields = ('user', 'payment_method', 'shipping_status', 'payment_status', 'shippingAddress_id', 'order_date')
    readonly_fields = ('order_date', )
    inlines = (OrderItemsInline, )
    list_display = ('user', 'payment_status', 'shipping_status', )
    list_editable = ('payment_status', 'shipping_status', )
    list_filter = ('payment_status', 'shipping_status', )
    ordering = ('payment_status', 'shipping_status', )
    actions = (export_to_csv, )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('user', 'payment_method', 'shippingAddress_id')
        return self.readonly_fields

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class OrderItemsAdmin(admin.ModelAdmin):
    fields = ('order_items_qantity', 'order', 'product')
    list_display = ('product', 'order_items_qantity', 'order')
    list_filter = ('product', )
    ordering = ('product', 'order', )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(OrderModel, OrderAdmin)
admin.site.register(OrderItemsModel, OrderItemsAdmin)

