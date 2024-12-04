from djoser.views import UserViewSet

from users.models import User
from .serializers import (
    ReadUserSerializer,
    CreateUserSerializer,
    AvatarSerializer
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        return ReadUserSerializer

    @action(
        methods=['put'],
        detail=False,
        url_path='me/avatar')
    def avatar_update(self, request):
        serializer = AvatarSerializer(request.user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(
            {'detail': 'Аватар успешно изменен!'},
            status=status.HTTP_204_NO_CONTENT)
