# from rest_framework import permissions
# from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAutenticatedAndReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method == 'GET' and request.user.is_authenticated


class IsAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user)
