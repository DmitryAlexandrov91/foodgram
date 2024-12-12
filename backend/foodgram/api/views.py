from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet

import csv
import os
from django.http import FileResponse
from django.db.models import Sum

from users.models import User, Subscribe
from recipes.models import (
    Tag, Recipe, Ingredient, IngredientInRecipe, ShoppingCart, Favorite)
from .serializers import (
    ReadUserSerializer,
    CreateUserSerializer,
    AvatarSerializer,
    TagSerializer,
    ReadRecipeSerializer,
    CreateRecipeSerializer,
    IngredientSerializer,
    ShoppingCartAndFavoriteSerializer,
    SubscribeSerializer
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, filters
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework import status

from api.constants import CSV_FOLDER_PATH


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
                status=status.HTTP_204_NO_CONTENT)
        if request.method == 'PUT':
            serializer = AvatarSerializer(request.user, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    {'avatar': request.build_absolute_uri(
                        request.user.avatar.url)})

    @action(
        detail=False,
        url_path='subscriptions'
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(subscribed_author__user=request.user)
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            paginated_queryset,
            many=True,
            context={'request': request})
        return self.get_paginated_response(serializer.data)


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
            {'detail': 'Рецепт успешно удалён'},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        detail=True,
        url_path='get-link',
        permission_classes=[]
    )
    def get_link(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        return Response(
            {"short-link": request.build_absolute_uri(
                recipe.image.url)}
        )

    @action(detail=False,
            url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        ingredients = IngredientInRecipe.objects.filter(
            recipe__shopping_cart__user=request.user).values(
                'ingredient__name',
                'ingredient__measurement_unit',
                'recipe__name').annotate(
                amount=Sum('amount')).order_by('recipe__name')
        shopping_cart = [(
            i["ingredient__name"],
            i["ingredient__measurement_unit"],
            i["amount"],
            i["recipe__name"]) for i in ingredients]
        file_path = os.path.join(
            CSV_FOLDER_PATH,
            f'shopping_cart_{request.user.username}.csv')
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                ['Ингредиент', 'Единица измерения', 'Количество', 'Рецепт']
            )
            for ingredient in shopping_cart:
                writer.writerow(ingredient)
        response = FileResponse(
            open(file_path, 'rb'),
            content_type='text/csv')
        response[
            'Content-Disposition'] = (
                f'attachment; filename="{os.path.basename(file_path)}"')
        return response

    @action(
        detail=True,
        url_path='shopping_cart',
        methods=['post', 'delete']
    )
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            serializer = ShoppingCartAndFavoriteSerializer(
                recipe,
                data=request.data
            )
            serializer.is_valid(raise_exception=True)
            if ShoppingCart.objects.filter(
                user=request.user, recipe=recipe
                    ).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            ShoppingCart.objects.create(user=request.user, recipe=recipe)
            modified_data = {
                **serializer.data,
                'image': request.build_absolute_uri(
                            recipe.image.url)}
            return Response(
                modified_data,
                status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            recipe_in_shopping_cart = get_object_or_404(
                ShoppingCart,
                user=request.user,
                recipe=recipe)
            recipe_in_shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete'],
        pagination_class=None,
        url_path='favorite'
    )
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        favorite = Favorite.objects.filter(
            user=request.user,
            recipe__id=pk)
        if request.method == 'POST':
            if favorite.exists():
                return Response(
                    status=status.HTTP_400_BAD_REQUEST
                )
            Favorite.objects.create(user=request.user, recipe=recipe)
            serializer = ShoppingCartAndFavoriteSerializer(
                recipe,
                context={'request': request})
            modified_data = {
                **serializer.data,
                'image': request.build_absolute_uri(
                            recipe.image.url)}
            return Response(modified_data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if favorite.exists():
                favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = []
