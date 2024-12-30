"""Представления api проекта foodgram."""
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    SAFE_METHODS)
from rest_framework.response import Response

from .utils import get_report_response
from recipes.models import (
    Favorite,
    Ingredient, IngredientInRecipe,
    Recipe, RecipeLinks,
    ShoppingCart, Tag)
from users.models import User, Subscribe
from .filters import IngredientFilter, RecipeFilter
from .paginations import RecipePagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    AvatarSerializer,
    CreateRecipeSerializer,
    CreateUserSerializer,
    IngredientSerializer,
    ReadRecipeSerializer,
    ReadUserSerializer,
    ResetPasswordSerializer,
    ShoppingCartAndFavoriteSerializer,
    SubscribeSerializer,
    TagSerializer
)


class CustomUserViewSet(UserViewSet):
    """Представление эндпоинта users."""

    queryset = User.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get_serializer_class(self):
        """Определяет класс сериализатора в зависимости от действия."""
        if self.action == 'create':
            return CreateUserSerializer
        return ReadUserSerializer

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        """Определяет поведение при GET запросе к /me."""
        serializer = ReadUserSerializer(
            request.user,
            context={'request': request})
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['post'])
    def set_password(self, request):
        """Определяет поведение при POST запросе к /set_password."""
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
        """Определяет поведение при запросе к /avatar."""
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
        """Определяет поведение при GET запросе к /subscriptions."""
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
        """Определяет поведение при POST/DELETE запросах к /subscribe."""
        author = get_object_or_404(User, pk=id)
        user = self.request.user
        serializer = SubscribeSerializer(
            author,
            data={'user': user},
            context={
                'request': request,
                'author': author}
        )
        serializer.is_valid(raise_exception=True)
        if request.method == 'POST':
            Subscribe.objects.create(author=author, user=user)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            user.follower.filter(
                author=author
            ).delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT)


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
    pagination_class = RecipePagination

    def get_serializer_class(self):
        """Определяет класс сериализатора в зависимости от метода запроса."""
        if self.action in SAFE_METHODS:
            return ReadRecipeSerializer
        return CreateRecipeSerializer

    def perform_create(self, serializer):
        """Добавляет поле author в сериализатор."""
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        url_path='get-link',
        permission_classes=[],
    )
    def get_link(self, request, pk=None):
        """Определяет поведение при GET запросе к /get-link."""
        links = get_object_or_404(RecipeLinks, recipe_id=pk)
        if links:
            return JsonResponse(
                {'short-link': request.build_absolute_uri(
                    f'/s/{links.short_link}')})
        return JsonResponse(
            {'detail': f'Рецепт с ID {pk} не найден.'},
            status=status.HTTP_404_NOT_FOUND
        )

    @action(detail=False,
            url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        """Определяет поведение при GET запросе к /download_shopping_cart."""
        ingredients = IngredientInRecipe.objects.filter(
            recipe__shopping_cart__user=request.user).values(
                'ingredient__name',
                'ingredient__measurement_unit',
                'recipe__name').annotate(
                amount=Sum('amount')).order_by('recipe__name')
        return get_report_response(ingredients)

    def to_create_delete(self, request, model, pk=None):
        """Вспомогательная DRY функция для shopping_cart и favorite."""
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            serializer = ShoppingCartAndFavoriteSerializer(
                recipe,
                data=request.data
            )
            serializer.is_valid(raise_exception=True)
            if model.objects.filter(
                user=request.user, recipe=recipe
            ).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            model.objects.create(user=request.user, recipe=recipe)
            modified_data = {
                **serializer.data,
                'image': request.build_absolute_uri(
                    recipe.image.url
                )
            }
            return Response(modified_data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            object = get_object_or_404(
                model,
                user=request.user,
                recipe=recipe
            )
            object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        url_path='shopping_cart',
        methods=['post', 'delete']
    )
    def shopping_cart(self, request, pk=None):
        """Обрабатывает POST/DELETE запросы к /shopping_cart."""
        return self.to_create_delete(request, ShoppingCart, pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        pagination_class=None,
        url_path='favorite'
    )
    def favorite(self, request, pk=None):
        """Обрабатывает POST/DELETE запросы к /favorite."""
        return self.to_create_delete(request, Favorite, pk)


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
        """Получает пороткую ссылку из БД и редиректит на полную."""
        link = get_object_or_404(
            RecipeLinks,
            short_link=short_link
        )
        return redirect(
            request.build_absolute_uri(
                f'/recipes/{link.recipe_id}/'))
