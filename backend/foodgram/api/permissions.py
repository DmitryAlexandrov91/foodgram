"""Кастомные пермишены приложения api."""
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    """Доступ только для чтения или автору объекта."""

    def has_permission(self, request, view):
        """Доступ к оъекту для чтения или аутентифицированным."""
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Доступ к действию с объектом для чтения или автору контента."""
        return (request.method in SAFE_METHODS
                or obj.author == request.user)
