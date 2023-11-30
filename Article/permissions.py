from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsSuperOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        elif request.method in SAFE_METHODS:
            return True
