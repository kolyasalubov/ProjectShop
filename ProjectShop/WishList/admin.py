from django.contrib import admin

from WishList.models import WishList


class WishListAdmin(admin.ModelAdmin):
    fields = ('user',)
    list_display = ('user',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(WishList, WishListAdmin)
