from rest_framework.permissions import BasePermission


class IsSuperuser(BasePermission):
    """
    超级管理员
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsAdmin(BasePermission):
    """
    超级管理员
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)
