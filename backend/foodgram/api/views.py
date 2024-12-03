from djoser.views import UserViewSet

from users.models import User
from .serializers import ReadUserSerializer, CreateUserSerializer
from rest_framework.pagination import LimitOffsetPagination


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        return ReadUserSerializer
