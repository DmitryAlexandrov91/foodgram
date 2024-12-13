from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, TagViewSet, RecipeViewSet, IngredientViewSet

app_name = 'api'

recipe_detail = RecipeViewSet.as_view({'get': 'retrieve'})

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipeViewSet, basename='recipe')
router.register(r'ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]


