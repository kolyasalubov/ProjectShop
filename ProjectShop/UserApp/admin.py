from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from UserApp.models import User


class UserAdmin(BaseUserAdmin):

    def has_delete_permission(self, request, obj=None) -> bool:
        """Restrict self deletion and deletion for not superusers"""
        return request.user != obj and request.user.is_superuser

    def has_add_permission(self, request) -> bool:
        """Restrict adding for not superusers"""
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None) -> bool:
        """Allow changing for superusers and for admin ot change users"""
        if obj:
            return not obj.role or request.user.is_superuser
        return request.user.is_superuser

    def get_form(self, request, obj=None, **kwargs):
        """Enable certain fields in form"""
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        enabled_fields = set()  # type: Set[str]

        if not is_superuser and obj != request.user and obj and not obj.role:
            enabled_fields |= {'is_active'}

        if is_superuser:
            enabled_fields |= set(form.base_fields.keys())  # going to enable all fields

        if obj == request.user:
            enabled_fields.remove('is_active')
            if obj.role:
                enabled_fields |= {'middle_name', 'birth_date'}

        for f in form.base_fields:
            if f in enabled_fields:
                continue
            form.base_fields[f].disabled = True  # disable form fields except enabled fields
        return form

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('phone_number', 'first_name', 'last_name', 'role', 'email', 'is_superuser', 'is_active')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('phone_number', )}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'middle_name', 'birth_date', 'email')}),
        ('Permissions', {'fields': ('is_active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'phone_number', 'email', 'role', 'password1', 'password2'),
        }),
    )
    search_fields = ('phone_number',)
    ordering = ('phone_number',)
    filter_horizontal = ()


# registering new django admin...
admin.site.register(User, UserAdmin)
# unregistering the Group model from admin.
admin.site.unregister(Group)
