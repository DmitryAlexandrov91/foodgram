# from rest_framework import permissions
# from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import BasePermission


class AutenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method == 'GET' and request.user.is_authenticated

