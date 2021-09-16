from rest_framework import permissions


class IsAdminBot(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_bot and request.user.role
