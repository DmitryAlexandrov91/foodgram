"""Представления api проекта foodgram."""
import csv
import os

from django.db.models import Sum
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404, redirect
from django.http import FileResponse, HttpResponseRedirect, JsonResponse
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated, AllowAny)
from rest_framework.views import APIView
from djoser.views import UserViewSet

from foodgram.constants import CSV_FOLDER_PATH
from recipes.models import (
    Favorite,
    Ingredient, IngredientInRecipe,
    Recipe, RecipeLinks,
    ShoppingCart, Tag)
from .filters import IngredientFilter, RecipeFilter
from .permissions import IsAuthorOrReadOnly
from users.models import User, Subscribe
from .serializers import (
    ReadUserSerializer,
    CreateUserSerializer,
    AvatarSerializer,
    TagSerializer,
    ReadRecipeSerializer,
    CreateRecipeSerializer,
    IngredientSerializer,
    ShoppingCartAndFavoriteSerializer,
    SubscribeSerializer,
    ResetPasswordSerializer
)


class CustomUserViewSet(UserViewSet):
    """Представление эндпоинта users."""

    queryset = User.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticatedOrReadOnly,]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        return ReadUserSerializer

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        serializer = ReadUserSerializer(
            request.user,
            context={'request': request})
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['post'])
    def set_password(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if user.check_password(serializer.data.get('current_password')):
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Указан неверный пароль'},
                        status=status.HTTP_400_BAD_REQUEST)

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
        url_path='subscriptions',
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(
            subscribed_author__user=request.user)
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            paginated_queryset,
            many=True,
            context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='subscribe'
    )
    def subscribe(self, request, id=None):
        author = get_object_or_404(User, pk=id)
        user = self.request.user
        if request.method == 'POST':
            if author == user:
                return Response(
                    {"errors": "Нельзя подписаться на самого себя."},
                    status=status.HTTP_400_BAD_REQUEST)
            if Subscribe.objects.filter(
                author=author, user=user
            ).exists():
                return Response(
                    {"errors": "Вы уже подписаны на этого пользователя."},
                    status=status.HTTP_400_BAD_REQUEST)
            Subscribe.objects.create(author=author, user=user)
            serializer = SubscribeSerializer(
                author,
                context={'request': request})
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            subscription = Subscribe.objects.filter(
                author=author, user=user
            )
            if subscription.exists():
                subscription.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {"errors": "Вы не подписаны на этого пользователя."},
                status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для эндпоинта tags."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = []
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Представление для эндпоинта recipes."""

    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

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
        permission_classes=[],
    )
    def get_link(self, request, pk=None):
        links = RecipeLinks.objects.get(recipe_id=pk)
        if links:
            return JsonResponse(
                {'short-link': request.build_absolute_uri(
                    f'/s/{links.short_link}')})
        return JsonResponse(
            {"detail": f"Рецепт с ID {pk} не найден."},
            status=status.HTTP_404_NOT_FOUND
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
            recipe_in_shopping_cart = ShoppingCart.objects.filter(
                user=request.user, recipe=recipe)
            if recipe_in_shopping_cart:
                recipe_in_shopping_cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)

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
    """Представление для эндпоинта ingredients."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    http_method_names = ['get']
    permission_classes = (AllowAny,)
    pagination_class = None
    filter_backends = (DjangoFilterBackend, )
    filterset_class = IngredientFilter
    search_fields = ('^name',)


class RedirectShortLink(View):
    """Представление для редиректа ссылок."""

    permission_classes = []

    def get(self, request, short_link):
        link = get_object_or_404(
            RecipeLinks,
            short_link=short_link
        )
        return redirect(
            request.build_absolute_uri(
                f'/recipes/{link.recipe_id}/'))
