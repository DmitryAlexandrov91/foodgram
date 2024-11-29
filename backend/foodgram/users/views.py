# from rest_framework import viewsets, serializers, status
# from rest_framework.decorators import action
# from rest_framework.permissions import (
#     IsAuthenticated, IsAuthenticatedOrReadOnly)
# from rest_framework.response import Response

# from .models import User


# class UserViewSet(viewsets.ModelViewSet):
#     """Вьюсет для просмотра профиля и создания пользователя."""
#     queryset = User.objects.all()
#     permission_classes = [IsAuthenticatedOrReadOnly,]
