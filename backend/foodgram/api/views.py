from djoser.views import UserViewSet

from users.models import User
from .serializers import ReadUserSerializer, CreateUserSerializer


class UserViewSet(UserViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        return ReadUserSerializer
