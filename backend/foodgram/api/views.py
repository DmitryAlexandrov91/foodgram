from djoser.views import UserViewSet

import csv
from django.http import HttpResponse

from users.models import User
from recipes.models import Tag, Recipe, Ingredient, ShoppingCart
from .serializers import (
    ReadUserSerializer,
    CreateUserSerializer,
    AvatarSerializer,
    TagSerializer,
    ReadRecipeSerializer,
    CreateRecipeSerializer,
    IngredientSerializer,
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, filters
from rest_framework.permissions import SAFE_METHODS


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        return ReadUserSerializer

    @action(
        methods=['put', 'delete'],
        detail=False,
        url_path='me/avatar')
    def avatar(self, request):
        if request.method == 'DELETE':
            request.user.avatar.delete()
            return Response(
                {'detail': 'Аватар успешно удалён'},
            )
        if request.method == 'PUT':
            serializer = AvatarSerializer(request.user, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    {'avatar': request.user.avatar.url},
                )


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = []
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = []
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name')

    def get_serializer_class(self):
        if self.action in SAFE_METHODS:
            return ReadRecipeSerializer
        return CreateRecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def destroy(self, request, pk=None):
        recipe = Recipe.objects.filter(pk=pk)
        recipe.delete()
        return Response(
            {'detail': 'Рецепт успешно удалён'}
        )
    
    # @action(detail=False,
    #         url_path='download_shopping_cart')
    # def download_shopping_cart(self, request):
    #     data = ShoppingCart.objects.filter(
    #         user=request.user
    #     )
    #     response = HttpResponse(content_type='text/csv')
    #     response['Content-Disposition'] = 'attachment; filename="shopping_cart.csv"'
    #     writer = csv.writer(response)
    #     # writer.writerow(['Поле 1', 'Поле 2'])
    #     for obj in data:
    #         print(obj)
    

    # @action(
    #     detail=True,
    #     methods=['get'],
    #     url_path='get_link')
    # def get_short_link(self, request, pk=None):
    #     serializer = ShortUrlSerializer(
    #         data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         return Response(
    #             {'short_url': serializer.validated_data}
    #         )


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = []
